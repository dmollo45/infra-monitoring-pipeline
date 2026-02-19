Infrastructure Monitoring Pipeline

    A production-ready serverless infrastructure monitoring pipeline built on AWS that collects, processes, stores, and analyzes system metrics with automated alerting capabilities.

Project Status: ✅ Complete | Duration: 24 days | Cost: ~$0.02/month
🎯 Project Overview

This project demonstrates advanced cloud architecture skills by implementing a fully serverless data pipeline on AWS. The system collects infrastructure metrics, processes them in parallel, stores data in multiple formats, and provides real-time alerting and historical analysis capabilities.
Key Features

    ✅ Parallel Processing - 3.3x performance improvement using Step Functions
    ✅ 100% Serverless - No servers to manage or maintain
    ✅ Cost Optimized - Stays within AWS Free Tier (~$0.02/month)
    ✅ Production Ready - Comprehensive error handling and monitoring
    ✅ Fully Automated - EventBridge scheduling with 3-hour intervals
    ✅ Scalable Design - Can handle 10x data volume without architecture changes

🏗️ Architecture

EventBridge (Every 3 Hours)
    ↓
Step Functions State Machine
    ↓
ParallelDataCollection (4 branches)
    ├─→ CPU Metrics
    ├─→ Memory Metrics
    ├─→ Disk Metrics
    └─→ Network Metrics
    ↓
S3 + DynamoDB + CloudWatch
    ↓
Athena Analytics + SNS Alerts

View Detailed Architecture Diagram →
🛠️ Technologies Used
README.md - Professional Portfolio README
Compute
	
AWS Lambda (Python 3.14)
Storage
	
Amazon S3, DynamoDB
Orchestration
	
AWS Step Functions, EventBridge
Monitoring
	
CloudWatch Logs, Metrics, Dashboards
Alerting
	
Amazon SNS
Analytics
	
Amazon Athena
Security
	
IAM Roles & Policies
📊 Performance Metrics
README.md - Professional Portfolio README
Parallel Execution Time
	
917ms (3.3x faster than sequential)
Total Pipeline Duration
	
6.3 seconds
Monthly Executions
	
240 (8 per day)
Success Rate
	
100% (50+ test executions)
Monthly Cost
	
$0.02 (99% under budget)
🚀 Quick Start
Prerequisites

    AWS Account with appropriate permissions
    AWS CLI configured
    Python 3.14+
    Git

Installation

README.md - Professional Portfolio README

# Clone the repository
git clone https://github.com/dmollo45/aws-data-pipeline.git
cd aws-data-pipeline

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure

Deployment

README.md - Professional Portfolio README

# Deploy IAM roles
./scripts/deploy-iam.sh

# Deploy Lambda functions
./scripts/deploy-lambda.sh

# Deploy Step Functions state machine
./scripts/deploy-stepfunctions.sh

# Configure EventBridge schedule
./scripts/deploy-eventbridge.sh

View Detailed Deployment Guide →
📁 Project Structure

aws-data-pipeline/
├── docs/                           # Comprehensive documentation
│   ├── phase1-iam-setup.md
│   ├── phase2-storage-setup.md
│   ├── phase3-lambda-collector.md
│   ├── phase4-event-processing.md
│   ├── phase5-cloudwatch.md
│   ├── phase6-sns-alerts.md
│   ├── phase7-athena-queries.md
│   ├── phase8-eventbridge.md
│   ├── phase9-testing.md
│   ├── phase10-step-functions.md
│   ├── architecture.md
│   ├── cost-analysis.md
│   └── deployment-guide.md
├── lambda/                         # Lambda function code
│   ├── data-collector/
│   │   ├── lambda_function.py
│   │   └── requirements.txt
│   └── log-processor/
│       ├── lambda_function.py
│       └── requirements.txt
├── step-functions/                 # Step Functions definitions
│   └── state-machine.json
├── iam/                           # IAM policies and roles
│   ├── lambda-execution-role.json
│   └── stepfunctions-execution-role.json
├── scripts/                       # Deployment scripts
│   ├── deploy-iam.sh
│   ├── deploy-lambda.sh
│   ├── deploy-stepfunctions.sh
│   └── deploy-eventbridge.sh
├── screenshots/                   # Project screenshots
│   ├── phase1-iam/
│   ├── phase2-storage/
│   ├── phase3-lambda/
│   ├── phase4-events/
│   ├── phase5-cloudwatch/
│   ├── phase6-sns/
│   ├── phase7-athena/
│   ├── phase8-eventbridge/
│   ├── phase9-testing/
│   └── phase10-step-functions/
├── tests/                         # Test files
│   ├── test_data_collector.py
│   └── test_log_processor.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt

📖 Documentation
Phase-by-Phase Implementation

    Phase 1: IAM Setup - IAM roles and security configuration
    Phase 2: Storage Setup - S3 and DynamoDB configuration
    Phase 3: Lambda Collector - Data collection Lambda function
    Phase 4: Event Processing - S3 events and log processor
    Phase 5: CloudWatch - Monitoring and metrics
    Phase 6: SNS Alerts - Email notification system
    Phase 7: Athena Queries - SQL analytics setup
    Phase 8: EventBridge - Automated scheduling
    Phase 9: Testing - Comprehensive testing and optimization
    Phase 10: Step Functions - Workflow orchestration with parallel processing

