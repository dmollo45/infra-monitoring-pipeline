Deployment Guide - Infrastructure Monitoring Pipeline

This guide provides step-by-step instructions for deploying the Infrastructure Monitoring Pipeline to your AWS account.
Prerequisites
Required Tools

    AWS Account with appropriate permissions
    AWS CLI v2.x or higher
    Python 3.14+
    Git
    Bash shell (Linux/macOS) or Git Bash (Windows)

AWS Permissions Required

    IAM: Create roles and policies
    Lambda: Create and update functions
    S3: Create buckets and configure notifications
    DynamoDB: Create tables
    Step Functions: Create state machines
    EventBridge: Create rules
    SNS: Create topics and subscriptions
    CloudWatch: Create log groups and dashboards

Step 1: Clone the Repository

DEPLOYMENT-GUIDE.md - Step-by-Step Deployment

# Clone the repository
git clone https://github.com/dmollo45/aws-data-pipeline.git
cd aws-data-pipeline

# Verify repository structure
ls -la

Step 2: Configure AWS CLI

DEPLOYMENT-GUIDE.md - Step-by-Step Deployment

# Configure AWS credentials
aws configure

# Verify configuration
aws sts get-caller-identity

# Set your AWS region (recommended: eu-west-1)
export AWS_REGION=eu-west-1

Step 3: Deploy IAM Roles

DEPLOYMENT-GUIDE.md - Step-by-Step Deployment

# Navigate to IAM directory
cd iam/

# Create Lambda execution role
aws iam create-role \
  --role-name lambda-execution-role \
  --assume-role-policy-document file://lambda-trust-policy.json

# Attach permissions policy
aws iam put-role-policy \
  --role-name lambda-execution-role \
  --policy-name LambdaExecutionPolicy \
  --policy-document file://lambda-permissions-policy.json

# Create Step Functions execution role
aws iam create-role \
  --role-name step-functions-execution-role \
  --assume-role-policy-document file://stepfunctions-trust-policy.json

# Attach permissions policy
aws iam put-role-policy \
  --role-name step-functions-execution-role \
  --policy-name StepFunctionsExecutionPolicy \
  --policy-document file://stepfunctions-permissions-policy.json

# Wait for IAM roles to propagate
sleep 10

cd ..

Expected Output: Role ARNs for both Lambda and Step Functions roles
Step 4: Create S3 Bucket

DEPLOYMENT-GUIDE.md - Step-by-Step Deployment

# Create S3 bucket (replace with unique name)
export BUCKET_NAME=infra-monitoring-pipeline-data-$(date +%s)

aws s3api create-bucket \
  --bucket $BUCKET_NAME \
  --region $AWS_REGION \
  --create-bucket-configuration LocationConstraint=$AWS_REGION

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket $BUCKET_NAME \
  --versioning-configuration Status=Enabled

# Block public access
aws s3api put-public-access-block \
  --bucket $BUCKET_NAME \
  --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

# Create folder structure
aws s3api put-object --bucket $BUCKET_NAME --key raw-metrics/
aws s3api put-object --bucket $BUCKET_NAME --key processed-logs/
aws s3api put-object --bucket $BUCKET_NAME --key athena-results/

echo "S3 Bucket created: $BUCKET_NAME"

Step 5: Create DynamoDB Table

DEPLOYMENT-GUIDE.md - Step-by-Step Deployment

# Create DynamoDB table
aws dynamodb create-table \
  --table-name InfraMetrics \
  --attribute-definitions \
    AttributeName=metric_id,AttributeType=S \
    AttributeName=timestamp,AttributeType=N \
  --key-schema \
    AttributeName=metric_id,KeyType=HASH \
    AttributeName=timestamp,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --region $AWS_REGION

# Wait for table to be active
aws dynamodb wait table-exists --table-name InfraMetrics

echo "DynamoDB table created: InfraMetrics"

Step 6: Deploy Lambda Functions

DEPLOYMENT-GUIDE.md - Step-by-Step Deployment

# Deploy data-collector Lambda
cd lambda/data-collector/

# Install dependencies
pip install -r requirements.txt -t .

# Create deployment package
zip -r data-collector.zip .

# Get Lambda role ARN
LAMBDA_ROLE_ARN=$(aws iam get-role --role-name lambda-execution-role --query 'Role.Arn' --output text)

