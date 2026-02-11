Phase 8: CloudWatch Alarms & Alerting ✅ COMPLETED

Date Completed: February 10, 2026
Duration: 2 hours
Status: ✅ Completed
Objectives

    Create SNS topic for alarm notifications
    Configure CloudWatch alarms for automated alerting
    Set up email notifications for critical events
    Test alarm triggers and notification delivery
    Document alarm configurations and thresholds

Deliverables

    ✅ SNS topic InfraMonitoring-Alarms created with email subscription
    ✅ 6 CloudWatch alarms configured for automated monitoring
    ✅ Email notifications tested and verified
    ✅ Alarm documentation with thresholds and actions
    ✅ Portfolio screenshots captured

SNS Topic Configuration

Topic Name: InfraMonitoring-Alarms
Protocol: Email
Subscription: Confirmed email endpoint for alarm notifications
CloudWatch Alarms Created
1. High CPU Utilization Alarm

    Alarm Name: InfraMonitoring-HighCPU
    Metric: cpu_utilization (InfraMonitoring namespace)
    Threshold: > 80%
    Evaluation Period: 2 consecutive periods of 5 minutes
    Action: Send notification to SNS topic
    Purpose: Alert when CPU usage exceeds safe operating threshold

2. Lambda Errors - Data Collector

    Alarm Name: DataCollector-Errors
    Metric: Errors (AWS/Lambda namespace)
    Threshold: > 0 errors
    Evaluation Period: 1 period of 5 minutes
    Action: Send notification to SNS topic
    Purpose: Immediate alert on data collection failures

3. Lambda Errors - Log Processor

    Alarm Name: LogProcessor-Errors
    Metric: Errors (AWS/Lambda namespace)
    Threshold: > 0 errors
    Evaluation Period: 1 period of 5 minutes
    Action: Send notification to SNS topic
    Purpose: Immediate alert on log processing failures

4. DynamoDB Throttling

    Alarm Name: InfraMetrics-Throttling
    Metric: UserErrors (AWS/DynamoDB namespace)
    Threshold: > 0 throttles
    Evaluation Period: 2 consecutive periods of 5 minutes
    Action: Send notification to SNS topic
    Purpose: Alert when DynamoDB capacity is exceeded

5. High Memory Usage

    Alarm Name: InfraMonitoring-HighMemory
    Metric: memory_usage (InfraMonitoring namespace)
    Threshold: > 90%
    Evaluation Period: 2 consecutive periods of 5 minutes
    Action: Send notification to SNS topic
    Purpose: Alert when memory usage approaches critical levels

6. Lambda Duration Threshold

    Alarm Name: DataCollector-HighDuration
    Metric: Duration (AWS/Lambda namespace)
    Threshold: > 3000ms (3 seconds)
    Evaluation Period: 3 consecutive periods of 5 minutes
    Action: Send notification to SNS topic
    Purpose: Alert when Lambda execution time indicates performance degradation

Key Achievements
Automated Alerting

    Proactive monitoring - Alarms trigger before issues impact system availability
    Email notifications - Instant alerts delivered to configured email address
    Multi-layer coverage - Alarms span infrastructure, application, and database layers
    Threshold tuning - Alarm thresholds set based on operational best practices

Operational Benefits

    Reduced MTTR - Mean Time To Resolution decreased through immediate notifications
    Cost optimization - Early detection of throttling prevents over-provisioning
    Performance tracking - Duration alarms identify optimization opportunities
    Reliability improvement - Error alarms enable rapid incident response

Technical Implementation
SNS Topic Creation

Phase 8 - CloudWatch Alarms Documentation

aws sns create-topic \
    --name InfraMonitoring-Alarms \
    --region eu-west-1

aws sns subscribe \
    --topic-arn arn:aws:sns:eu-west-1:ACCOUNT_ID:InfraMonitoring-Alarms \
    --protocol email \
    --notification-endpoint your-email@example.com

Sample Alarm Configuration (High CPU)

Phase 8 - CloudWatch Alarms Documentation

aws cloudwatch put-metric-alarm \
    --alarm-name InfraMonitoring-HighCPU \
    --alarm-description "Alert when CPU utilization exceeds 80%" \
    --metric-name cpu_utilization \
    --namespace InfraMonitoring \
    --statistic Average \
    --period 300 \
    --evaluation-periods 2 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --dimensions Name=Region,Value=eu-west-1 \
    --alarm-actions arn:aws:sns:eu-west-1:ACCOUNT_ID:InfraMonitoring-Alarms \
    --region eu-west-1

Testing & Validation
Alarm Testing Process

    Trigger simulation - Manually published high metric values to CloudWatch
    State verification - Confirmed alarms transitioned to ALARM state
    Notification delivery - Verified email notifications received within 1 minute
    Recovery testing - Confirmed alarms returned to OK state after metrics normalized

Test Results

    ✅ All 6 alarms successfully created
    ✅ SNS email subscription confirmed
    ✅ Test notifications delivered successfully
    ✅ Alarm state transitions working correctly
    ✅ Email formatting and content verified

Documentation

    Phase 8 Documentation: docs/phase8-cloudwatch-alarms.md
    Screenshots Directory: screenshots/phase8-alarms/
    Alarm Configurations: Detailed in phase documentation

Screenshots

    sns-topic-created.png - SNS topic configuration
    email-subscription-confirmed.png - Email subscription confirmation
    alarms-overview.png - All 6 alarms in CloudWatch console
    high-cpu-alarm-config.png - High CPU alarm configuration
    lambda-error-alarms.png - Lambda error alarm configurations
    dynamodb-throttling-alarm.png - DynamoDB throttling alarm
    test-notification-email.png - Sample alarm notification email
    alarm-history.png - Alarm state change history

Key Learnings

    SNS subscription confirmation - Email subscriptions require manual confirmation before notifications work
    Alarm evaluation periods - Multiple evaluation periods reduce false positives from transient spikes
    Metric dimensions - Dimension filters ensure alarms monitor correct reyour source documents. Threshold tuning - Conservative thresholds (80% CPU, 90% memory) provide early warning
    Testing importance - Manual alarm testing validates configuration before production incidents

Next Steps

Phase 9: Step Functions Workflow (Scheduled: February 11, 2026)

    Design state machine for orchestrating data pipeline
    Implement error handling and retry logic
    Add parallel processing for improved performance
    Create workflow visualization
    Test end-to-end pipeline orchestration

Phase Status: ✅ Completed
Total Time Invested: 2 hours
Alarms Created: 6
SNS Topics: 1
Email Subscriptions: 1 (Confirmed)davoduo