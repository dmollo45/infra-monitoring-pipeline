
import json
import boto3
import os
import time
from datetime import datetime
from decimal import Decimal
from botocore.exceptions import ClientError

# Initialize AWS clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
cloudwatch = boto3.client('cloudwatch')

# Environment variables
DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE', 'InfraMetrics')
REGION = os.environ.get('AWS_REGION', 'us-east-1')
DLQ_URL = os.environ.get('DLQ_URL', '')  # Optional: SQS DLQ URL

# Initialize DynamoDB table
table = dynamodb.Table(DYNAMODB_TABLE)

# Constants
TTL_DAYS = 30
MAX_RETRIES = 3
BATCH_SIZE = 25  # DynamoDB batch write limit


def lambda_handler(event, context):
    """
    Main Lambda handler for processing S3 events and writing to DynamoDB.
    
    Args:
        event: S3 event notification
        context: Lambda context object
        
    Returns:
        dict: Response with status code and processing summary
    """
    print(f"Received event: {json.dumps(event)}")
    
    processing_summary = {
        'total_files': 0,
        'total_metrics': 0,
        'successful_writes': 0,
        'failed_writes': 0,
        'errors': []
    }
    
    try:
        # Parse S3 event records
        records = event.get('Records', [])
        if not records:
            return create_response(400, 'No S3 records found in event')
        
        processing_summary['total_files'] = len(records)
        
        # Process each S3 object
        for record in records:
            try:
                process_s3_record(record, processing_summary)
            except Exception as e:
                error_msg = f"Failed to process record: {str(e)}"
                print(f"ERROR: {error_msg}")
                processing_summary['errors'].append(error_msg)
        
        # Publish CloudWatch metrics
        publish_processing_metrics(processing_summary)
        
        # Determine response status
        if processing_summary['failed_writes'] > 0:
            status_code = 207  # Multi-status (partial success)
        else:
            status_code = 200
        
        return create_response(status_code, 'Processing complete', processing_summary)
        
    except Exception as e:
        error_msg = f"Lambda execution failed: {str(e)}"
        print(f"CRITICAL ERROR: {error_msg}")
        processing_summary['errors'].append(error_msg)
        
        # Send to DLQ if configured
        if DLQ_URL:
            send_to_dlq(event, error_msg)
        
        return create_response(500, error_msg, processing_summary)


def process_s3_record(record, summary):
    """
    Process a single S3 event record.
    
    Args:
        record: S3 event record
        summary: Processing summary dictionary to update
    """
    # Extract S3 object details
    bucket_name = record['s3']['bucket']['name']
    object_key = record['s3']['object']['key']
    
    print(f"Processing: s3://{bucket_name}/{object_key}")
    
    # Download and parse JSON from S3
    metrics = download_and_parse_json(bucket_name, object_key)
    
    if not metrics:
        raise ValueError(f"No valid metrics found in {object_key}")
    
    summary['total_metrics'] += len(metrics)
    
    # Validate metrics structure
    validated_metrics = validate_metrics(metrics)
    
    # Write to DynamoDB with retry logic
    success_count, failure_count = write_to_dynamodb_batch(validated_metrics)
    
    summary['successful_writes'] += success_count
    summary['failed_writes'] += failure_count
    
    print(f"Processed {len(metrics)} metrics: {success_count} succeeded, {failure_count} failed")


def download_and_parse_json(bucket, key):
    """
    Download JSON file from S3 and parse it.
    
    Args:
        bucket: S3 bucket name
        key: S3 object key
        
    Returns:
        list: Parsed metrics data
        
    Raises:
        ClientError: If S3 download fails
        json.JSONDecodeError: If JSON parsing fails
    """
    try:
        # Download object from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        
        # Parse JSON
        data = json.loads(content)
        
        # Handle both single object and array formats
        if isinstance(data, dict):
            return [data]
        elif isinstance(data, list):
            return data
        else:
            raise ValueError(f"Unexpected JSON structure: {type(data)}")
            
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchKey':
            print(f"ERROR: S3 object not found: {key}")
        elif error_code == 'AccessDenied':
            print(f"ERROR: Access denied to S3 object: {key}")
        raise
        
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {key}: {str(e)}")
        raise


def validate_metrics(metrics):
    """
    Validate metrics structure and filter out invalid entries.
    
    Args:
        metrics: List of metric dictionaries
        
    Returns:
        list: Validated metrics
    """
    validated = []
    required_fields = ['metric_id', 'timestamp', 'metric_type', 'value', 'hostname']
    
    for metric in metrics:
        # Check required fields
        if not all(field in metric for field in required_fields):
            print(f"WARNING: Skipping invalid metric (missing fields): {metric}")
            continue
        
        # Validate data types
        try:
            metric['timestamp'] = int(metric['timestamp'])
            metric['value'] = float(metric['value'])
        except (ValueError, TypeError) as e:
            print(f"WARNING: Skipping metric with invalid data types: {metric}")
            continue
        
        validated.append(metric)
    
    return validated


