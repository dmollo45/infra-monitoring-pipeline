AWS Infrastructure Monitoring Data Pipeline
Project Overview

A comprehensive AWS data pipeline for collecting, processing, storing, and monitoring synthetic infrastructure metrics using Lambda, S3, DynamoDB, and CloudWatch.
Phase 7: CloudWatch Dashboard ✅ COMPLETED

Date Completed: February 10, 2026
Duration: 2 hours
Status: ✅ Completed
Objectives

    Create comprehensive CloudWatch dashboard for real-time pipeline monitoring
    Visualize infrastructure metrics (CPU, memory, disk, network)
    Monitor Lambda function performance and errors
    Track DynamoDB write capacity consumption
    Monitor S3 storage growth
    Capture professional screenshots for portfolio documentation

Deliverables

    ✅ InfraMonitoring-Dashboard created with 7 monitoring widgets
    ✅ Infrastructure metrics visualization - 4 metrics (CPU utilization, memory usage, disk usage, network traffic)
    ✅ Lambda performance monitoring - Invocations, duration, and error tracking
    ✅ DynamoDB write capacity tracking - Consumed write capacity units
    ✅ S3 storage size monitoring - Bucket size tracking
    ✅ 8 portfolio screenshots captured and organized

Dashboard Widgets Configuration

    Infrastructure Metrics - Real-time Monitoring (Line Chart)
        Metrics: cpu_utilization, memory_usage, disk_usage, network_traffic
        Namespace: InfraMonitoring
        Dimension: Region = eu-west-1
        Statistic: Average | Period: 5 minutes

    Log Processor - Processing Statistics (Line Chart)
        Metrics: FilesProcessed, MetricsProcessed, MetricsFailed
        Namespace: InfraMonitoring/LogProcessor
        Statistic: Sum | Period: 5 minutes

    Lambda Function Invocations (Line Chart)
        Metrics: data-collector Invocations, log-processor Invocations
        Namespace: AWS/Lambda
        Statistic: Sum | Period: 5 minutes

    Lambda Execution Duration (Line Chart)
        Metrics: data-collector Duration, log-processor Duration
        Namespace: AWS/Lambda
        Statistic: Average | Period: 5 minutes

    DynamoDB Write Capacity (Line Chart)
        Metric: InfraMetrics ConsumedWriteCapacityUnits
        Namespace: AWS/DynamoDB
        Statistic: Sum | Period: 5 minutes

    Lambda Error Count (Number Widget)
        Metrics: data-collector Errors, log-processor Errors
        Namespace: AWS/Lambda
        Statistic: Sum | Period: 1 hour

    S3 Storage Size (Number Widget)
        Metric: infra-monitoring-pipeline-data BucketSizeBytes
        Namespace: AWS/S3
        Statistic: Average | Period: 1 day

Key Achievements
Technical Fixes

    Fixed CloudWatch metrics publishing bug - Corrected array indexing in data-collector Lambda (metrics[0]['value'] instead of metrics['value'])
    Resolved region-specific metric issues - Added explicit region_name='eu-west-1' to all boto3 clients
    Implemented error handling and logging - Added try-except blocks with print statements for debugging CloudWatch publishing
    Added metric dimensions - Included Region: eu-west-1 dimension to all custom metrics

Dashboard Features

    Centralized monitoring - Single pane of glass for all pipeline metrics
    Real-time visibility - 5-minute refresh intervals for near real-time monitoring
    Performance tracking - Lambda duration and invocation metrics identify bottlenecks
    Error detection - Dedicated error count widget for quick health checks
    Resource planning - S3 storage and DynamoDB capacity metrics aid in cost forecasting

Technical Highlights

CloudWatch Metrics Publishing:

# Initialize clients with explicit region
cloudwatch = boto3.client('cloudwatch', region_name='eu-west-1')

# Publish metrics with dimensions
cloudwatch.put_metric_data(
    Namespace='InfraMonitoring',
    MetricData=[
        {
            'MetricName': 'cpu_utilization',
            'Value': float(metrics[0]['value']),  # Fixed array indexing
            'Unit': 'Percent',
            'Timestamp': datetime.utcnow(),
            'Dimensions': [
                {'Name': 'Region', 'Value': 'eu-west-1'}
            ]
        },
        # ... other 3 metrics
    ]
)

Key Learnings:

    CloudWatch metrics take 2-3 minutes to appear after publishing
    Explicit region specification prevents cross-region metric issues
    Error handling with logging is essential for debugging metric publishing
    Custom dimensions enable better metric filtering and organization

Documentation

    Phase 7 Documentation: docs/phase7-cloudwatch-dashboard.md
    Screenshots Directory: screenshots/phase7-cloudwatch/
    Widget Configurations: Detailed in phase documentation

