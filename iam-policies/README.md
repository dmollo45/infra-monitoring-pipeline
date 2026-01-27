
# IAM Policies Documentation

## DataPipelineLambdaPolicy

**Purpose**: Grants Lambda functions the minimum permissions needed to operate the serverless data pipeline.

**Policy ARN**: `arn:aws:iam::YOUR_ACCOUNT_ID:policy/DataPipelineLambdaPolicy`

**Attached to Role**: `DataPipelineLambdaRole`

### Permissions Breakdown

#### S3 Access (Statement ID: S3Access)
- **Actions Allowed**:
  - `s3:GetObject` - Read files from S3 bucket
  - `s3:PutObject` - Write files to S3 bucket
  - `s3:ListBucket` - List contents of S3 bucket
  
- **Resources**: 
  - `arn:aws:s3:::your-bucket-name/*` - Objects within the bucket
  - `arn:aws:s3:::your-bucket-name` - The bucket itself

- **Why Needed**: Lambda functions need to read raw data files and write processed logs to S3 for storage and archival.

#### DynamoDB Access (Statement ID: DynamoDBAccess)
- **Actions Allowed**:
  - `dynamodb:PutItem` - Insert new records
  - `dynamodb:GetItem` - Retrieve specific records
  - `dynamodb:Query` - Query records with conditions
  - `dynamodb:Scan` - Scan entire table

- **Resources**: `arn:aws:dynamodb:*:*:table/your-table-name`

- **Why Needed**: Lambda functions store processed metrics and metadata in DynamoDB for quick retrieval and analysis.

#### CloudWatch Logs Access (Statement ID: CloudWatchLogsAccess)
- **Actions Allowed**:
  - `logs:CreateLogGroup` - Create log groups
  - `logs:CreateLogStream` - Create log streams
  - `logs:PutLogEvents` - Write log events

- **Resources**: `arn:aws:logs:*:*:*` - All CloudWatch Logs resources

- **Why Needed**: Lambda automatically sends execution logs to CloudWatch for monitoring, debugging, and troubleshooting.

### Security Notes

- **Principle of Least Privilege**: This policy grants only the minimum permissions required for the pipeline to function.
- **Resource Restrictions**: Permissions are scoped to specific resources (bucket names, table names) rather than wildcard access.
- **No Administrative Access**: No permissions to delete resources or modify IAM policies.

### Maintenance

- **Last Updated**: January 27, 2026
- **Review Schedule**: Quarterly
- **Owner**: [Your Name/Team]

### Future Enhancements

Consider adding these permissions as the project grows:
- SNS publish permissions for alerting
- SQS permissions for message queuing
- Additional DynamoDB tables as needed
