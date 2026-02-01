
# phase 1 Setup - January 27, 2026

## Completed Tasks
✅ AWS account access verified
✅ IAM role created: DataPipelineLambdaRole
✅ IAM policy created: DataPipelineLambdaPolicy
✅ Local Git repository initialized
✅ Project structure created

## IAM Role Details
- **Name**: DataPipelineLambdaRole
- **ARN**: [Copy from AWS Console: IAM → Roles → DataPipelineLambdaRole]
- **Type**: AWS Service Role for Lambda
- **Console Link**: https://console.aws.amazon.com/iam/home#/roles/DataPipelineLambdaRole

## IAM Policy Details
- **Name**: DataPipelineLambdaPolicy
- **ARN**: arn:aws:iam::190517931751:role/DataPipelineLambdaRole
- **Location**: `iam-policies/DataPipelineLambdaPolicy.json`
- **Console Link**: https://console.aws.amazon.com/iam/home#/policies

## AWS CLI Alternative
Using AWS CloudShell for CLI commands instead of local installation.

### CloudShell Test Results
```bash
# Run this in CloudShell:
aws sts get-caller-identity

# Expected output:
# {
#     "UserId": "AIDAI...",
#     "Account": "123456789012",
#     "Arn": "arn:aws:iam::123456789012:user/your-username"
# }
```

## Project Structure
```
aws-data-pipeline/
├── .git/
├── iam-policies/
│   ├── DataPipelineLambdaPolicy.json
│   └── README.md
├── docs/
│   └── day1-setup.md
├── lambda/
│   ├── data-collector/
│   └── log-processor/
└── README.md
```

## Next Steps (Day 2 - January 28, 2026)
- Create S3 bucket for data storage
- Set up DynamoDB table
- Configure CloudWatch logging
- Document bucket and table ARNs

## Notes
- IAM policies follow principle of least privilege
- All resources documented for easy reference
- Using CloudShell as AWS CLI alternative
