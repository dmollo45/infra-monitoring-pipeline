
# AWS Serverless Data Pipeline

Infrastructure monitoring and log analytics pipeline built with AWS Lambda, S3, and DynamoDB.

## Project Overview
This project implements a serverless data pipeline for collecting, processing, and analyzing infrastructure logs and metrics using AWS services.

## Project Timeline
- **Start Date**: January 27, 2026
- **End Date**: February 14, 2026
- **Duration**: 15 days

## Current Status
**Day 1 - IAM Setup** ✅ (January 27, 2026)

## Technologies
- **AWS Lambda** - Serverless compute for data processing
- **Amazon S3** - Object storage for raw and processed data
- **DynamoDB** - NoSQL database for metrics storage
- **CloudWatch** - Monitoring and logging
- **EventBridge** - Event scheduling
- **Python** - Lambda function runtime

## Architecture
```
EventBridge → Lambda (data-collector) → S3 (raw data)
                                          ↓
                                    Lambda (log-processor)
                                          ↓
                                      DynamoDB
                                          ↓
                                   CloudWatch Dashboard
```

## Project Structure
```
aws-data-pipeline/
├── iam-policies/          # IAM policy definitions
├── docs/                  # Project documentation
├── lambda/
│   ├── data-collector/    # Data collection Lambda
│   └── log-processor/     # Log processing Lambda
└── README.md
```

## Documentation
- [Day 1 Setup - IAM Configuration](docs/day1-setup.md)
- [IAM Policies Documentation](iam-policies/README.md)

## Daily Progress
- ✅ **Day 1** (Jan 27): AWS account setup & IAM configuration
- ⏳ **Day 2** (Jan 28): S3 bucket & DynamoDB table creation
- ⏳ **Day 3** (Jan 29): Lambda function development (data-collector)
- ⏳ **Day 4** (Jan 30): Deploy data-collector & EventBridge setup
- ⏳ **Day 5** (Jan 31): Lambda function development (log-processor)
- ⏳ **Day 6** (Feb 3): Deploy log-processor & S3 event notifications
- ⏳ **Day 7** (Feb 4): CloudWatch dashboard creation
- ⏳ **Day 8** (Feb 5): CloudWatch alarms setup
- ⏳ **Day 9** (Feb 6): Integration testing
- ⏳ **Day 10** (Feb 7): Cost optimization
- ⏳ **Day 11** (Feb 10): Architecture documentation
- ⏳ **Day 12** (Feb 11): Code documentation
- ⏳ **Day 13** (Feb 12): Troubleshooting guide
- ⏳ **Day 14** (Feb 13): Portfolio preparation
- ⏳ **Day 15** (Feb 14): Final review & retrospective

## Medium Articles
- Week 1 (Feb 2): Days 1-5 overview
- Week 2 (Feb 9): Days 6-10 overview
- Week 3 (Feb 16): Days 11-15 overview

## Success Criteria
- ✅ IAM role and policies configured
- ⏳ S3 bucket with lifecycle policies
- ⏳ DynamoDB table with proper schema
- ⏳ Two Lambda functions deployed
- ⏳ CloudWatch dashboard operational
- ⏳ Monthly cost under $0.50
- ⏳ Complete documentation

## Author
[David Mollo]

## License
MIT License
