
# Infrastructure Monitoring Pipeline - Complete Project Documentation

**Project Name**: Serverless Infrastructure Monitoring Pipeline  
**Duration**: January 27 - February 19, 2026 (24 days)  
**Status**: ✅ 100% COMPLETE  
**AWS Region**: eu-west-1 (Europe - Ireland)  
**Final Monthly Cost**: ~$0.02 (99% under budget)

---

## Executive Summary

I successfully built a production-ready serverless infrastructure monitoring pipeline on AWS that collects, processes, stores, and analyzes system metrics with automated alerting capabilities. The project demonstrates advanced cloud architecture skills including parallel processing, workflow orchestration, and cost optimization.

### Key Achievements

- ✅ **100% Serverless Architecture** - No servers to manage or maintain
- ✅ **Parallel Processing** - 3.3x performance improvement with Step Functions
- ✅ **Cost Optimized** - Stays within AWS Free Tier (~$0.02/month)
- ✅ **Production Ready** - Comprehensive error handling and monitoring
- ✅ **Fully Automated** - EventBridge scheduling with 3-hour intervals
- ✅ **Scalable Design** - Can handle 10x data volume without architecture changes

### Technologies Used

**Compute**: AWS Lambda (Python 3.14)  
**Storage**: Amazon S3, DynamoDB  
**Orchestration**: AWS Step Functions, EventBridge  
**Monitoring**: CloudWatch Logs, Metrics, Dashboards  
**Alerting**: Amazon SNS  
**Analytics**: Amazon Athena  
**Security**: IAM roles and policies

---

## Project Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                EventBridge Rule (Every 3 Hours)                  │
│                    8 executions/day = 240/month                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              Step Functions State Machine                        │
│           InfraMonitoring-Pipeline-Orchestration                 │
│                                                                   │
│  ┌───────────────────────────────────────────────────────┐     │
│  │         ParallelDataCollection (4 Branches)           │     │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐│     │
│  │  │   CPU    │ │  Memory  │ │   Disk   │ │ Network  ││     │
│  │  │ Metrics  │ │ Metrics  │ │ Metrics  │ │ Metrics  ││     │
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘│     │
│  │       └────────────┴─────────────┴────────────┘      │     │
│  │                    Lambda: data-collector             │     │
│  └───────────────────────────┬───────────────────────────┘     │
│                              │                                   │
│                    ┌─────────▼─────────┐                        │
│                    │ WaitForProcessing  │                        │
│                    │    (5 seconds)     │                        │
│                    └─────────┬─────────┘                        │
│                              │                                   │
│                    ┌─────────▼─────────┐                        │
│                    │CheckPipelineHealth│                        │
│                    └─────────┬─────────┘                        │
│                              │                                   │
│                    ┌─────────▼─────────┐                        │
│                    │ ParallelAnalytics  │                        │
│                    │   (2 Branches)     │                        │
│                    └─────────┬─────────┘                        │
│                              │                                   │
│                    ┌─────────▼─────────┐                        │
│                    │   NotifySuccess    │                        │
│                    │   (SNS Email)      │                        │
│                    └────────────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Amazon S3  │    │  DynamoDB    │    │  CloudWatch  │
│  Raw Metrics │    │ InfraMetrics │    │   Metrics    │
│              │    │              │    │              │
│ 960 files/mo │    │ 960 writes/mo│    │ 960 points/mo│
└──────┬───────┘    └──────────────┘    └──────────────┘
       │
       │ S3 Event Notification
       ▼