Additional Documentation

    Architecture Overview - Detailed system architecture
    Cost Analysis - Complete cost breakdown and optimization
    Deployment Guide - Step-by-step deployment instructions
    Troubleshooting Guide - Common issues and solutions

💡 Key Technical Highlights
1. Parallel Processing Architecture

Implemented Step Functions Parallel state with 4 simultaneous branches for metric collection:

    Performance: 3.3x faster than sequential execution (917ms vs 3,000ms)
    Scalability: Scales linearly with additional metric types
    Fault Tolerance: Individual branch failures don't break entire pipeline

View Implementation Details →
2. Cost Optimization

Achieved 99% cost reduction through strategic optimizations:

    EventBridge Scheduling: Changed from 5-minute to 3-hour intervals
    S3 Lifecycle Policies: Automatic transition to IA storage after 30 days
    DynamoDB On-Demand: Pay only for actual usage
    Lambda Memory Optimization: 128MB sufficient for workload

View Cost Analysis →
3. Error Handling & Retry Logic

Comprehensive error handling with exponential backoff:

    Retry Configuration: 3 attempts with 10s, 20s, 40s intervals
    Graceful Degradation: Partial data collection on individual failures
    SNS Notifications: Immediate alerts on pipeline failures

View Error Handling Strategy →
📈 Performance Results
Execution Performance
README.md - Professional Portfolio README
Data Collection
	
3,000ms
	
917ms
	
3.3x faster
Total Execution
	
~8 seconds
	
~6.3 seconds
	
21% faster
Throughput
	
1 metric/750ms
	
4 metrics/917ms
	
4.4x better
Cost Comparison
README.md - Professional Portfolio README
Original Plan
	
(5-min intervals)
	
$2.00
Optimized Plan
	
(3-hour intervals)
	
$0.02
🧪 Testing

Comprehensive testing performed across all components:

    ✅ Unit Testing - Lambda functions with different inputs
    ✅ Integration Testing - End-to-end pipeline execution
    ✅ Performance Testing - Parallel vs sequential comparison
    ✅ Error Handling - Retry logic and failure scenarios
    ✅ Load Testing - 50+ successful executions

View Testing Documentation →
💰 Cost Breakdown
README.md - Professional Portfolio README
Step Functions
	
2,880 transitions
	
4,000/month
	
$0.00
Lambda
	
960 invocations
	
1M/month
	
$0.00
S3
	
960 files (~20MB)
	
5GB/month
	
$0.01
DynamoDB
	
960 writes
	
25GB storage
	
$0.00
CloudWatch
	
Logs + Metrics
	
Always Free
	
$0.00
SNS
	
240 emails
	
1,000/month
	
$0.00
EventBridge
	
240 triggers
	
Always Free
	
$0.00
Athena
	
Minimal queries
	
1TB/month
	
$0.01
Total
	
	
	
$0.02/month

View Detailed Cost Analysis →
🎓 Skills Demonstrated

This project showcases proficiency in:
Cloud Architecture

    ✅ Serverless architecture design
    ✅ Event-driven systems
    ✅ Parallel processing patterns
    ✅ Multi-tier storage strategies

AWS Services

    ✅ Lambda (Python 3.14)
    ✅ Step Functions (workflow orchestration)
    ✅ S3 (data lake)
    ✅ DynamoDB (NoSQL database)
    ✅ CloudWatch (monitoring)
    ✅ SNS (notifications)
    ✅ Athena (SQL analytics)
    ✅ EventBridge (scheduling)

DevOps & SRE

    ✅ Infrastructure as Code
    ✅ CI/CD principles
    ✅ Monitoring and alerting
    ✅ Error handling and retry logic
    ✅ Cost optimization
    ✅ Performance tuning

Data Engineering

    ✅ Data pipeline design
    ✅ ETL processes
    ✅ Data lake architecture
    ✅ SQL analytics
    ✅ Real-time processing

🔮 Future Enhancements
Short-Term (1-3 months)

    Real infrastructure monitoring (EC2/RDS)
    Machine learning for anomaly detection
    QuickSight dashboards for business users

Long-Term (3-6 months)

    Multi-region support
    Auto-remediation capabilities
    Advanced cost optimization with Intelligent-Tiering

View Roadmap →
📸 Screenshots
Step Functions Visual Workflow

CloudWatch Dashboard

Parallel Execution Logs

View All Screenshots →
🤝 Contributing

Contributions are welcome! Please read the Contributing Guidelines before submitting pull requests.
📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
👤 Author

Your Name

    GitHub: @dmollo45
    LinkedIn: https://www.linkedin.com/in/david-m-499254145/
    Email: dmollo45@gmail.com.com

🙏 Acknowledgments

    AWS Documentation for comprehensive service guides
    AWS Free Tier for enabling cost-effective learning
    Open-source community for Python libraries

📊 Project Statistics

    Total Lines of Code: ~500 (Python)
    AWS Services Used: 8
    IAM Roles Created: 2
    Lambda Functions: 2
    Step Functions States: 15
    Documentation Pages: 11
    Test Executions: 50+
    Success Rate: 100%
    Project Duration: 24 days
    Final Cost: $0.02/month
