
import json
import boto3
import random
from datetime import datetime
from decimal import Decimal

# Initialize AWS clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Environment variables (will be set in Lambda configuration)
S3_BUCKET = 'infra-monitoring-pipeline-data'
DYNAMODB_TABLE = 'InfraMetrics'

def generate_metrics():
    """Generate synthetic infrastructure metrics"""
    timestamp = datetime.utcnow().isoformat()
    
    metrics = {
        'metric_id': f"metric-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
        'timestamp': timestamp,
        'metric_type': random.choice(['cpu', 'memory', 'disk', 'network']),
        'value': round(random.uniform(10.0, 95.0), 2),
        'server_id': f"server-{random.randint(1, 10):03d}",
        'region': random.choice(['us-east-1', 'us-west-2', 'eu-west-1']),
        'status': random.choice(['healthy', 'warning', 'critical'])
    }
    
    return metrics

def save_to_s3(metrics):
    """Save metrics to S3 bucket"""
    try:
        timestamp = datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')
        file_name = f"metrics-{timestamp}.json"
        
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=file_name,
            Body=json.dumps(metrics, indent=2),
            ContentType='application/json'
        )
        
        return file_name
    except Exception as e:
        raise Exception(f"Error saving to S3: {str(e)}")

def save_to_dynamodb(metrics):
    """Save metrics to DynamoDB table"""
    try:
        table = dynamodb.Table(DYNAMODB_TABLE)
        
        # Convert float values to Decimal for DynamoDB
        metrics_decimal = json.loads(
            json.dumps(metrics), 
            parse_float=Decimal
        )
        
        table.put_item(Item=metrics_decimal)
        
        return metrics['metric_id']
    except Exception as e:
        raise Exception(f"Error saving to DynamoDB: {str(e)}")

def lambda_handler(event, context):
    """Main Lambda handler function"""
    try:
        # Generate metrics
        metrics = generate_metrics()
        
        # Save to S3
        s3_file = save_to_s3(metrics)
        
        # Save to DynamoDB
        dynamodb_id = save_to_dynamodb(metrics)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Metrics collected successfully',
                's3_file': s3_file,
                'dynamodb_id': dynamodb_id,
                'metrics': metrics
            })
        }
        
    except Exception as e:
        print(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error collecting metrics',
                'error': str(e)
            })
        }

