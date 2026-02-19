
# Infrastructure Monitoring Pipeline - Architecture Diagrams

## 1. High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AWS Cloud (eu-west-1)                            │
│                                                                           │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                    Orchestration Layer                              │ │
│  │                                                                      │ │
│  │  ┌──────────────────┐         ┌──────────────────┐                │ │
│  │  │   EventBridge    │────────▶│ Step Functions   │                │ │
│  │  │                  │         │  State Machine   │                │ │
│  │  │ rate(3 hours)    │         │                  │                │ │
│  │  │ 8 exec/day       │         │ InfraMonitoring- │                │ │
│  │  │ 240 exec/month   │         │ Pipeline-Orch    │                │ │
│  │  └──────────────────┘         └────────┬─────────┘                │ │
│  └─────────────────────────────────────────┼──────────────────────────┘ │
│                                             │                            │
│  ┌─────────────────────────────────────────┼──────────────────────────┐ │
│  │                    Compute Layer         │                          │ │
│  │                                          │                          │ │
│  │              ┌───────────────────────────┼──────────────┐          │ │
│  │              │   Parallel Execution (4 branches)        │          │ │
│  │              │                                           │          │ │
│  │  ┌───────────▼──────────┐  ┌───────────────────────┐  │          │ │
│  │  │ Lambda: data-collector│  │ Lambda: log-processor │  │          │ │
│  │  │                       │  │                       │  │          │ │
│  │  │ Runtime: Python 3.14  │  │ Runtime: Python 3.14  │  │          │ │
│  │  │ Memory: 128MB         │  │ Memory: 128MB         │  │          │ │
│  │  │ Timeout: 30s          │  │ Timeout: 30s          │  │          │ │
│  │  │                       │  │                       │  │          │ │
│  │  │ Invocations: 960/mo   │  │ Trigger: S3 Event     │  │          │ │
│  │  └───────┬───────────────┘  └───────▲───────────────┘  │          │ │
│  │          │                           │                   │          │ │
│  └──────────┼───────────────────────────┼───────────────────┘          │
│             │                           │                               │
│  ┌──────────┼───────────────────────────┼───────────────────────────┐ │
│  │          │      Storage Layer        │                           │ │
│  │          │                           │                           │ │
│  │  ┌───────▼──────────┐    ┌──────────┴──────────┐               │ │
│  │  │   Amazon S3      │    │     DynamoDB        │               │ │
│  │  │                  │    │                     │               │ │
│  │  │ Bucket: infra-   │    │ Table: InfraMetrics │               │ │
│  │  │ monitoring-      │    │                     │               │ │
│  │  │ pipeline-data    │    │ Partition Key:      │               │ │
│  │  │                  │    │   metric_id         │               │ │
│  │  │ Structure:       │    │ Sort Key:           │               │ │
│  │  │ raw-metrics/     │    │   timestamp         │               │ │
│  │  │   YYYY/MM/DD/    │    │                     │               │ │
│  │  │                  │    │ Billing: On-Demand  │               │ │
│  │  │ Files: 960/month │    │ Records: 960/month  │               │ │
│  │  │ Size: ~20MB      │    │                     │               │ │
│  │  │                  │    │                     │               │ │
│  │  │ Lifecycle:       │    │                     │               │ │
│  │  │ - IA after 30d   │    │                     │               │ │
│  │  │ - Delete after   │    │                     │               │ │
│  │  │   90d            │    │                     │               │ │
│  │  └───────┬──────────┘    └─────────────────────┘               │ │
│  └──────────┼───────────────────────────────────────────────────────┘ │
│             │                                                           │
│  ┌──────────┼───────────────────────────────────────────────────────┐ │
│  │          │      Analytics & Monitoring Layer                     │ │
│  │          │                                                        │ │
│  │  ┌───────▼──────────┐    ┌──────────────────┐                  │ │
│  │  │   Amazon Athena  │    │   CloudWatch     │                  │ │
│  │  │                  │    │                  │                  │ │
│  │  │ Database:        │    │ Namespace:       │                  │ │
│  │  │ infra_monitoring │    │ InfraMonitoring  │                  │ │
│  │  │                  │    │                  │                  │ │
│  │  │ Table: metrics   │    │ Metrics:         │                  │ │
│  │  │                  │    │ - cpu_utilization│                  │ │
│  │  │ Queries: SQL     │    │ - memory_usage   │                  │ │
│  │  │ Cost: ~$0.01/mo  │    │ - disk_usage     │                  │ │
│  │  │                  │    │ - network_traffic│                  │ │
│  │  │                  │    │                  │                  │ │
│  │  │                  │    │ Dashboards: 1    │                  │ │
│  │  │                  │    │ Log Groups: 2    │                  │ │
│  │  └──────────────────┘    └──────────────────┘                  │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                           │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                    Notification Layer                              │ │
│  │                                                                     │ │
│  │  ┌──────────────────────────────────────────────────────────────┐ │ │
│  │  │                      Amazon SNS                               │ │ │
│  │  │                                                               │ │ │
│  │  │  Topic: InfraMonitoring-Alarms                               │ │ │
│  │  │                                                               │ │ │
│  │  │  Subscriptions:                                              │ │ │
│  │  │  - Email: your-email@example.com                            │ │ │
│  │  │                                                               │ │ │
│  │  │  Notifications:                                              │ │ │
│  │  │  - Pipeline Success (every 3 hours)                         │ │ │
│  │  │  - Pipeline Failure (on error)                              │ │ │
│  │  │                                                               │ │ │
│  │  │  Volume: 240 emails/month                                    │ │ │
│  │  │  Cost: FREE (within 1,000/month limit)                      │ │ │
│  │  └──────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Data Flow Diagram
AWS Infrastructure Monitoring Pipeline - Data Flow DiagramSystem Overview┌─────────────────────────────────────────────────────────────────────────────┐
│                    AWS INFRASTRUCTURE MONITORING PIPELINE                    │
│                         Serverless Data Pipeline (2026)                      │
└─────────────────────────────────────────────────────────────────────────────┘Complete Data Flow Architecture┌──────────────────────────────────────────────────────────────────────────────┐
│ TRIGGER LAYER                                                                 │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────▼────────────────┐
                    │   Amazon EventBridge Rule      │
                    │   Schedule: Every 3 Hours      │
                    │   (240 executions/month)       │
                    └───────────────┬────────────────┘
                                    │
