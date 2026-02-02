
# Phase 4: Lambda Deployment & EventBridge Automation

**Date Completed:** February 2, 2026  
**Status:** ✅ Complete  
**Cost:** $0.00 (within AWS Free Tier)

## Overview

Phase 4 deployed the data-collector Lambda function to AWS and configured EventBridge for automated scheduling with enable/disable control for cost optimization.

## What Was Built

### 1. Lambda Function Deployment
- **Function Name:** `data-collector`
- **Runtime:** Python 3.11
- **Memory:** 128 MB
- **Timeout:** 1 minute
- **Handler:** `data_collector.lambda_handler`
- **IAM Role:** `DataPipelineLambdaRole` (from Phase 1)

### 2. Environment Variables
```
S3_BUCKET=infra-monitoring-pipeline-data
DYNAMODB_TABLE=InfraMetrics
REGION=eu-west-1
```

### 3. EventBridge Automation
- **Rule Name:** `data-collector-schedule`
- **Schedule:** `rate(5 minutes)`
- **Target:** Lambda function `data-collector`
- **Default State:** Disabled (cost optimization)
- **Usage:** Enable during study sessions only

## Deployment Steps Completed

### Lambda Deployment
1. ✅ Created deployment package (ZIP file)
2. ✅ Uploaded code to AWS Lambda
3. ✅ Configured environment variables
4. ✅ Set IAM role permissions
5. ✅ Adjusted timeout and memory settings
6. ✅ Tested manual invocation successfully

### EventBridge Configuration
1. ✅ Created schedule-based rule
2. ✅ Configured 5-minute rate expression
3. ✅ Set Lambda as target
4. ✅ Disabled rule by default for cost control
5. ✅ Tested enable/disable workflow

## Testing Results

### Manual Testing
- **Test Executions:** 11 successful invocations
- **Average Duration:** 344 ms
- **Memory Usage:** 97 MB (76% of allocated 128 MB)
- **Error Rate:** 0% (after fixing initial configuration issues)
- **Success Rate:** 100%

### Automated Testing (20-minute session)
- **Automated Executions:** 4 invocations (every 5 minutes)
- **S3 Files Created:** 4 JSON files with metrics
- **DynamoDB Entries:** 4 items with correct schema
- **CloudWatch Logs:** All executions logged successfully

## Issues Resolved

### Issue 1: Handler Configuration
**Problem:** `No module named 'lambda_function'`  
**Solution:** Updated handler from `lambda_function.lambda_handler` to `data_collector.lambda_handler`

### Issue 2: S3 Access Denied
**Problem:** Lambda couldn't write to S3 bucket in eu-west-1  
**Solution:** Updated IAM policy to be region-agnostic and changed Lambda environment variable `REGION` to `eu-west-1`

### Issue 3: DynamoDB Type Mismatch
**Problem:** `timestamp` field type mismatch (String vs Number)  
**Solution:** 
- Updated Lambda code to use Unix timestamp (integer)
- Recreated DynamoDB GSI with correct Number type for timestamp
- Added `timestamp_iso` field for human-readable format

## Cost Optimization Strategy

### Implemented Controls
1. **S3 Lifecycle Policy:** 7-day automatic deletion
2. **EventBridge Disabled by Default:** Zero cost when not studying
3. **Manual Enable/Disable:** Full control over invocations
4. **Minimal Memory Allocation:** 128 MB (lowest cost tier)
5. **AWS Budget Alert:** $1.50 monthly threshold

### Cost Breakdown
- **EventBridge Schedule:** $0.00 (free for schedule-based rules)
- **Lambda Invocations:** $0.00 (within 1M requests/month Free Tier)
- **Lambda Compute:** $0.00 (within 400K GB-seconds/month Free Tier)
- **S3 Storage:** $0.00 (minimal KB with 7-day retention)
- **S3 PUT Requests:** $0.00 (within 2,000 requests/month Free Tier)
- **DynamoDB Writes:** $0.00 (within 25 GB storage Free Tier)
- **CloudWatch Logs:** $0.00 (within 5 GB ingestion Free Tier)

