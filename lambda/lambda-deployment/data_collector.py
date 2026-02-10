import json
import boto3
import random
import time
from datetime import datetime
from decimal import Decimal

# Initialize AWS clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
cloudwatch = boto3.client('cloudwatch')

# Environment variables (will be set in Lambda configuration)
S3_BUCKET = 'infra-monitoring-pipeline-data'
DYNAMODB_TABLE = 'InfraMetrics'

def lambda_handler(event, context):
    try:
        # Generate synthetic infrastructure metrics
        timestamp = int(time.time())  # Unix timestamp as integer
        current_time = datetime.utcnow().isoformat()
        
        metrics = [
            {
                'metric_id': f'cpu-{timestamp}',
                'metric_type': 'cpu_utilization',
                'timestamp': timestamp,  # FIXED: Now as Number, not String
                'value': Decimal(str(random.uniform(20.0, 80.0))),
                'instance_id': f'i-{random.randint(100000, 999999)}',
                'region': 'eu-west-1',
                'collected_at': current_time
            },
            {
                'metric_id': f'mem-{timestamp}',
                'metric_type': 'memory_usage',
                'timestamp': timestamp,  # FIXED: Now as Number, not String
                'value': Decimal(str(random.uniform(30.0, 90.0))),
                'instance_id': f'i-{random.randint(100000, 999999)}',
                'region': 'eu-west-1',
                'collected_at': current_time
            },
            {
                'metric_id': f'disk-{timestamp}',
                'metric_type': 'disk_usage',
                'timestamp': timestamp,  # FIXED: Now as Number, not String
                'value': Decimal(str(random.uniform(40.0, 85.0))),
                'instance_id': f'i-{random.randint(100000, 999999)}',
                'region': 'eu-west-1',
                'collected_at': current_time
            },
            {
                'metric_id': f'net-{timestamp}',
                'metric_type': 'network_traffic',
                'timestamp': timestamp,  # FIXED: Now as Number, not String
                'value': Decimal(str(random.uniform(100.0, 1000.0))),
                'instance_id': f'i-{random.randint(100000, 999999)}',
                'region': 'eu-west-1',
                'collected_at': current_time
            }
        ]
        
        # Save to DynamoDB
        table = dynamodb.Table(DYNAMODB_TABLE)
        for metric in metrics:
            table.put_item(Item=metric)
        
        # Save to S3
        s3_key = f'raw-metrics/{datetime.utcnow().strftime("%Y/%m/%d")}/metrics-{timestamp}.json'
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=json.dumps(metrics, default=str),
            ContentType='application/json'
        )
        
        # Publish custom metrics to CloudWatch
        cloudwatch.put_metric_data(
            Namespace='InfraMonitoring',
            MetricData=[
                {
                    'MetricName': 'cpu_utilization',
                    'Value': float(metrics['value']),
                    'Unit': 'Percent',
                    'Timestamp': datetime.utcnow()
                },
                {
                    'MetricName': 'memory_usage',
                    'Value': float(metrics['value']),
                    'Unit': 'Percent',
                    'Timestamp': datetime.utcnow()
                },
                {
                    'MetricName': 'disk_usage',
                    'Value': float(metrics['value']),
                    'Unit': 'Percent',
                    'Timestamp': datetime.utcnow()
                },
                {
                    'MetricName': 'network_traffic',
                    'Value': float(metrics['value']),
                    'Unit': 'Kilobytes',
                    'Timestamp': datetime.utcnow()
                }
            ]
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Metrics collected successfully',
                'metrics_count': len(metrics),
                's3_key': s3_key,
                'timestamp': timestamp
            })
        }
        
    except Exception as e:
        print(f'Error in lambda_handler: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
