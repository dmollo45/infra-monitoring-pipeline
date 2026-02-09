
# log-processor Lambda Function

## Overview
Event-driven Lambda function that processes infrastructure metrics from S3 and writes them to DynamoDB for real-time querying.

## Architecture
- **Trigger**: S3 ObjectCreated events
- **Input**: JSON files from `infra-monitoring-pipeline-data` bucket
- **Output**: Metrics written to `InfraMetrics` DynamoDB table
- **Monitoring**: Custom CloudWatch metrics published

## Features
- ✅ Automatic S3 event processing
- ✅ Batch writes to DynamoDB (up to 25 items)
- ✅ Exponential backoff retry logic
- ✅ Data validation and error handling
- ✅ CloudWatch metrics publishing
- ✅ Dead Letter Queue support (optional)
- ✅ TTL-based automatic cleanup (30 days)

## Environment Variables
- `DYNAMODB_TABLE`: Target DynamoDB table (default: InfraMetrics)
- `AWS_REGION`: AWS region (default: us-east-1)
- `DLQ_URL`: SQS Dead Letter Queue URL (optional)

## Error Handling
1. **S3 Read Failures**: Retried automatically by S3 event notifications (up to 24 hours)
2. **JSON Parsing Errors**: Logged and skipped (non-blocking)
3. **DynamoDB Throttling**: Exponential backoff retry (3 attempts)
4. **Batch Write Failures**: Failed items sent to DLQ if configured

## Testing Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run unit tests
python test_log_processor.py

# Test with sample event
python -c "
import json
import lambda_function
with open('sample_s3_event.json') as f:
    event = json.load(f)
# Note: Requires AWS credentials and actual S3 file
"
```

## Deployment
See Day 6 deployment guide for AWS deployment steps.

## Monitoring
Custom CloudWatch metrics published:
- `MetricsProcessed`: Total metrics processed
- `SuccessfulWrites`: Successful DynamoDB writes
- `FailedWrites`: Failed DynamoDB writes
- `FilesProcessed`: S3 files processed

## Cost
- Lambda: Free tier (1M requests/month)
- DynamoDB: Free tier (25 GB storage)
- CloudWatch: Free tier (10 custom metrics)
- **Estimated**: $0.00/month (within free tier)