┌──────────────────────────────────▼────────────────────────────────────────────┐
│ ORCHESTRATION LAYER                                                            │
└────────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────▼────────────────┐
                    │  AWS Step Functions            │
                    │  State Machine                 │
                    │  (Workflow Orchestration)      │
                    └───────────────┬────────────────┘
                                    │
                    ┌───────────────▼────────────────┐
                    │  Parallel State Execution      │
                    │  (4 Concurrent Branches)       │
                    │  Duration: 917ms               │
                    └───────────────┬────────────────┘
                                    │
        ┌───────────────┬───────────┴───────────┬───────────────┐
        │               │                       │               │
┌──────────────────────────────────────────────────────────────────────────────┐
│ DATA COLLECTION LAYER (Parallel Processing)                                  │
└──────────────────────────────────────────────────────────────────────────────┘
        │               │                       │               │
   ┌────▼────┐    ┌────▼────┐           ┌─────▼─────┐   ┌─────▼─────┐
   │ Lambda  │    │ Lambda  │           │  Lambda   │   │  Lambda   │
   │ Branch  │    │ Branch  │           │  Branch   │   │  Branch   │
   │   #1    │    │   #2    │           │    #3     │   │    #4     │
   └────┬────┘    └────┬────┘           └─────┬─────┘   └─────┬─────┘
        │               │                      │               │
   ┌────▼────┐    ┌────▼────┐           ┌─────▼─────┐   ┌─────▼─────┐
   │   CPU   │    │ Memory  │           │   Disk    │   │  Network  │
   │ Metrics │    │ Metrics │           │  Metrics  │   │  Metrics  │
   └────┬────┘    └────┬────┘           └─────┬─────┘   └─────┬─────┘
        │               │                      │               │
        └───────────────┴──────────┬───────────┴───────────────┘
                                   │
