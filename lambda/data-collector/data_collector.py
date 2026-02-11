
import json
import boto3
import random
from datetime import datetime
from decimal import Decimal
import os

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
cloudwatch = boto3.client('cloudwatch')

BUCKET_NAME = 'infra-monitoring-pipeline-data'
TABLE_NAME = 'InfraMetrics'  # ✅ Fixed: Correct table name
REGION = 'eu-west-1'

def lambda_handler(event, context):
    """
    Collects infrastructure metrics and writes them to S3 and DynamoDB.
    Now combines all 4 metrics into a single JSON file per collection run.
    """
    
    timestamp = int(datetime.now().timestamp())
    collected_at = datetime.now().isoformat()
    
    # Generate random instance ID for this collection run
    instance_id = f"i-{random.randint(100000, 999999)}"
    
    # Generate all 4 metrics for this instance
    metrics = []
    
    # 1. CPU Utilization
    metrics.append({
        "metric_id": f"cpu-{timestamp}",
        "metric_type": "cpu_utilization",
        "timestamp": timestamp,
        "value": str(round(random.uniform(20.0, 90.0), 2)),
        "instance_id": instance_id,
        "region": REGION,
        "collected_at": collected_at
    })
    
    # 2. Memory Usage
    metrics.append({
        "metric_id": f"mem-{timestamp}",
        "metric_type": "memory_usage",
        "timestamp": timestamp,
        "value": str(round(random.uniform(40.0, 95.0), 2)),
        "instance_id": instance_id,
        "region": REGION,
        "collected_at": collected_at
    })
    
    # 3. Disk Usage
    metrics.append({
        "metric_id": f"disk-{timestamp}",
        "metric_type": "disk_usage",
        "timestamp": timestamp,
        "value": str(round(random.uniform(30.0, 85.0), 2)),
        "instance_id": instance_id,
        "region": REGION,
        "collected_at": collected_at
    })
    
    # 4. Network Traffic
    metrics.append({
        "metric_id": f"net-{timestamp}",
        "metric_type": "network_traffic",
        "timestamp": timestamp,
        "value": str(round(random.uniform(100.0, 1000.0), 2)),
        "instance_id": instance_id,
        "region": REGION,
        "collected_at": collected_at
    })
    
    # Write all metrics to S3 as a single JSON array file
    try:
        date_path = datetime.now().strftime('%Y/%m/%d')
        s3_key = f"raw-metrics/{date_path}/metrics-{timestamp}.json"
        
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=json.dumps(metrics, indent=2),
            ContentType='application/json'
        )
        
        print(f"Successfully wrote {len(metrics)} metrics to S3: {s3_key}")
        
    except Exception as e:
        print(f"Error writing to S3: {str(e)}")
        raise
    
    # Write metrics to DynamoDB
    try:
        table = dynamodb.Table(TABLE_NAME)
        
        with table.batch_writer() as batch:
            for metric in metrics:
                item = {
                    'metric_id': metric['metric_id'],
                    'timestamp': timestamp,
                    'metric_type': metric['metric_type'],
                    'value': Decimal(metric['value']),
                    'instance_id': metric['instance_id'],
                    'region': metric['region'],
                    'collected_at': metric['collected_at']
                }
                batch.put_item(Item=item)
        
        print(f"Successfully wrote {len(metrics)} metrics to DynamoDB")
        
    except Exception as e:
        print(f"Error writing to DynamoDB: {str(e)}")
        raise
    
    # Publish CloudWatch metrics
    try:
        for metric in metrics:
            cloudwatch.put_metric_data(
                Namespace='InfraMonitoring',
                MetricData=[
                    {
                        'MetricName': metric['metric_type'],
                        'Value': float(metric['value']),
                        'Unit': 'Percent' if metric['metric_type'] != 'network_traffic' else 'Megabits/Second',
                        'Timestamp': datetime.now(),
                        'Dimensions': [
                            {'Name': 'Region', 'Value': REGION},
                            {'Name': 'InstanceID', 'Value': metric['instance_id']}
                        ]
                    }
                ]
            )
        
        print(f"Successfully published {len(metrics)} metrics to CloudWatch")
        
    except Exception as e:
        print(f"Error publishing to CloudWatch: {str(e)}")
        raise
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Successfully collected {len(metrics)} metrics',
            'timestamp': timestamp,
            'instance_id': instance_id,
            's3_key': s3_key
        })
    }