**Total Phase 4 Cost:** $0.00 ✅

## Monitoring & Observability

### CloudWatch Logs
- **Log Group:** `/aws/lambda/data-collector`
- **Retention:** Default (never expire)
- **Contents:** Execution logs, error traces, performance metrics

### CloudWatch Metrics
- **Lambda Metrics:** Invocations, duration, errors, throttles, concurrency
- **S3 Metrics:** Storage size, request counts, data transfer
- **DynamoDB Metrics:** Read/write capacity, item count, table size
- **EventBridge Metrics:** Invocations, triggered rules, failed invocations

### Performance Metrics
- **Cold Start Duration:** 1,143 ms (first invocation)
- **Warm Start Duration:** 300-500 ms (subsequent invocations)
- **Average Execution Time:** 344 ms
- **Memory Efficiency:** 76% utilization (97 MB / 128 MB)

## Data Pipeline Flow

```
EventBridge (5-minute schedule)
    ↓
Lambda: data-collector
    ↓
    ├─→ S3: metrics-YYYY-MM-DD-HH-MM-SS.json
    └─→ DynamoDB: InfraMetrics table
         ↓
    CloudWatch Logs: Execution logs
```

## Usage Instructions

### Enable Automation (Study Session Start)
```
1. Go to EventBridge Console
2. Navigate to Rules → data-collector-schedule
3. Click toggle switch to enable (turns green)
4. Lambda runs automatically every 5 minutes
```

### Disable Automation (Study Session End)
```
1. Go to EventBridge Console
2. Navigate to Rules → data-collector-schedule
3. Click toggle switch to disable (turns gray)
4. Lambda stops running automatically
```

### Manual Testing
```
1. Go to Lambda Console
2. Select data-collector function
3. Click Test tab
4. Click Test button
5. Verify success (statusCode 200)
```

## Key Learnings

### Technical Skills
- Deploying serverless Lambda functions to AWS
- Configuring EventBridge for automated scheduling
- Cross-region AWS service integration
- DynamoDB data type handling and GSI management
- IAM policy configuration for multi-service access
- CloudWatch monitoring and log analysis

### Best Practices
- Enable/disable automation for cost control
- Use environment variables for configuration
- Implement proper error handling and logging
- Test thoroughly before enabling automation
- Monitor costs with AWS Budgets and billing alerts
- Use lifecycle policies for automatic data cleanup

### Troubleshooting Skills
- Debugging Lambda handler configuration issues
- Resolving cross-region permission problems
- Fixing DynamoDB schema type mismatches
- Reading and interpreting CloudWatch logs
- Using AWS Console for real-time monitoring

## Next Steps

**Phase 5 (Day 5):** Develop log-processor Lambda
- Create data transformation logic
- Implement aggregation functions
- Add error handling and validation
- Write unit tests

**Phase 6 (Day 6):** Deploy log-processor with S3 trigger
- Configure S3 event notifications
- Deploy Lambda function
- Test automated processing
- Verify data transformation

## Resources

### AWS Services Used
- AWS Lambda
- Amazon EventBridge
- Amazon S3
- Amazon DynamoDB
- Amazon CloudWatch

### Documentation
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Amazon EventBridge Documentation](https://docs.aws.amazon.com/eventbridge/)
- [CloudWatch Logs Documentation](https://docs.aws.amazon.com/cloudwatch/)

### Project Files
- Lambda Code: `lambda/data-collector/data_collector.py`
- IAM Policy: `iam-policies/DataPipelineLambdaPolicy.json`
- Phase 1 Docs: `docs/day1-setup.md`
- Phase 2 Docs: `docs/phase2-storage.md`
- Phase 3 Docs: `docs/phase3-lambda-development.md`

---

**Phase 4 Status:** ✅ Complete  
**Total Project Cost to Date:** $0.00  
**Next Phase:** Phase 5 - Log Processor Development
