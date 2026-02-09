Phase 5: Log Processor Lambda Development
Date: February 9, 2026 (Day 5)
Focus: Data Processing Development

Overview
Development of the log-processor Lambda function that acts as a data transformation and loading service in the pipeline.

Tasks Completed
- Wrote log-processor Lambda function code (250+ lines)
- Implemented S3 event parsing logic
- Added DynamoDB batch write operations (25 items per batch)
- Created CloudWatch custom metrics publishing
- Implemented error handling with retry logic
- Fixed IAM permissions (added DynamoDB and CloudWatch access)
- Configured for Ireland (eu-west-1) region

Lambda Function Configuration
- Function Name: log-processor
- Runtime: Python 3.12
- Memory: 256 MB
- Timeout: 2 min 0 sec
- Execution Role: DataPipelineLambdaRole
- Region: eu-west-1 (Ireland)

Environment Variables
DYNAMODB_TABLE: InfraMetrics
REGION: eu-west-1

IAM Permissions Required
- AmazonS3ReadOnlyAccess (AWS managed)
- AmazonDynamoDBFullAccess (AWS managed)
- CloudWatchFullAccess (AWS managed)
- DataPipelineLambdaPolicy (Customer managed)

Code Features
1. S3 Event Processing: Parses S3 ObjectCreated events
2. JSON Validation: Validates metric data structure with required fields
3. Batch Operations: Writes up to 25 items per DynamoDB batch
4. Retry Logic: Exponential backoff for throttling (max 3 retries)
5. TTL Support: 30-day automatic data cleanup
6. CloudWatch Metrics: Custom metrics for monitoring (MetricsProcessed, MetricsFailed, FilesProcessed)
7. Error Handling: Comprehensive exception handling for S3, DynamoDB, and JSON parsing errors

Testing
- Local testing with sample S3 events
- Unit tests written (test_processor.py) with 5 test cases
- Error handling validated
- Automated S3 trigger tested successfully

Test Results
- Manual test event: Failed (file path mismatch)
- Automated S3 upload trigger: SUCCESS
  - File processed: metrics/2026/02/09/auto-trigger-test.json
  - 5 metrics written to DynamoDB
  - Processing time: 404ms
  - Success rate: 100%

Success Criteria
- Processor successfully parses JSON and writes to DynamoDB
- Automated S3 trigger works flawlessly
- CloudWatch metrics published correctly
- Zero throttled requests

Issues Resolved
1. IAM Permission Errors:
   - Added AmazonDynamoDBFullAccess policy
   - Added CloudWatchFullAccess policy

2. Region Configuration:
   - Updated all AWS clients to use eu-west-1 explicitly
   - Fixed environment variable default from us-east-1 to eu-west-1

3. S3 File Access:
   - Automated S3 trigger works correctly
   - Manual test event had folder structure mismatch