def write_to_dynamodb_batch(metrics):
    """
    Write metrics to DynamoDB using batch operations with retry logic.
    
    Args:
        metrics: List of validated metrics
        
    Returns:
        tuple: (success_count, failure_count)
    """
    success_count = 0
    failure_count = 0
    
    # Process in batches of 25 (DynamoDB limit)
    for i in range(0, len(metrics), BATCH_SIZE):
        batch = metrics[i:i + BATCH_SIZE]
        
        # Retry logic for batch write
        for attempt in range(MAX_RETRIES):
            try:
                with table.batch_writer() as batch_writer:
                    for metric in batch:
                        item = prepare_dynamodb_item(metric)
                        batch_writer.put_item(Item=item)
                
                success_count += len(batch)
                break  # Success - exit retry loop
                
            except ClientError as e:
                error_code = e.response['Error']['Code']
                
                if error_code == 'ProvisionedThroughputExceededException':
                    # Throttling - retry with exponential backoff
                    if attempt < MAX_RETRIES - 1:
                        wait_time = (2 ** attempt) * 0.5  # 0.5s, 1s, 2s
                        print(f"DynamoDB throttled, retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        print(f"ERROR: DynamoDB throttling persists after {MAX_RETRIES} attempts")
                        failure_count += len(batch)
                        
                        # Send failed batch to DLQ
                        if DLQ_URL:
                            send_batch_to_dlq(batch)
                else:
                    # Non-retryable error
                    print(f"ERROR: DynamoDB write failed: {error_code}")
                    failure_count += len(batch)
                    break
                    
            except Exception as e:
                print(f"ERROR: Unexpected error writing to DynamoDB: {str(e)}")
                failure_count += len(batch)
                break
    
    return success_count, failure_count


def prepare_dynamodb_item(metric):
    """
    Prepare metric for DynamoDB insertion.
    
    Args:
        metric: Metric dictionary
        
    Returns:
        dict: DynamoDB item with TTL
    """
    # Calculate TTL (30 days from now)
    ttl = int(time.time()) + (TTL_DAYS * 24 * 60 * 60)
    
    # Convert float to Decimal for DynamoDB
    item = {
        'metric_id': metric['metric_id'],
        'timestamp': metric['timestamp'],
        'metric_type': metric['metric_type'],
        'value': Decimal(str(metric['value'])),
        'unit': metric.get('unit', 'unknown'),
        'hostname': metric['hostname'],
        'region': metric.get('region', REGION),
        'environment': metric.get('environment', 'unknown'),
        'ttl': ttl
    }
    
    # Add optional tags if present
    if 'tags' in metric:
        item['tags'] = metric['tags']
    
    return item


def publish_processing_metrics(summary):
    """
    Publish custom CloudWatch metrics for monitoring.
    
    Args:
        summary: Processing summary dictionary
    """
    try:
        cloudwatch.put_metric_data(
            Namespace='InfraMonitoring/Pipeline',
            MetricData=[
                {
                    'MetricName': 'MetricsProcessed',
                    'Value': summary['total_metrics'],
                    'Unit': 'Count',
                    'Timestamp': datetime.utcnow()
                },
                {
                    'MetricName': 'SuccessfulWrites',
                    'Value': summary['successful_writes'],
                    'Unit': 'Count',
                    'Timestamp': datetime.utcnow()
                },
                {
                    'MetricName': 'FailedWrites',
                    'Value': summary['failed_writes'],
                    'Unit': 'Count',
                    'Timestamp': datetime.utcnow()
                },
                {
                    'MetricName': 'FilesProcessed',
                    'Value': summary['total_files'],
                    'Unit': 'Count',
                    'Timestamp': datetime.utcnow()
                }
            ]
        )
        print("Published CloudWatch metrics successfully")
    except Exception as e:
        print(f"WARNING: Failed to publish CloudWatch metrics: {str(e)}")


def send_to_dlq(event, error_message):
    """
    Send failed event to Dead Letter Queue (SQS).
    
    Args:
        event: Original Lambda event
        error_message: Error description
    """
    if not DLQ_URL:
        return
    
    try:
        sqs = boto3.client('sqs')
        sqs.send_message(
            QueueUrl=DLQ_URL,
            MessageBody=json.dumps({
                'event': event,
                'error': error_message,
                'timestamp': datetime.utcnow().isoformat()
            })
        )
        print(f"Sent failed event to DLQ: {DLQ_URL}")
    except Exception as e:
        print(f"ERROR: Failed to send to DLQ: {str(e)}")


def send_batch_to_dlq(batch):
    """
    Send failed batch of metrics to DLQ.
    
    Args:
        batch: List of metrics that failed to write
    """
    if not DLQ_URL:
        return
    
    try:
        sqs = boto3.client('sqs')
        sqs.send_message(
            QueueUrl=DLQ_URL,
            MessageBody=json.dumps({
                'failed_metrics': batch,
                'timestamp': datetime.utcnow().isoformat()
            })
        )
        print(f"Sent {len(batch)} failed metrics to DLQ")
    except Exception as e:
        print(f"ERROR: Failed to send batch to DLQ: {str(e)}")


def create_response(status_code, message, data=None):
    """
    Create standardized Lambda response.
    
    Args:
        status_code: HTTP status code
        message: Response message
        data: Optional response data
        
    Returns:
        dict: Lambda response object
    """
    response = {
        'statusCode': status_code,
        'message': message
    }
    
    if data:
        response['data'] = data
    
    return response