┌──────────────────────────────────▼────────────────────────────────────────────┐
│ STORAGE LAYER (Multi-Tier Architecture)                                       │
└────────────────────────────────────────────────────────────────────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
            ┌───────▼────────┐          ┌────────▼────────┐
            │  SPEED LAYER   │          │  BATCH LAYER    │
            │  (Hot Path)    │          │  (Cold Path)    │
            └───────┬────────┘          └────────┬────────┘
                    │                            │
        ┌───────────▼───────────┐    ┌──────────▼──────────┐
        │   Amazon DynamoDB     │    │    Amazon S3        │
        │   Table: InfraMetrics │    │    Bucket: infra-   │
        │   • Partition Key:    │    │    monitoring-      │
        │     metric_id         │    │    pipeline-data    │
        │   • Sort Key:         │    │                     │
        │     timestamp         │    │   Folders:          │
        │   • GSI: metric_type- │    │   • raw-metrics/    │
        │     timestamp-index   │    │   • processed/      │
        │   • TTL: Enabled      │    │                     │
        │   • On-Demand Billing │    │   Lifecycle:        │
        │                       │    │   • 30-day IA       │
        │   960 writes/month    │    │   • 960 files/month │
        └───────────┬───────────┘    └──────────┬──────────┘
                    │                           │
                    │         ┌─────────────────┘
                    │         │
┌──────────────────────────────────────────────────────────────────────────────┐
│ PROCESSING LAYER                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                    │         │
                    │    ┌────▼─────────────────┐
                    │    │  S3 Event Trigger    │
                    │    │  (On Object Created) │
                    │    └────┬─────────────────┘
                    │         │
                    │    ┌────▼─────────────────┐
                    │    │  AWS Lambda          │
                    │    │  log-processor       │
                    │    │  • Parse JSON        │
                    │    │  • Transform Data    │
                    │    │  • Enrich Metadata   │
                    │    └────┬─────────────────┘
                    │         │
                    └─────────┴──────────┐
                                         │
┌──────────────────────────────────────▼────────────────────────────────────────┐
│ MONITORING & OBSERVABILITY LAYER                                              │
└────────────────────────────────────────────────────────────────────────────────┘
                                         │
                    ┌────────────────────┴────────────────────┐
                    │                                         │
        ┌───────────▼──────────┐              ┌──────────────▼──────────┐
        │  Amazon CloudWatch   │              │  Amazon CloudWatch      │
        │  Logs                │              │  Metrics                │
        │                      │              │                         │
        │  Log Groups:         │              │  Custom Metrics:        │
        │  • /aws/lambda/      │              │  • CPUUtilization       │
        │    data-collector    │              │  • MemoryUsage          │
        │  • /aws/lambda/      │              │  • DiskUsage            │
        │    log-processor     │              │  • NetworkTraffic       │
        │  • /aws/states/      │              │  • LambdaErrors         │
        │    pipeline          │              │  • LambdaDuration       │
        └───────────┬──────────┘              └──────────────┬──────────┘
                    │                                        │
                    └────────────────┬───────────────────────┘
                                     │
                         ┌───────────▼──────────┐
                         │  CloudWatch Alarms   │
                         │  (6 Alarms)          │
                         │                      │
                         │  • High CPU (>80%)   │
                         │  • Collector Errors  │
                         │  • Processor Errors  │
                         │  • DynamoDB Throttle │
                         │  • High Memory (>90%)│
                         │  • Lambda Duration   │
                         └───────────┬──────────┘
                                     │
┌──────────────────────────────────▼────────────────────────────────────────────┐
│ ALERTING LAYER                                                                 │
└────────────────────────────────────────────────────────────────────────────────┘
                                     │
                         ┌───────────▼──────────┐
                         │   Amazon SNS         │
                         │   Topic:             │
                         │   InfraMonitoring-   │
                         │   Alarms             │
                         │                      │
                         │   240 emails/month   │
                         └───────────┬──────────┘
                                     │
                              ┌──────▼──────┐
                              │   Email     │
                              │   Alerts    │
                              └─────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ ANALYTICS LAYER                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
                                     │
                         ┌───────────▼──────────┐
                         │   Amazon Athena      │
                         │   SQL Analytics      │
                         │                      │
                         │   Queries:           │
                         │   • Historical       │
                         │     Trends           │
                         │   • Aggregations     │
                         │   • Performance      │
                         │     Analysis         │
                         └──────────────────────┘Detailed Component Flow1. Trigger & Orchestration FlowEventBridge (Every 3 hours)
    ↓
Step Functions State Machine
    ↓
StartExecution
    ↓
ParallelState (4 branches)
    ├─→ InvokeCPUCollector
    ├─→ InvokeMemoryCollector
    ├─→ InvokeDiskCollector
    └─→ InvokeNetworkCollector
    ↓
WaitForCompletion (All branches)
    ↓
AggregateResults
    ↓
EndExecution2. Data Collection Flow (Per Branch)Lambda Invocation
    ↓
