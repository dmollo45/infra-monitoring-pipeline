import json
import boto3
import random
import time
from datetime import datetime

# Initialize AWS clients
s3_client = boto3.client('s3')

# Configuration
S3_BUCKET = 'infra-monitoring-pipeline-data'
METRIC_TYPES = ['cpu', 'memory', 'disk', 'network']
HOST_IDS = ['host-001', 'host-002', 'host-003', 'host-004', 'host-005']
REGION = 'eu-west-1'

def generate_metric(metric_type, host_id, timestamp):
    """Generate a single synthetic metric based on type."""
    if metric_type == 'cpu':
        value = round(random.uniform(10.0, 95.0), 2)
    elif metric_type == 'memory':
        value = round(random.uniform(20.0, 90.0), 2)
    elif metric_type == 'disk':
        value = round(random.uniform(30.0, 85.0), 2)
    elif metric_type == 'network':
        value = round(random.uniform(100.0, 10000.0), 2)
    else:
        value = 0.0

    metric_id = f"{metric_type}-{timestamp}-{host_id}"
    ttl = timestamp + (30 * 24 * 60 * 60)

    return {
        'metric_id': metric_id,
        'timestamp': timestamp,
        'metric_type': metric_type,
        'value': value,
        'host_id': host_id,
        'region': REGION,
        'ttl': ttl
    }

def generate_metrics_batch():
    """Generate a batch of metrics for all hosts and metric types."""
    timestamp = int(time.time())
    metrics = []

    for host_id in HOST_IDS:
        for metric_type in METRIC_TYPES:
            metric = generate_metric(metric_type, host_id, timestamp)
            metrics.append(metric)

    return metrics

def upload_to_s3(metrics, timestamp):
    """Upload metrics to S3 as JSON file."""
    date_str = datetime.fromtimestamp(timestamp).strftime('%Y/%m/%d')
    filename = f"metrics/{date_str}/metrics-{timestamp}.json"
    json_data = json.dumps(metrics, indent=2)

    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=filename,
        Body=json_data,
        ContentType='application/json'
    )

    return filename

def lambda_handler(event, context):
    """Main Lambda handler function."""
    try:
        print("Generating metrics batch...")
        metrics = generate_metrics_batch()
        print(f"Generated {len(metrics)} metrics")

        timestamp = int(time.time())
        s3_key = upload_to_s3(metrics, timestamp)
        print(f"Uploaded metrics to S3: {s3_key}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Metrics generated and uploaded successfully',
                's3_key': s3_key,
                'metrics_count': len(metrics),
                'timestamp': timestamp
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error generating metrics',
                'error': str(e)
            })
        }

# For local testing
if __name__ == "__main__":
    print("=" * 60)
    print("LOCAL TESTING MODE - S3 upload disabled")
    print("=" * 60)
    print("")

    print("Generating metrics batch...")
    metrics = generate_metrics_batch()
    print(f"Generated {len(metrics)} metrics")
    print("")

    print("Sample metrics (first 3):")
    for i, metric in enumerate(metrics[:3]):
        print("")
        print(f"{i+1}. Metric ID: {metric['metric_id']}")
        print(f"   Type: {metric['metric_type']}")
        print(f"   Value: {metric['value']}")
        print(f"   Host: {metric['host_id']}")
        print(f"   Timestamp: {metric['timestamp']}")

    print("")
    print("=" * 60)
    print(f"SUCCESS: Generated {len(metrics)} metrics")
    print("- 5 hosts x 4 metric types = 20 total metrics")
    print("- Metric types: cpu, memory, disk, network")
    print("- Ready for AWS deployment!")
    print("=" * 60)