# Create Lambda function
aws lambda create-function \
  --function-name data-collector \
  --runtime python3.14 \
  --role $LAMBDA_ROLE_ARN \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://data-collector.zip \
  --timeout 30 \
  --memory-size 128 \
  --environment Variables="{BUCKET_NAME=$BUCKET_NAME,TABLE_NAME=InfraMetrics,REGION=$AWS_REGION}" \
  --region $AWS_REGION

cd ../..

# Deploy log-processor Lambda
cd lambda/log-processor/

# Install dependencies
pip install -r requirements.txt -t .

# Create deployment package
zip -r log-processor.zip .

# Create Lambda function
aws lambda create-function \
  --function-name log-processor \
  --runtime python3.14 \
  --role $LAMBDA_ROLE_ARN \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://log-processor.zip \
  --timeout 30 \
  --memory-size 128 \
  --region $AWS_REGION

cd ../..

echo "Lambda functions deployed successfully"

Step 7: Configure S3 Event Notification

DEPLOYMENT-GUIDE.md - Step-by-Step Deployment

# Add Lambda permission for S3 to invoke log-processor
aws lambda add-permission \
  --function-name log-processor \
  --statement-id s3-invoke-permission \
  --action lambda:InvokeFunction \
  --principal s3.amazonaws.com \
  --source-arn arn:aws:s3:::$BUCKET_NAME

# Create S3 event notification configuration
cat > s3-event-config.json <<EOF
{
  "LambdaFunctionConfigurations": [
    {
      "Id": "ProcessNewMetrics",
      "LambdaFunctionArn": "$(aws lambda get-function --function-name log-processor --query 'Configuration.FunctionArn' --output text)",
      "Events": ["s3:ObjectCreated:*"],
      "Filter": {
        "Key": {
          "FilterRules": [
            {"Name": "prefix", "Value": "raw-metrics/"},
            {"Name": "suffix", "Value": ".json"}
          ]
        }
      }
    }
  ]
}
EOF

# Apply S3 event notification
aws s3api put-bucket-notification-configuration \
  --bucket $BUCKET_NAME \
  --notification-configuration file://s3-event-config.json

echo "S3 event notification configured"

Step 8: Create SNS Topic

DEPLOYMENT-GUIDE.md - Step-by-Step Deployment

# Create SNS topic
SNS_TOPIC_ARN=$(aws sns create-topic \
  --name InfraMonitoring-Alarms \
  --region $AWS_REGION \
  --query 'TopicArn' \
  --output text)

# Subscribe your email (replace with your email)
aws sns subscribe \
  --topic-arn $SNS_TOPIC_ARN \
  --protocol email \
  --notification-endpoint your-email@example.com

echo "SNS topic created: $SNS_TOPIC_ARN"
echo "⚠️  Check your email and confirm the subscription!"

Step 9: Deploy Step Functions State Machine

DEPLOYMENT-GUIDE.md - Step-by-Step Deployment

# Get Step Functions role ARN
STEPFUNCTIONS_ROLE_ARN=$(aws iam get-role --role-name step-functions-execution-role --query 'Role.Arn' --output text)

# Update state machine definition with actual ARNs
cd step-functions/

# Replace placeholders in state-machine.json
sed -i "s|LAMBDA_ARN_PLACEHOLDER|$(aws lambda get-function --function-name data-collector --query 'Configuration.FunctionArn' --output text)|g" state-machine.json
sed -i "s|SNS_TOPIC_ARN_PLACEHOLDER|$SNS_TOPIC_ARN|g" state-machine.json

# Create state machine
aws stepfunctions create-state-machine \
  --name InfraMonitoring-Pipeline-Orchestration \
  --definition file://state-machine.json \
  --role-arn $STEPFUNCTIONS_ROLE_ARN \
  --region $AWS_REGION

cd ..

echo "Step Functions state machine deployed"

Step 10: Configure EventBridge Schedule

DEPLOYMENT-GUIDE.md - Step-by-Step Deployment

# Get Step Functions state machine ARN
STATE_MACHINE_ARN=$(aws stepfunctions list-state-machines \
  --query "stateMachines[?name=='InfraMonitoring-Pipeline-Orchestration'].stateMachineArn" \
  --output text)

# Create EventBridge rule
aws events put-rule \
  --name InfraMonitoring-Trigger \
  --schedule-expression "rate(3 hours)" \
  --state ENABLED \
  --region $AWS_REGION

# Add Step Functions as target
aws events put-targets \
  --rule InfraMonitoring-Trigger \
  --targets "Id"="1","Arn"="$STATE_MACHINE_ARN","RoleArn"="$STEPFUNCTIONS_ROLE_ARN"

echo "EventBridge schedule configured (every 3 hours)"