Generate Metrics
    ├─→ CPU: utilization, load_average
    ├─→ Memory: used, available, percent
    ├─→ Disk: used, free, percent
    └─→ Network: bytes_sent, bytes_received
    ↓
Add Metadata
    ├─→ timestamp
    ├─→ metric_id (UUID)
    ├─→ metric_type
    └─→ region
    ↓
Parallel Write
    ├─→ DynamoDB (Hot Path)
    └─→ S3 (Cold Path)3. Storage FlowData Ingestion
    ↓
┌─────────────────┴─────────────────┐
│                                   │
DynamoDB Write              S3 Write
    ↓                           ↓
Store in Table          Store as JSON
    ↓                           ↓
GSI Indexing            Trigger S3 Event
    ↓                           ↓
TTL Cleanup             Lambda Processing
(Auto-delete)                   ↓
                        Transform & Enrich
                                ↓
                        Write to DynamoDB4. Monitoring FlowLambda Execution
    ↓
CloudWatch Logs
    ├─→ Execution logs
    ├─→ Error logs
    └─→ Performance logs
    ↓
CloudWatch Metrics
    ├─→ Custom metrics
    ├─→ Lambda metrics
    └─→ DynamoDB metrics
    ↓
CloudWatch Alarms
    ├─→ Threshold evaluation
    └─→ Alarm state change
    ↓
SNS Notification
    ↓
Email Alert5. Analytics FlowHistorical Data (S3)
    ↓
Athena Query
    ↓
SQL Processing
    ├─→ Aggregations
    ├─→ Filtering
    └─→ Joins
    ↓
Query Results
    ↓
Analysis & InsightsPerformance MetricsExecution TimelineT+0ms:    EventBridge triggers Step Functions
T+100ms:  Step Functions starts parallel execution
T+150ms:  4 Lambda functions invoked simultaneously
T+917ms:  All Lambda functions complete
T+1000ms: Results aggregated
T+6300ms: Pipeline execution completeData VolumePer Execution:
    • 4 metrics collected
    • 8 writes (4 DynamoDB + 4 S3)
    • ~20KB data generated

Daily (8 executions):
    • 32 metrics
    • 64 writes
    • ~160KB data

Monthly (240 executions):
    • 960 metrics
    • 1,920 writes
    • ~20MB dataError Handling & Retry LogicLambda Execution
    ↓
Try: Execute Function
    ↓
    ├─→ Success → Continue
    │
    └─→ Failure
        ↓
        Retry #1 (Wait 10s)
        ↓
        ├─→ Success → Continue
        │
        └─→ Failure
            ↓
            Retry #2 (Wait 20s)
            ↓
            ├─→ Success → Continue
            │
            └─→ Failure
                ↓
                Retry #3 (Wait 40s)
                ↓
                ├─→ Success → Continue
                │
                └─→ Final Failure
                    ↓
                    CloudWatch Alarm
                    ↓
                    SNS AlertSecurity & IAM FlowIAM Role: DataPipelineLambdaRole
    ↓
Attached Policies:
    ├─→ AWSLambdaBasicExecutionRole
    ├─→ DynamoDB Read/Write
    ├─→ S3 Read/Write
    └─→ CloudWatch Logs
    ↓
Lambda Assumes Role
    ↓
Execute with Permissions
    ↓
Audit via CloudTrailCost Optimization FlowOriginal Design (5-min intervals)
    ↓
Cost Analysis
    ↓
Identified Optimization
    ├─→ Reduce frequency (3-hour intervals)
    ├─→ S3 lifecycle policies
    ├─→ DynamoDB on-demand
    └─→ Lambda memory optimization
    ↓
Optimized Design
    ↓
Cost Reduction: $2.00 → $0.02/month (99%)Legend┌─────┐
│ Box │  = AWS Service / Component
└─────┘

   ↓     = Data Flow Direction

   │     = Connection / Relationship

   ├─→   = Branch / Multiple Paths

   •     = List Item / FeatureKey CharacteristicsArchitecture Pattern: Lambda Architecture (Speed + Batch Layers)Processing Model: Event-Driven + ScheduledExecution Model: Parallel Processing (4 concurrent branches)Storage Strategy: Multi-tier (Hot + Cold paths)Monitoring: Comprehensive observability stackCost Model: Serverless, pay-per-useScalability: Linear scaling with data volumeReliability: 100% success rate with retry logic
