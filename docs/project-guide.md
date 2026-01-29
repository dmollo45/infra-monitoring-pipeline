AWS INFRASTRUCTURE ANALYTICS PIPELINE
COMPLETE IMPLEMENTATION GUIDE (UNDER $2/MONTH)

================================================================================
PROJECT OVERVIEW
================================================================================

Build an end-to-end data pipeline for infrastructure monitoring and log 
analytics using AWS "Always Free" services + minimal S3 storage costs.

Target Role: L4 Data Engineer at Amazon
Relevant Departments: AWS Infrastructure Operations, OpsTech, Data Center Engineering
Monthly Cost: $0.50 - $2.00
Timeline: 6-8 weeks
Skill Level: Beginner to Intermediate

================================================================================
TABLE OF CONTENTS
================================================================================
Project Architecture
Prerequisites & Setup
Cost Breakdown
Phase 1: AWS Account Setup (Day 1)
Phase 2: Data Generation Pipeline (Days 2-3)
Phase 3: Data Processing & Storage (Days 4-5)
Phase 4: Monitoring & Alerting (Days 6-7)
Phase 5: Analytics & Visualization (Days 8-10)
Phase 6: Infrastructure as Code (Days 11-12)
Testing & Validation
Portfolio Presentation
Interview Preparation

================================================================================
PROJECT ARCHITECTURE
================================================================================

HIGH-LEVEL ARCHITECTURE DIAGRAM

┌─────────────────────────────────────────────────────────────┐
│                    DATA GENERATION LAYER                     │
│  Lambda Function (Synthetic Log Generator) - Always FREE    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                     STORAGE LAYER                            │
│  S3 Data Lake (Partitioned by date) - ~$0.50/month         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   PROCESSING LAYER                           │
│  Lambda Functions (ETL Processing) - Always FREE            │
│  AWS Glue Data Catalog - Always FREE                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    ANALYTICS LAYER                           │
│  Amazon Athena (SQL Queries) - ~$0.01/month                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 MONITORING & ALERTING                        │
│  CloudWatch Dashboards - Always FREE                        │
│  CloudWatch Alarms - Always FREE (10 alarms)               │
│  SNS Email Notifications - Always FREE (1K emails/month)   │
└─────────────────────────────────────────────────────────────┘

DATA FLOW EXPLANATION
Generation: Lambda function generates synthetic infrastructure logs every 5 minutes
Storage: Logs stored in S3 with date partitioning (year/month/day/hour)
Cataloging: Glue Crawler automatically discovers schema and creates tables
Processing: Lambda functions aggregate and transform data
Querying: Athena enables SQL queries on S3 data
Visualization: CloudWatch dashboards display key metrics
Alerting: CloudWatch alarms trigger SNS notifications for anomalies

================================================================================
PREREQUISITES & SETUP
================================================================================

REQUIRED SOFTWARE (ALL FREE)

AWS Account:
• Existing AWS account (free tier expired, but using Always Free services)
• Valid payment method (for minimal S3 charges)

Local Development Environment:

Python 3.9+
• Windows: Download from python.org
• Mac: brew install python3
• Linux: sudo apt-get install python3 python3-pip

AWS CLI Installation:
Windows (PowerShell as Administrator):
  msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

Mac:
  brew install awscli

Linux:
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  sudo ./aws/install

Verify installation:
  aws --version

Terraform Installation:
Windows (Chocolatey):
  choco install terraform

Mac:
  brew install terraform

Linux:
  wget https://releases.hashicorp.com/terraform/1.6.0/terraform1.6.0linux_amd64.zip
  unzip terraform1.6.0linux_amd64.zip
  sudo mv terraform /usr/local/bin/

Verify installation:
  terraform --version

Git:
• Download from: git-scm.com

Visual Studio Code:
• Download from: code.visualstudio.com
• Install extensions: Python, AWS Toolkit, Terraform, YAML

Python Libraries:
  pip install boto3 pandas numpy faker

AWS Account Configuration:

Create IAM User for Development:
Go to AWS Console → IAM → Users → Create User
User Details:
• Username: data-pipeline-dev
• Access type: Programmatic access
Attach Policies:
• AmazonS3FullAccess
• AWSLambda_FullAccess
• CloudWatchFullAccess
• AWSGlueConsoleFullAccess
• AmazonSNSFullAccess
• AmazonAthenaFullAccess
• IAMReadOnlyAccess
Save credentials: Access Key ID and Secret Access Key

