import json
import boto3
import os
from datetime import datetime
from decimal import Decimal
from botocore.exceptions import ClientError
import time

# Initialize AWS clients with explicit region
s3_client = boto3.client('s3', region_name='eu-west-1')
dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
cloudwatch = boto3.client('cloudwatch', region_name='eu-west-1')

# Environment variables
TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'InfraMetrics')
REGION = os.environ.get('REGION', 'eu-west-1')

# Constants
MAX_RETRIES = 3
BATCH_SIZE = 25
TTL_DAYS = 30

def lambda_handler(event, context):
    """
    Main handler for S3 event notifications.
    Processes JSON files and writes metrics to DynamoDB.
    """
    print(f"Received event: {json.dumps(event)}")

    metrics_processed = 0
    metrics_failed = 0
    files_processed = 0

    try:
        for record in event.get('Records', []):
            try:
                bucket = record['s3']['bucket']['name']
                key = record['s3']['object']['key']

                print(f"Processing file: s3://{bucket}/{key}")

                metrics_data = download_and_parse_json(bucket, key)

                if metrics_data:
                    valid_metrics = validate_metrics(metrics_data)

                    if valid_metrics:
                        success_count, fail_count = write_to_dynamodb_batch(valid_metrics)
                        metrics_processed += success_count
                        metrics_failed += fail_count
                        files_processed += 1
                    else:
                        print(f"No valid metrics found in {key}")
                        metrics_failed += 1
                else:
                    print(f"Failed to parse JSON from {key}")
                    metrics_failed += 1

            except Exception as e:
                print(f"Error processing record: {str(e)}")
                metrics_failed += 1

        publish_processing_metrics(metrics_processed, metrics_failed, files_processed)

        return create_response(200, {
            'metrics_processed': metrics_processed,
            'metrics_failed': metrics_failed,
            'files_processed': files_processed
        })

    except Exception as e:
        print(f"Lambda execution error: {str(e)}")
        publish_processing_metrics(metrics_processed, metrics_failed, files_processed)
        return create_response(500, {'error': str(e)})

def download_and_parse_json(bucket, key):
    """Downloads JSON file from S3 and parses it."""
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)
        return data

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchKey':
            print(f"File not found: {key}")
        elif error_code == 'AccessDenied':
            print(f"Access denied to file: {key}")
        else:
            print(f"S3 error: {error_code}")
        return None

    except json.JSONDecodeError as e:
        print(f"Invalid JSON in file {key}: {str(e)}")
        return None

    except Exception as e:
        print(f"Unexpected error downloading {key}: {str(e)}")
        return None

def validate_metrics(data):
    """Validates metrics data structure."""
    if not isinstance(data, dict):
        print("Data is not a dictionary")
        return []

    metrics = data.get('metrics', {})
    if not isinstance(metrics, dict):
        print("Metrics field is not a dictionary")
        return []

    required_fields = ['timestamp', 'region', 'instance_id']
    for field in required_fields:
        if field not in data:
            print(f"Missing required field: {field}")
            return []

    valid_metrics = []
    for metric_name, metric_value in metrics.items():
        if isinstance(metric_value, (int, float)):
            metric_item = {
                'metric_name': metric_name,
                'value': metric_value,
                'timestamp': data['timestamp'],
                'region': data.get('region', 'unknown'),
                'instance_id': data.get('instance_id', 'unknown'),
                'environment': data.get('environment', 'production')
            }
            valid_metrics.append(metric_item)

    return valid_metrics

def prepare_dynamodb_item(metric):
    """Prepares a metric for DynamoDB insertion."""
    timestamp_str = metric['timestamp']
    if isinstance(timestamp_str, str):
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        timestamp_unix = int(dt.timestamp())
    else:
        timestamp_unix = int(timestamp_str)

    ttl = int(time.time()) + (TTL_DAYS * 24 * 60 * 60)

    item = {
        'metric_id': f"{metric['metric_name']}#{metric['instance_id']}#{timestamp_unix}",
        'timestamp': timestamp_unix,
        'metric_type': metric['metric_name'],
        'value': Decimal(str(metric['value'])),
        'hostname': metric['instance_id'],
        'region': metric['region'],
        'environment': metric['environment'],
        'ttl': ttl
    }

    return item

def write_to_dynamodb_batch(metrics):
    """Writes metrics to DynamoDB using batch operations."""
    table = dynamodb.Table(TABLE_NAME)
    success_count = 0
    failure_count = 0

    for i in range(0, len(metrics), BATCH_SIZE):
        batch = metrics[i:i + BATCH_SIZE]

        for attempt in range(MAX_RETRIES):
            try:
                with table.batch_writer() as batch_writer:
                    for metric in batch:
                        item = prepare_dynamodb_item(metric)
                        batch_writer.put_item(Item=item)

                success_count += len(batch)
                print(f"Successfully wrote batch of {len(batch)} items")
                break

            except ClientError as e:
                error_code = e.response['Error']['Code']

                if error_code == 'ProvisionedThroughputExceededException':
                    if attempt < MAX_RETRIES - 1:
                        wait_time = (2 ** attempt) * 0.5
                        print(f"Throttled. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        print(f"Failed after {MAX_RETRIES} retries")
                        failure_count += len(batch)
                else:
                    print(f"DynamoDB error: {error_code}")
                    failure_count += len(batch)
                    break

            except Exception as e:
                print(f"Unexpected error writing batch: {str(e)}")
                failure_count += len(batch)
                break

    return success_count, failure_count

def publish_processing_metrics(processed, failed, files):
    """Publishes custom CloudWatch metrics for monitoring."""
    try:
        cloudwatch.put_metric_data(
            Namespace='InfraMonitoring/LogProcessor',
            MetricData=[
                {
                    'MetricName': 'MetricsProcessed',
                    'Value': processed,
                    'Unit': 'Count',
                    'Timestamp': datetime.utcnow()
                },
                {
                    'MetricName': 'MetricsFailed',
                    'Value': failed,
                    'Unit': 'Count',
                    'Timestamp': datetime.utcnow()
                },
                {
                    'MetricName': 'FilesProcessed',
                    'Value': files,
                    'Unit': 'Count',
                    'Timestamp': datetime.utcnow()
                }
            ]
        )
        print(f"Published metrics: Processed={processed}, Failed={failed}, Files={files}")

    except Exception as e:
        print(f"Error publishing CloudWatch metrics: {str(e)}")

def create_response(status_code, body):
    """Creates standardized Lambda response."""
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
