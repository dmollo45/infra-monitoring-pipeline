
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

```
┌─────────────────────────────────────────────────────