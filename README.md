
# AWS Infrastructure Monitoring Pipeline

> Production-ready serverless infrastructure monitoring solution with parallel processing, automated alerting, and SQL analytics

[![Status](https://img.shields.io/badge/Status-Complete-success)]() [![AWS](https://img.shields.io/badge/AWS-Serverless-orange)]() [![Python](https://img.shields.io/badge/Python-3.14-blue)]() [![Cost](https://img.shields.io/badge/Cost-$0.02%2Fmonth-green)]()

**Duration:** 24 days | **Cost:** $0.02/month | **Success Rate:** 100%

---

## Overview

Fully serverless AWS monitoring pipeline that collects infrastructure metrics every 3 hours, processes them in parallel using Step Functions, and provides real-time alerting with historical analysis capabilities.

**Key Achievements:**
- 3.3x performance improvement through parallel processing
- 99% cost reduction ($2.00 → $0.02/month)
- 100% success rate across 50+ executions
- Zero server management required


---

## Architecture

High-Level Architecture Flow

# Infrastructure Monitoring Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    EventBridge Scheduler                         │
│                  (Every 3 Hours - 240/month)                     │
└────────────────────────────┬────────────────────────────────────┘
                             │ triggers
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              Step Functions State Machine                        │
│              (Workflow Orchestration)                            │
└────────────────────────────┬────────────────────────────────────┘
                             │ initiates
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Parallel Data Collection                        │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐  │
│  │ CPU Metrics  │ Memory       │ Disk Metrics │ Network      │  │
│  │ Collection   │ Metrics      │ Collection   │ Metrics      │  │
│  │              │ Collection   │              │ Collection   │  │
│  └──────────────┴──────────────┴──────────────┴──────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ all branches converge
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Storage Layer (3 Paths)                       │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Path 1: S3 (Cold Path - Long-term Storage)             │    │
│  │         └──→ Athena (SQL Queries)                       │    │
│  │              Cost: ~$0.50/month (20GB)                  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Path 2: DynamoDB (Hot Path - Real-time Access)         │    │
│  │         Batch writes (25 items/request)                 │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Path 3: CloudWatch (Monitoring Metrics)                │    │
│  │         └──→ CloudWatch Alarms (6 configured)          │    │
│  │              └──→ SNS (Email Alerts)                    │    │
│  └─────────────────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────────────┘
```

---

## Detailed Component Flow

### 1. SCHEDULING → ORCHESTRATION

```
EventBridge Scheduler
│
└──→ Triggers every 3 hours (240 executions/month)
     │
     ▼
Step Functions State Machine
│
└──→ Orchestrates parallel Lambda executions
```

---

### 2. DATA COLLECTION (PARALLEL)

```
Step Functions
│
├──→ Lambda: CPU Metrics ──────┐
│                               │
├──→ Lambda: Memory Metrics ────┤──→ All execute simultaneously
│                               │
├──→ Lambda: Disk Metrics ──────┤
│                               │
└──→ Lambda: Network Metrics ───┘
     │
     └──→ Results converge after completion
```

---

### 3. STORAGE LAYER (TRIPLE PATH)

```
Collected Metrics
│
├──→ Path 1: S3 Bucket
│    │
│    ├──→ Raw metric files stored
│    ├──→ Cost: ~$0.50/month (20GB)
│    └──→ Purpose: Historical data & batch analytics
│         │
│         └──→ Athena
│              └──→ SQL queries on historical data
│                   Cost: ~$0.01/month
│
├──→ Path 2: DynamoDB Table
│    │
│    ├──→ Processed metrics stored
│    ├──→ Batch writes (25 items/request)
│    └──→ Purpose: Real-time queries & fast access
│
└──→ Path 3: CloudWatch Metrics
     │
     ├──→ Lambda execution metrics
     ├──→ Custom infrastructure metrics
     └──→ Purpose: Operational monitoring
```

---

### 4. ANALYTICS & ALERTING LAYER

```
S3 Data
│
└──→ Athena
     └──→ SQL queries on historical data
          └──→ Cost: ~$0.01/month

CloudWatch Metrics
│
└──→ CloudWatch Alarms (6 alarms configured)
     │
     ├──→ High CPU (>80%)
     ├──→ Data Collector Errors (>0)
     ├──→ Log Processor Errors (>0)
     ├──→ DynamoDB Throttling (>0)
     ├──→ High Memory (>90%)
     └──→ Lambda Duration (>3000ms)
          │
          └──→ SNS Topic
               └──→ Email notifications sent
```
    │
│  └─────────────────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────────────┘


KEY METRICS

    Execution Frequency: Every 3 hours (240/month)
    Parallel Branches: 4 simultaneous metric collections
    Storage Paths: 3 (cold/hot/monitoring)
    Analytics Services: 3 (query/alarm/notify)
    Performance Improvement: 3.3x with parallel processing

```

**Data Flow:**
1. EventBridge triggers Step Functions every 3 hours
2. 4 Lambda functions collect metrics in parallel (917ms)
3. Data stored in S3 (cold path) and DynamoDB (hot path)
4. CloudWatch monitors execution, SNS sends alerts
5. Athena enables SQL queries on historical data

---

## Technologies

| Category | Technologies |
|----------|-------------|
| **Compute** | Lambda (Python 3.14), Step Functions, EventBridge |
| **Storage** | S3 (lifecycle policies), DynamoDB (on-demand, TTL) |
| **Monitoring** | CloudWatch (metrics, logs, alarms), SNS, Athena |
| **Security** | IAM (least-privilege roles) |

---

## Performance Metrics

| Metric | Sequential | Parallel | Improvement |
|--------|-----------|----------|-------------|
| Collection Time | 3,000ms | 917ms | **3.3x faster** |
| Total Duration | ~8s | ~6.3s | **21% faster** |
| Throughput | 1/750ms | 4/917ms | **4.4x better** |
| Success Rate | 100% | 100% | Maintained |

---

## Quick Start

Prerequisites

    AWS Account with appropriate permissions
    AWS CLI v2.x configured with credentials
    Python 3.14 or higher
    Git for version control

```bash
# Clone repository
git clone https://github.com/dmollo45/aws-data-pipeline.git
cd aws-data-pipeline

# Install dependencies
pip install -r requirements.txt

# Deploy (requires AWS CLI configured)
./scripts/deploy-iam.sh
./scripts/deploy-lambda.sh
./scripts/deploy-stepfunctions.sh
./scripts/deploy-eventbridge.sh

# Test execution
aws stepfunctions start-execution \
  --state-machine-arn arn:aws:states:REGION:ACCOUNT:stateMachine:InfraMonitoringPipeline


## Project Structure

aws-data-pipeline/
├── docs/                              # Comprehensive documentation
│   ├── phase1-iam-setup.md           # IAM roles and policies
│   ├── phase2-storage-setup.md       # S3 and DynamoDB configuration
│   ├── phase3-lambda-collector.md    # Data collector implementation
│   ├── phase4-event-processing.md    # Event-driven processing
│   ├── phase5-cloudwatch.md          # Monitoring setup
│   ├── phase6-sns-alerts.md          # Alerting configuration
│   ├── phase7-athena-queries.md      # SQL analytics
│   ├── phase8-eventbridge.md         # Scheduling automation
│   ├── phase9-testing.md             # Testing strategy
│   ├── phase10-step-functions.md     # Parallel orchestration
│   ├── architecture.md               # System architecture
│   ├── cost-analysis.md              # Cost breakdown
│   └── deployment-guide.md           # Deployment instructions
│
├── lambda/                            # Lambda function code
│   ├── data-collector/
│   │   ├── lambda_function.py        # Metric collection logic
│   │   └── requirements.txt          # Python dependencies
│   └── log-processor/
│       ├── lambda_function.py        # Event processing logic
│       └── requirements.txt          # Python dependencies
│
├── step-functions/                    # Step Functions definitions
│   └── state-machine.json            # Parallel workflow definition
│
├── iam/                              # IAM policies and roles
│   ├── lambda-execution-role.json    # Lambda IAM role
│   └── stepfunctions-execution-role.json  # Step Functions IAM role
│
├── scripts/                          # Deployment automation
│   ├── deploy-iam.sh                 # IAM deployment
│   ├── deploy-lambda.sh              # Lambda deployment
│   ├── deploy-stepfunctions.sh       # Step Functions deployment
│   └── deploy-eventbridge.sh         # EventBridge configuration
│
├── screenshots/                      # Project screenshots
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
│
├── tests/                            # Test files
│   ├── test_data_collector.py        # Unit tests for collector
│   └── test_log_processor.py         # Unit tests for processor
│
├── .gitignore                        # Git ignore rules
├── LICENSE                           # MIT License
├── README.md                         # This file
└── requirements.txt                  # Python dependencies


```

---

## Technical Highlights

### 1. Parallel Processing
Step Functions parallel state with 4 branches achieving 3.3x performance improvement over sequential execution.
Challenge: Sequential metric collection was taking 3+ seconds, creating bottlenecks.

Solution: Implemented Step Functions Parallel state with 4 simultaneous branches:

{
  "Type": "Parallel",
  "Branches": [
    {"StartAt": "CollectCPU", ...},
    {"StartAt": "CollectMemory", ...},
    {"StartAt": "CollectDisk", ...},
    {"StartAt": "CollectNetwork", ...}
  ]
}

Results:

    Performance: 3.3x faster execution (917ms vs 3,000ms)
    Scalability: Linear scaling with additional metric types
    Fault Tolerance: Individual branch failures don't break entire pipeline
    Cost Efficiency: Same Lambda invocations, better throughput

### 2. Cost Optimization
- EventBridge: 5-min → 3-hour intervals (97.5% reduction)
- S3 Lifecycle: Auto-transition to IA after 30 days
- DynamoDB: On-demand pricing for low-volume workloads
- Lambda: Optimized to 128MB memory
Challenge: Initial design projected $2.00/month, exceeding free tier budget.

Solution: Multi-faceted optimization approach:

EventBridge Scheduling:

    Changed from 5-minute to 3-hour intervals
    Reduced executions from 8,640 to 240 per month
    Savings: $1.95/month (97.5% reduction)

S3 Lifecycle Policies:

    Automatic transition to Infrequent Access after 30 days
    Reduced storage costs by 50% for historical data
    Savings: $0.02/month

DynamoDB On-Demand:

    Pay-per-request pricing instead of provisioned capacity
    Zero cost for low-volume workloads
    Savings: $0.01/month

Lambda Memory Optimization:

    Tested 128MB, 256MB, 512MB configurations
    128MB sufficient for workload (no performance impact)
    Savings: Minimal but optimized for cost

Final Cost: $0.02/month (99% under original projection)

### 3. Error Handling
Exponential backoff retry logic (3 attempts: 10s, 20s, 40s) with SNS notifications and CloudWatch integration.
Challenge: Transient failures in distributed systems require robust error handling.

Solution: Comprehensive retry strategy with exponential backoff:

{
  "Retry": [
    {
      "ErrorEquals": ["States.TaskFailed", "Lambda.ServiceException"],
      "IntervalSeconds": 10,
      "MaxAttempts": 3,
      "BackoffRate": 2.0
    }
  ],
  "Catch": [
    {
      "ErrorEquals": ["States.ALL"],
      "Next": "NotifyFailure"
    }
  ]
}

Features:

    Retry Configuration: 3 attempts with 10s, 20s, 40s intervals
    Graceful Degradation: Partial data collection on individual failures
    SNS Notifications: Immediate alerts on pipeline failures
    CloudWatch Integration: Detailed error logs for debugging

Results:

    Zero production failures across 50+ executions
    Average recovery time: <30 seconds for transient errors
    100% visibility into failure scenarios

### 4. Multi-Tier Storage
- **Hot Path (DynamoDB):** Real-time queries (<10ms), 7-day TTL
- **Cold Path (S3):** Historical analysis, Athena SQL queries
Challenge: Balance between query performance and storage costs.

Solution: Lambda Architecture pattern with hot and cold paths:

Hot Path (DynamoDB):

    Real-time queries (<10ms latency)
    Last 7 days of data
    TTL-based automatic cleanup
    GSI for metric_type queries

Cold Path (S3):

    Historical analysis (30+ days)
    Cost-effective long-term storage
    Athena SQL queries
    Lifecycle policies for IA transition

Benefits:

    Performance: Fast queries for recent data
    Cost: 90% cheaper storage for historical data
    Flexibility: SQL analytics on cold data
    Scalability: Unlimited S3 storage capacity

---

## Cost Analysis

| Service | Usage | Free Tier | Cost |
|---------|-------|-----------|------|
| Step Functions | 2,880 transitions | 4,000/month | $0.00 |
| Lambda | 960 invocations | 1M/month | $0.00 |
| S3 | ~20MB | 5GB/month | $0.01 |
| DynamoDB | 960 writes | 25GB storage | $0.00 |
| CloudWatch | Logs + Metrics | Always Free | $0.00 |
| SNS | 240 emails | 1,000/month | $0.00 |
| Athena | Minimal queries | 1TB/month | $0.01 |
| **Total** | | | **$0.02/month** |

## Test Results

Unit Tests:
✅ test_data_collector.py - 12 tests passed
✅ test_log_processor.py - 8 tests passed

Integration Tests:
✅ End-to-end pipeline execution - 50+ runs
✅ Parallel processing validation - 20+ runs
✅ Error handling scenarios - 15+ runs
✅ Cost validation - Continuous monitoring

Performance Tests:
✅ Sequential execution: 3,000ms average
✅ Parallel execution: 917ms average
✅ Improvement: 3.3x faster



## Skills Demonstrated

**Cloud Architecture:** Serverless design, event-driven systems, parallel processing, multi-tier storage

**AWS Services:** Lambda, Step Functions, S3, DynamoDB, CloudWatch, SNS, Athena, EventBridge, IAM

**DevOps:** IaC principles, monitoring, error handling, cost optimization, performance tuning

**Data Engineering:** Pipeline design, ETL processes, data lake architecture, SQL analytics

**Software Engineering:** Python (500+ LOC), unit testing, error handling, documentation


## Documentation

- [Architecture Overview](docs/architecture.md)
- [Deployment Guide](docs/DEPLOYMENT-GUIDE.md)
- [Cost Analysis](docs/cost-analysis.md)
- [Testing Strategy](docs/phase9-testing.md)
- [Phase-by-Phase Implementation](docs/)

---

## Future Enhancements

**Short-Term:** Real EC2/RDS monitoring, ML anomaly detection, QuickSight dashboards

**Long-Term:** Multi-region support, auto-remediation, API development

---

## Author

**David Mollo**
- GitHub: [@dmollo45](https://github.com/dmollo45)
- LinkedIn: [David Mollo.](https://www.linkedin.com/in/david-m-499254145/)
- Email: dmollo45@gmail.com

SRE Data Engineer specializing in AWS cloud architecture, serverless computing, and scalable data pipelines.

---

## License

MIT License - See [LICENSE](LICENSE) for details

---

**Project Stats:** 500+ LOC | 8 AWS Services | 15 Step Functions States | 50+ Test Executions | 100% Success Rate

⭐ Star this repo if you find it helpful!