Configure AWS CLI:
  aws configure
  AWS Access Key ID: [your-access-key]
  AWS Secret Access Key: [your-secret-key]
  Default region name: us-east-1
  Default output format: json

Verify configuration:
  aws sts get-caller-identity

================================================================================
COST BREAKDOWN
================================================================================

MONTHLY COST ESTIMATE

Service          | Free Tier              | Your Usage           | Cost/Month
-----------------|------------------------|----------------------|-----------
Lambda           | 1M requests, 400K GB-s | ~50K requests        | $0.00
S3 Storage       | None (expired)         | 20 GB                | $0.46
S3 Requests      | None (expired)         | 10K PUT, 50K GET     | $0.05
Glue Data Catalog| 1M objects             | 1K objects           | $0.00
Athena           | None                   | 1 GB scanned         | $0.005
CloudWatch       | 10 metrics, 10 alarms  | 5 metrics, 5 alarms  | $0.00
SNS              | 1K emails              | 100 emails           | $0.00
Data Transfer    | 1 GB out               | 0.5 GB               | $0.00
TOTAL                                                            | $0.51

COST OPTIMIZATION STRATEGIES

S3 Lifecycle Policies:
• Delete logs older than 30 days
• Reduces storage from 20GB to ~5GB
• Savings: $0.35/month

Athena Query Optimization:
• Use partitioning (already implemented)
• Limit SELECT columns
• Use LIMIT clauses
• Savings: Minimal queries = $0.005/month

Lambda Optimization:
• Reduce memory allocation (128MB sufficient)
• Optimize execution time
• Already FREE (within Always Free limits)

Optimized Monthly Cost: $0.15 - $0.50

================================================================================
PHASE 1: AWS ACCOUNT SETUP (DAY 1)
================================================================================

STEP 1: CREATE S3 BUCKET FOR DATA LAKE

Using AWS Console:
Go to S3 Console: https://s3.console.aws.amazon.com/
Click "Create bucket"
Bucket name: infrastructure-logs-[your-initials]-[random-number]
   Example: infrastructure-logs-jd-12345 (must be globally unique)
Region: us-east-1 (N. Virginia)
Block Public Access: Keep all boxes checked (security best practice)
Bucket Versioning: Disabled (to save costs)
Encryption: Server-side encryption with Amazon S3 managed keys (SSE-S3)
Click "Create bucket"

Using AWS CLI:
  aws s3 mb s3://infrastructure-logs-jd-12345 --region us-east-1

STEP 2: CREATE S3 LIFECYCLE POLICY

Purpose: Automatically delete logs older than 30 days to minimize costs

Using AWS Console:
Go to your bucket → Management tab
Click "Create lifecycle rule"
Rule name: delete-old-logs
Rule scope: Apply to all objects
Lifecycle rule actions: Check "Expire current versions of objects"
Days after object creation: 30
Click "Create rule"

STEP 3: CREATE SNS TOPIC FOR ALERTS

Using AWS Console:
Go to SNS Console: https://console.aws.amazon.com/sns/
Click "Topics" → "Create topic"
Type: Standard
Name: infrastructure-alerts
Click "Create topic"
Click "Create subscription"
Protocol: Email
Endpoint: your-email@example.com
Click "Create subscription"
Check your email and confirm subscription

Using AWS CLI:
  aws sns create-topic --name infrastructure-alerts
  aws sns subscribe --topic-arn arn:aws:sns:us-east-1:123456789012:infrastructure-alerts --protocol email --notification-endpoint your-email@example.com

STEP 4: CREATE IAM ROLE FOR LAMBDA

Using AWS Console:
Go to IAM Console → Roles → Create role
Trusted entity: AWS service → Lambda
Permissions policies: Attach these policies:
• AWSLambdaBasicExecutionRole
• AmazonS3FullAccess (or create custom policy with limited S3 access)
• CloudWatchFullAccess
• AmazonSNSFullAccess
Role name: lambda-data-pipeline-role
Click "Create role"

================================================================================
PHASE 2: DATA GENERATION PIPELINE (DAYS 2-3)
================================================================================

Overview: Create a Lambda function that generates realistic infrastructure 
logs every 5 minutes. This simulates data from servers, applications, and 
network devices.