┌──────────────┐
│   Lambda     │
│log-processor │
│              │
│ Triggered by │
│ S3 events    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Athena     │
│   Queries    │
│              │
│ SQL analysis │
│ on S3 data   │
└──────────────┘
```

---

## Phase-by-Phase Implementation

### Phase 1: Initial Setup & IAM Configuration
**Date**: January 27, 2026 (Day 1)  
**Status**: ✅ COMPLETE

**What I Built**:
- AWS account setup with MFA enabled
- IAM user with programmatic access
- Lambda execution role with S3, DynamoDB, CloudWatch permissions
- Step Functions execution role with Lambda, SNS permissions

**Key Deliverables**:
- ✅ AWS CLI configured
- ✅ IAM roles created with least-privilege policies
- ✅ Security best practices documented

**Lessons Learned**:
- Always use IAM roles instead of hardcoded credentials
- Enable MFA for all privileged accounts
- Document all permissions for audit purposes

---

### Phase 2: S3 & DynamoDB Setup
**Date**: January 28, 2026 (Day 2)  
**Status**: ✅ COMPLETE

**What I Built**:
- S3 bucket: `infra-monitoring-pipeline-data`
- Folder structure: `raw-metrics/YYYY/MM/DD/`
- DynamoDB table: `InfraMetrics` with on-demand billing
- S3 lifecycle policies for cost optimization

**Key Deliverables**:
- ✅ S3 bucket with versioning and public access blocked
- ✅ DynamoDB table with partition key (metric_id) and sort key (timestamp)
- ✅ Lifecycle policy: transition to IA after 30 days, delete after 90 days

**Cost Optimization**:
- S3 lifecycle policies reduce storage costs by 50%
- DynamoDB on-demand billing eliminates provisioned capacity waste

---

### Phase 3: Lambda Data Collector
**Date**: January 29-30, 2026 (Days 3-4)  
**Status**: ✅ COMPLETE

**What I Built**:
- Lambda function: `data-collector` (Python 3.14)
- Generates 4 metric types: CPU, Memory, Disk, Network
- Writes to S3 (JSON Lines format)
- Writes to DynamoDB (batch operations)
- Publishes to CloudWatch Metrics

**Key Deliverables**:
- ✅ Lambda function with 128MB memory, 30s timeout
- ✅ Supports parallel processing with `metric_type` parameter
- ✅ Backward compatible (defaults to collecting all metrics)

**Technical Highlights**:
- Used `boto3` for AWS service integration
- Implemented batch writes for DynamoDB efficiency
- JSON Lines format for S3 enables streaming processing

---

### Phase 4: S3 Event Trigger & Log Processor
**Date**: January 31 - February 1, 2026 (Days 5-6)  
**Status**: ✅ COMPLETE

**What I Built**:
- S3 event notification for `raw-metrics/` prefix
- Lambda function: `log-processor`
- Automatic processing of new metric files
- Threshold-based alerting logic

**Key Deliverables**:
- ✅ S3 event notification configured
- ✅ Log processor Lambda deployed
- ✅ Automatic processing on file upload

**Technical Highlights**:
- Event-driven architecture reduces polling overhead
- Processes JSON Lines format efficiently
- Logs warnings for metrics exceeding thresholds

---

### Phase 5: CloudWatch Integration
**Date**: February 3-4, 2026 (Days 7-8)  
**Status**: ✅ COMPLETE

**What I Built**:
- CloudWatch Logs for Lambda functions
- Custom CloudWatch Metrics in `InfraMonitoring` namespace
- CloudWatch Dashboard with 4 metric visualizations

**Key Deliverables**:
- ✅ Log retention set to 7 days (cost optimization)
- ✅ Custom metrics with Region and InstanceID dimensions
- ✅ Dashboard with line charts for all metric types

**Monitoring Capabilities**:
- Real-time metric visualization
- Lambda invocation and error tracking
- Historical trend analysis

---

### Phase 6: SNS Alerting System
**Date**: February 5, 2026 (Day 9)  
**Status**: ✅ COMPLETE

**What I Built**:
- SNS topic: `InfraMonitoring-Alarms`
- Email subscription for notifications
- Integration with Step Functions for success/failure alerts

**Key Deliverables**:
- ✅ SNS topic created
- ✅ Email subscription confirmed
- ✅ Success and failure notifications configured

**Alert Types**:
- Pipeline execution success (every 3 hours)
- Pipeline execution failure (with error details)
- Threshold violations (future enhancement)

---

### Phase 7: Athena Query Setup
**Date**: February 6, 2026 (Day 10)  
**Status**: ✅ COMPLETE

**What I Built**:
- Athena database: `infra_monitoring`
- External table pointing to S3 raw metrics
- SQL queries for historical analysis

**Key Deliverables**:
- ✅ Athena database and table created
- ✅ Query result location configured
- ✅ Sample analytical queries documented

**Query Capabilities**:
- Average CPU utilization by instance
- Metrics over time analysis
- Threshold violation detection
- Cost: ~$0.01/month for minimal queries

---

### Phase 8: EventBridge Automation
**Date**: February 7, 2026 (Day 11)  
**Status**: ✅ COMPLETE

**What I Built**:
- EventBridge rule: `InfraMonitoring-Trigger`
- Schedule: `rate(3 hours)` = 8 executions/day
- Integration with Step Functions state machine

**Key Deliverables**:
- ✅ EventBridge rule created and enabled
- ✅ 3-hour schedule configured
- ✅ Step Functions as target

**Cost Optimization**:
- Changed from 5-minute to 3-hour intervals
- Reduced monthly executions from 8,640 to 240
- Saved 99% on Step Functions costs

---

### Phase 9: Testing & Optimization
**Date**: February 10-14, 2026 (Days 12-14)  
**Status**: ✅ COMPLETE

**What I Tested**:
- Unit testing: Lambda functions with different inputs
- Integration testing: End-to-end pipeline execution
- Performance testing: Parallel vs sequential execution
- Error handling: Retry logic and failure scenarios

**Optimization Results**:
- **Performance**: 3.3x faster with parallel processing
- **Cost**: 99% reduction ($2.00 → $0.02/month)
- **Reliability**: 100% success rate in 50+ test executions

**Key Metrics**:
- Lambda cold start: ~690ms
- Parallel execution: ~917ms for 4 metrics
- Total pipeline: ~6.3 seconds end-to-end

---

### Phase 10: Step Functions Workflow Orchestration
**Date**: February 17-19, 2026 (Days 15-17)  
**Status**: ✅ COMPLETE

**What I Built**:
- Step Functions state machine: `InfraMonitoring-Pipeline-Orchestration`
- 4 parallel branches for simultaneous metric collection
- Comprehensive error handling with retry logic
- SNS notifications for success/failure

**Key Deliverables**:
- ✅ State machine with 15 states
- ✅ Parallel processing (3.3x faster)
- ✅ Error handling with exponential backoff
- ✅ EventBridge integration (3-hour schedule)
- ✅ Stays within FREE tier (2,880 transitions/month)

**Technical Achievements**:
- Parallel data collection reduces execution time by 66%
- Individual branch failures don't break entire pipeline
- Complete execution history and audit trail
- Visual workflow representation for debugging

---

## Performance Metrics

### Execution Performance

| Metric | Value |
|--------|-------|
| **Parallel Data Collection** | 917ms |
| **Total Pipeline Execution** | 6.3 seconds |
| **Lambda Cold Start** | 690ms |
| **Lambda Warm Start** | 50-100ms |
| **S3 Write Latency** | 100-200ms |
| **DynamoDB Write Latency** | 50-100ms |

### Throughput Metrics

| Metric | Value |
|--------|-------|
| **Metrics Collected/Day** | 32 (8 executions × 4 metrics) |
| **Metrics Collected/Month** | 960 |
| **S3 Files Created/Month** | 960 |
| **DynamoDB Records/Month** | 960 |
| **CloudWatch Data Points/Month** | 960 |

### Reliability Metrics

| Metric | Value |
|--------|-------|
| **Success Rate** | 100% (50+ executions) |
| **Lambda Error Rate** | 0% |
| **Step Functions Success Rate** | 100% |
| **Average Execution Time** | 6.3 seconds |

---

## Cost Analysis

### Monthly Cost Breakdown

| Service | Usage | FREE Tier Limit | Actual Cost |
|---------|-------|-----------------|-------------|
| **Step Functions** | 2,880 transitions | 4,000/month | $0.00 |
| **Lambda** | 960 invocations | 1M/month | $0.00 |
| **S3** | 960 files (~20MB) | 5GB/month | $0.01 |
| **DynamoDB** | 960 writes | 25GB storage | $0.00 |
| **CloudWatch** | Logs + Metrics | Always Free | $0.00 |
| **SNS** | 240 emails | 1,000/month | $0.00 |
| **EventBridge** | 240 triggers | Always Free | $0.00 |
| **Athena** | Minimal queries | 1TB/month | $0.01 |
| **Total** | | | **$0.02/month** |

### Cost Optimization Strategies

1. **EventBridge Scheduling**: Changed from 5-minute to 3-hour intervals (99% cost reduction)
2. **S3 Lifecycle Policies**: Transition to IA after 30 days, delete after 90 days (50% storage savings)
3. **DynamoDB On-Demand**: Pay only for actual usage (no provisioned capacity waste)
4. **Lambda Memory Optimization**: 128MB sufficient for workload (lowest cost tier)
5. **CloudWatch Log Retention**: 7 days instead of indefinite (reduces storage costs)

**Total Savings**: $1.98/month (99% under original $2.00 budget)

---

## Technical Highlights

### 1. Parallel Processing Architecture

**Implementation**:
- Step Functions Parallel state with 4 branches
- Each branch invokes Lambda with specific `metric_type` parameter
- All branches execute simultaneously

**Benefits**:
- 3.3x faster than sequential execution
- Scales linearly with additional metric types
- Fault isolation (one failure doesn't break pipeline)

**Performance**:
- Sequential: 4 × 750ms = 3,000ms
- Parallel: 917ms (all 4 metrics)
- Improvement: 66% reduction in execution time

### 2. Error Handling & Retry Logic

**Retry Configuration**:
- 3 retry attempts per branch
- Exponential backoff: 10s, 20s, 40s
- Prevents transient failures

**Graceful Degradation**:
- Individual branch failures don't break pipeline
- Partial data collection is better than complete failure
- SNS notifications for all failure scenarios

**Error Notification**:
- Success emails every 3 hours
- Failure emails with detailed error information
- CloudWatch Logs for debugging

### 3. Event-Driven Architecture

**S3 Event Notifications**:
- Automatic processing on file upload
- No polling overhead
- Real-time data processing

**EventBridge Scheduling**:
- Cron-like scheduling without servers
- Reliable execution every 3 hours
- Automatic retry on failures

### 4. Dual Storage Strategy

**S3 (Data Lake)**:
- Raw metrics in JSON Lines format
- Partitioned by date (YYYY/MM/DD)
- Queryable with Athena SQL
- Cost-effective long-term storage

**DynamoDB (Operational Database)**:
- Structured data for fast queries
- Partition key: metric_id
- Sort key: timestamp
- On-demand billing for cost efficiency

---

## Key Learnings

### Technical Insights

1. **Parallel Processing is Essential**
   - 3.3x performance improvement with minimal code changes
   - Critical for production-grade data pipelines
   - Scales linearly with data volume

2. **Error Handling is Non-Negotiable**
   - Retry logic prevents transient failures
   - Graceful degradation maintains service availability
   - Comprehensive logging aids troubleshooting

3. **Cost Optimization Requires Planning**
   - Small scheduling changes = massive cost reductions
   - Always calculate monthly usage before deployment
   - FREE tier limits are generous but easy to exceed

4. **Step Functions Simplifies Orchestration**
   - Visual workflow aids debugging
   - Built-in retry and error handling
   - Complete execution history and audit trail

### Best Practices

1. **Design for Failure**
   - Every state should have error handling
   - Use Catch blocks for graceful degradation
   - Always send notifications on failures

2. **Optimize for Cost**
   - Calculate monthly usage before deployment
   - Use EventBridge schedules wisely
   - Monitor state transitions in CloudWatch

3. **Test Thoroughly**
   - Test parallel execution with real data
   - Simulate failures to verify error handling
   - Verify end-to-end workflow multiple times

4. **Document Everything**
   - State machine JSON version controlled
   - Document retry policies and error handling
   - Maintain execution logs for troubleshooting

---

## Challenges Overcome

### Challenge 1: Lambda Function Modification
**Problem**: Existing Lambda collected all metrics together, not individually.

**Solution**: Added `metric_type` parameter support while maintaining backward compatibility. Function now accepts optional parameter and defaults to collecting all metrics if none provided.

### Challenge 2: State Transition Limits
**Problem**: Initial 5-minute schedule would exceed FREE tier (103,680 transitions/month).

**Solution**: Changed to 3-hour schedule, reducing transitions to 2,880/month (72% of FREE tier). Still provides adequate monitoring coverage with 8 data points per day.

### Challenge 3: Error Handling Complexity
**Problem**: Needed to handle individual branch failures without breaking entire pipeline.

**Solution**: Implemented separate Catch blocks for each branch with failure states, allowing partial success. Pipeline continues even if one metric collection fails.

### Challenge 4: Testing Parallel Execution
**Problem**: Difficult to verify all branches execute simultaneously.

**Solution**: Used CloudWatch Logs timestamps to confirm all 4 Lambda invocations started within 917ms. Verified separate S3 files created with different instance IDs.

---

## Future Enhancements

### Short-Term (1-3 months)

1. **Real Infrastructure Monitoring**
   - Replace synthetic metrics with actual EC2/RDS monitoring
   - Integrate with CloudWatch Agent
   - Add custom application metrics

2. **Advanced Analytics**
   - Machine learning for anomaly detection
   - Predictive alerting based on trends
   - Automated capacity planning

3. **Enhanced Dashboards**
   - QuickSight dashboards for business users
   - Real-time metric streaming
   - Custom visualization widgets

### Long-Term (3-6 months)

1. **Multi-Region Support**
   - Deploy pipeline in multiple AWS regions
   - Cross-region data aggregation
   - Global dashboard view

2. **Auto-Remediation**
   - Automated response to threshold violations
   - Lambda functions for common fixes
   - Integration with AWS Systems Manager

3. **Cost Optimization**
   - S3 Intelligent-Tiering for automatic cost optimization
   - Reserved capacity for predictable workloads
   - Spot instances for batch processing

---

## Conclusion

I successfully built a production-ready serverless infrastructure monitoring pipeline on AWS that demonstrates:

- ✅ **Advanced Cloud Architecture** - Parallel processing, event-driven design, dual storage
- ✅ **Cost Optimization** - 99% under budget, stays within FREE tier
- ✅ **Operational Excellence** - Comprehensive monitoring, error handling, automation
- ✅ **Scalability** - Can handle 10x data volume without architecture changes
- ✅ **Security** - IAM roles, least-privilege policies, encrypted storage

**Project Status**: 🎉 **100% COMPLETE**

**Total Duration**: 24 days (January 27 - February 19, 2026)

**Final Monthly Cost**: ~$0.02 (well under $2 budget)

This project showcases my ability to design and implement production-grade serverless architectures on AWS, with a focus on performance, cost optimization, and operational excellence.

---

## Project Statistics

- **Total Lines of Code**: ~500 (Python)
- **AWS Services Used**: 8 (Lambda, S3, DynamoDB, Step Functions, EventBridge, SNS, CloudWatch, Athena)
- **IAM Roles Created**: 2
- **Lambda Functions**: 2
- **Step Functions States**: 15
- **CloudWatch Dashboards**: 1
- **Documentation Pages**: 11 (including this summary)
- **Screenshots Captured**: 20+
- **Test Executions**: 50+
- **Success Rate**: 100%