Step 11: Create Athena Database and Table

DEPLOYMENT-GUIDE.md - Step-by-Step Deployment

# Create Athena database
aws athena start-query-execution \
  --query-string "CREATE DATABASE IF NOT EXISTS infra_monitoring" \
  --result-configuration "OutputLocation=s3://$BUCKET_NAME/athena-results/" \
  --region $AWS_REGION

# Wait for query to complete
sleep 5

# Create Athena table
aws athena start-query-execution \
  --query-string "CREATE EXTERNAL TABLE IF NOT EXISTS infra_monitoring.metrics (
    metric_id STRING,
    metric_type STRING,
    timestamp BIGINT,
    value DOUBLE,
    instance_id STRING,
    region STRING,
    collected_at STRING
  )
  ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
  LOCATION 's3://$BUCKET_NAME/raw-metrics/'
  TBLPROPERTIES ('has_encrypted_data'='false')" \
  --result-configuration "OutputLocation=s3://$BUCKET_NAME/athena-results/" \
  --region $AWS_REGION

echo "Athena database and table created"

Step 12: Verify Deployment

DEPLOYMENT-GUIDE.md - Step-by-Step Deployment

# Test data-collector Lambda
aws lambda invoke \
  --function-name data-collector \
  --payload '{"metric_type": "cpu_utilization"}' \
  --region $AWS_REGION \
  response.json

cat response.json

# Check S3 for new file
aws s3 ls s3://$BUCKET_NAME/raw-metrics/ --recursive | tail -5

# Check DynamoDB for new record
aws dynamodb scan \
  --table-name InfraMetrics \
  --limit 5 \
  --region $AWS_REGION

# Start Step Functions execution
aws stepfunctions start-execution \
  --state-machine-arn $STATE_MACHINE_ARN \
  --region $AWS_REGION

echo "✅ Deployment verification complete!"

Step 13: Monitor First Execution

DEPLOYMENT-GUIDE.md - Step-by-Step Deployment

# Get latest execution ARN
EXECUTION_ARN=$(aws stepfunctions list-executions \
  --state-machine-arn $STATE_MACHINE_ARN \
  --max-results 1 \
  --query 'executions[0].executionArn' \
  --output text)

# Check execution status
aws stepfunctions describe-execution \
  --execution-arn $EXECUTION_ARN \
  --region $AWS_REGION

# View CloudWatch Logs
aws logs tail /aws/lambda/data-collector --follow

Deployment Summary

After completing all steps, you should have:

✅ IAM roles for Lambda and Step Functions ✅ S3 bucket with folder structure ✅ DynamoDB table for metrics ✅ 2 Lambda functions (data-collector, log-processor) ✅ S3 event notification configured ✅ SNS topic with email subscription ✅ Step Functions state machine ✅ EventBridge rule (every 3 hours) ✅ Athena database and table
Troubleshooting
Issue: Lambda function fails with permission error

Solution: Verify IAM role has correct permissions and wait 10 seconds for propagation
Issue: S3 event notification not triggering log-processor

Solution: Check Lambda permission for S3 invocation and verify event configuration
Issue: Step Functions execution fails

Solution: Check CloudWatch Logs for Lambda errors and verify all ARNs in state machine definition
Issue: SNS email not received

Solution: Check spam folder and confirm subscription in email
Clean Up (Optional)

To remove all resources:

DEPLOYMENT-GUIDE.md - Step-by-Step Deployment

# Delete EventBridge rule
aws events remove-targets --rule InfraMonitoring-Trigger --ids "1"
aws events delete-rule --name InfraMonitoring-Trigger

# Delete Step Functions state machine
aws stepfunctions delete-state-machine --state-machine-arn $STATE_MACHINE_ARN

# Delete Lambda functions
aws lambda delete-function --function-name data-collector
aws lambda delete-function --function-name log-processor

# Delete DynamoDB table
aws dynamodb delete-table --table-name InfraMetrics

# Delete S3 bucket (remove all objects first)
aws s3 rm s3://$BUCKET_NAME --recursive
aws s3api delete-bucket --bucket $BUCKET_NAME

# Delete SNS topic
aws sns delete-topic --topic-arn $SNS_TOPIC_ARN

# Delete IAM roles
aws iam delete-role-policy --role-name lambda-execution-role --policy-name LambdaExecutionPolicy
aws iam delete-role --role-name lambda-execution-role
aws iam delete-role-policy --role-name step-functions-execution-role --policy-name StepFunctionsExecutionPolicy
aws iam delete-role --role-name step-functions-execution-role