See separate documentation for Lambda function code and deployment steps.

================================================================================
PHASE 3: DATA PROCESSING & STORAGE (DAYS 4-5)
================================================================================

STEP 1: CREATE GLUE DATABASE

Using AWS Console:
Go to Glue Console → Databases → Add database
Database name: infrastructurelogsdb
Click "Create"

Using AWS CLI:
  aws glue create-database --database-input '{"Name":"infrastructurelogsdb"}'

STEP 2: CREATE GLUE CRAWLER

Using AWS Console:
Go to Glue Console → Crawlers → Add crawler
Crawler name: infrastructure-logs-crawler
Data source: S3 → s3://your-bucket-name/logs/
IAM role: Create new role → AWSGlueServiceRole-logs
Schedule: On demand (run manually)
Database: infrastructurelogsdb
Table prefix: raw_
Click "Create"

STEP 3: RUN CRAWLER

Using AWS Console:
Go to Glue Console → Crawlers
Select infrastructure-logs-crawler
Click "Run crawler"
Wait 2-3 minutes for completion

STEP 4: VERIFY TABLE CREATION

Using AWS Console:
Go to Glue Console → Tables
You should see: raw_logs
Click on table to view schema

================================================================================
PHASE 4: MONITORING & ALERTING (DAYS 6-7)
================================================================================

STEP 1: CREATE CLOUDWATCH DASHBOARD

Using AWS Console:
Go to CloudWatch Console → Dashboards → Create dashboard
Dashboard name: Infrastructure-Monitoring
Add widgets for:
• Log Volume (Line Chart)
• Error Rate (Number)
• Lambda Invocations (Line Chart)

STEP 2: CREATE CLOUDWATCH ALARMS

Alarm 1: High Error Rate
• Metric: Custom metric
• Threshold: > 10 errors in 5 minutes
• Action: Send notification to SNS topic infrastructure-alerts

Alarm 2: Lambda Failures
• Metric: AWS/Lambda Errors
• Threshold: > 5 errors in 5 minutes
• Action: Send notification to SNS topic

================================================================================
PHASE 5: ANALYTICS & VISUALIZATION (DAYS 8-10)
================================================================================

STEP 1: QUERY DATA WITH ATHENA

Setup Athena:
Go to Athena Console
Settings → Query result location: s3://your-bucket-name/athena-results/
Click "Save"

Sample Queries:

Query 1: Total Log Count
  SELECT COUNT() as totallogs FROM raw_logs;

Query 2: Logs by Severity
  SELECT severity, COUNT(*) as count 
  FROM raw_logs 
  GROUP BY severity 
  ORDER BY count DESC;

Query 3: Top Error Messages
  SELECT message, COUNT(*) as count 
  FROM raw_logs 
  WHERE severity = 'ERROR' 
  GROUP BY message 
  ORDER BY count DESC 
  LIMIT 10;

Query 4: Hourly Log Volume Trend
  SELECT DATETRUNC('hour', timestamp) as hour, COUNT() as count 
  FROM raw_logs 
  GROUP BY DATE_TRUNC('hour', timestamp) 
  ORDER BY hour;

================================================================================
PHASE 6: INFRASTRUCTURE AS CODE (DAYS 11-12)
================================================================================

Create Terraform configuration files to automate infrastructure deployment.

See separate terraform/ folder for:
• main.tf (Main configuration)
• variables.tf (Variable definitions)
• outputs.tf (Output definitions)
• terraform.tfvars (Variable values)

Deploy with Terraform:
  terraform init
  terraform plan
  terraform apply

================================================================================
PROJECT TIMELINE
================================================================================

Start Date: January 27, 2026
End Date: February 14, 2026
Study Schedule: 2-3 hours/day, 6 days/week

Weekly Milestones:
• Week 1: Phases 1-2 (Setup + Data Generation)
• Week 2: Phases 3-4 (Processing + Monitoring)
• Week 3: Phases 5-6 (Analytics + IaC)

================================================================================
ADDITIONAL RESOURCES
================================================================================
• AWS Documentation: https://docs.aws.amazon.com/
• Terraform AWS Provider: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
• Project GitHub Repository: https://github.com/dmollo45/aws-data-pipeline

Last Updated: January 29, 2026
Author: David Mollo