Screenshots

InfraMonitoring-Dashboard showing all 7 widgets with real-time metrics visualization
File Structure

aws-data-pipeline/
├── screenshots/
│   └── phase7-cloudwatch/
│       ├── cloudwatch-dashboard-full.png
│       ├── widget-infrastructure-metrics.png
│       ├── widget-processing-statistics.png
│       ├── widget-lambda-invocations.png
│       ├── widget-lambda-duration.png
│       ├── widget-dynamodb-writes.png
│       ├── widget-lambda-errors.png
│       └── widget-s3-storage.png
├── docs/
│   └── phase7-cloudwatch-dashboard.md
└── README.md

Current Progress

Completed Phases: 7/10 (70%)

    ✅ Phase 1: IAM Setup (January 28, 2026)
    ✅ Phase 2: S3 & DynamoDB Setup (January 29, 2026)
    ✅ Phase 3: Lambda Development - data-collector (January 29, 2026)
    ✅ Phase 4: Lambda Deployment & EventBridge Automation (January 30, 2026)
    ✅ Phase 5: Data Processing Development - log-processor (February 4, 2026)
    ✅ Phase 6: Deploy Log Processor & S3 Integration (February 5, 2026)
    ✅ Phase 7: CloudWatch Dashboard Creation (February 10, 2026)
    🔄 Phase 8: CloudWatch Alarms (Next - February 11, 2026)
    ⏳ Phase 9: Step Functions Workflow
    ⏳ Phase 10: Final Testing & Documentation

Target Completion: February 14, 2026
Project Statistics (as of Phase 7)
AWS Resources

    Lambda Functions: 2 (data-collector, log-processor)
    CloudWatch Metrics: 7 custom metrics
    Dashboard Widgets: 7 widgets
    S3 Buckets: 1 (infra-monitoring-pipeline-data)
    DynamoDB Tables: 1 (InfraMetrics with GSI)
    EventBridge Rules: 1 (5-minute schedule)
    IAM Policies: 2 (Lambda execution policies)

Documentation

    Phase Documents: 7 markdown files
    Screenshots: 8+ portfolio screenshots
    Code Files: 2 Lambda functions (Python 3.14)
    Total Lines of Code: ~300 lines

Metrics Generated

    Data Collection Frequency: Every 5 minutes
    Metrics per Collection: 4 infrastructure metrics
    Daily Metric Data Points: ~1,152 data points
    S3 Files Generated: ~288 JSON files per day

Next Phase Preview: Phase 8 - CloudWatch Alarms

Planned Date: February 11, 2026
Estimated Duration: 1-2 hours
Objectives

    Create SNS topic for alarm notifications
    Configure 5 CloudWatch alarms for automated alerting
    Test alarm triggers and notifications
    Document alarm configurations

Alarms to Create

    High CPU Utilization - Threshold: > 80%
    Lambda Errors - Threshold: > 0 errors
    DynamoDB Throttling - Threshold: > 0 throttles
    High Memory Usage - Threshold: > 90%
    Lambda Duration - Threshold: > 3000ms

Technologies Used

    AWS Lambda - Serverless compute (Python 3.14)
    Amazon S3 - Object storage for raw metrics
    Amazon DynamoDB - NoSQL database with GSI
    Amazon CloudWatch - Monitoring and dashboards
    Amazon EventBridge - Scheduled Lambda triggers
    AWS IAM - Identity and access management
    Python - Lambda function development
    boto3 - AWS SDK for Python

Repository Structure

aws-data-pipeline/
├── README.md                          # This file
├── docs/
│   ├── phase1-iam-setup.md
│   ├── phase2-s3-dynamodb-setup.md
│   ├── phase3-data-collector.md
│   ├── phase4-lambda-deployment.md
│   ├── phase5-log-processor-development.md
│   ├── phase6-log-processor-deployment.md
│   └── phase7-cloudwatch-dashboard.md
├── screenshots/
│   ├── phase1-iam/
│   ├── phase2-s3-dynamodb/
│   ├── phase3-lambda-dev/
│   ├── phase4-deployment/
│   ├── phase5-log-processor/
│   ├── phase6-s3-trigger/
│   └── phase7-cloudwatch/
└── lambda/
    ├── data-collector/
    │   └── lambda_function.py
    └── log-processor/
        └── lambda_function.py

Contact & Portfolio

Project Author: David Mollo
Project Type: AWS Infrastructure Monitoring Pipeline 
Completion Status: 70% (7/10 phases completed)
Last Updated: February 10, 2026
License

This project is for educational and portfolio purposes.