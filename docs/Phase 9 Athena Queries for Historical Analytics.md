
# Phase 9: Athena Queries for Historical Analytics

**Completion Date**: February 11, 2026  
**Duration**: 4 hours  
**Status**: ✅ Complete

---

## Overview

Phase 9 implements historical analytics capabilities using Amazon Athena to query infrastructure metrics stored in S3. This enables long-term trend analysis, performance reporting, and data-driven insights beyond the 15-day retention limit of CloudWatch metrics.

## Architecture

**Data Flow:**
```
Lambda (data-collector) 
  → S3 (JSON Lines format)
  → AWS Glue Crawler (schema detection)
  → Athena (SQL queries)
  → Analytics & Reports
```

**Key Components:**
- **S3 Storage**: Raw metrics in JSON Lines format (one JSON object per line)
- **AWS Glue Crawler**: Automatic schema detection and table cataloging
- **Athena Database**: `infra_monitoring_db`
- **Athena Table**: `raw_metrics`
- **Data Format**: JSON Lines (newline-delimited JSON)

---

## Data Format

### JSON Lines Structure

Each file contains 4 metrics (one JSON object per line):

```json
{"metric_id": "cpu-1770819523", "metric_type": "cpu_utilization", "timestamp": 1770819523, "value": "37.66", "instance_id": "i-608681", "region": "eu-west-1", "collected_at": "2026-02-11T14:18:43.994272"}
{"metric_id": "mem-1770819523", "metric_type": "memory_usage", "timestamp": 1770819523, "value": "73.07", "instance_id": "i-608681", "region": "eu-west-1", "collected_at": "2026-02-11T14:18:43.994272"}
{"metric_id": "disk-1770819523", "metric_type": "disk_usage", "timestamp": 1770819523, "value": "47.94", "instance_id": "i-608681", "region": "eu-west-1", "collected_at": "2026-02-11T14:18:43.994272"}
{"metric_id": "net-1770819523", "metric_type": "network_traffic", "timestamp": 1770819523, "value": "467.38", "instance_id": "i-608681", "region": "eu-west-1", "collected_at": "2026-02-11T14:18:43.994272"}
```

**Benefits of JSON Lines Format:**
- ✅ Native Athena support (no SerDe parsing issues)
- ✅ Simpler queries (direct column access, no UNNEST needed)
- ✅ Better performance (faster parsing)
- ✅ Industry standard (used by AWS CloudWatch Logs, Kinesis)
- ✅ Reliable (no HIVE_CURSOR_ERROR)

---

## Table Schema

### Athena Table: `raw_metrics`

```sql
CREATE EXTERNAL TABLE infra_monitoring_db.raw_metrics (
    metric_id STRING,
    metric_type STRING,
    timestamp BIGINT,
    value STRING,
    instance_id STRING,
    region STRING,
    collected_at STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://infra-monitoring-pipeline-data/raw-metrics/'
TBLPROPERTIES ('has_encrypted_data'='false');
```

**Column Descriptions:**
- `metric_id`: Unique identifier (e.g., "cpu-1770819523")
- `metric_type`: Type of metric (cpu_utilization, memory_usage, disk_usage, network_traffic)
- `timestamp`: Unix timestamp (seconds since epoch)
- `value`: Metric value as string (convert to DOUBLE for calculations)
- `instance_id`: EC2 instance identifier (e.g., "i-608681")
- `region`: AWS region (eu-west-1)
- `collected_at`: ISO 8601 timestamp string

---

## Analytical Queries

### 1. Daily Metrics Summary

**Purpose**: Provides 7-day rolling aggregates by metric type for trend analysis.

**Query:**
```sql
SELECT
    metric_type,
    DATE(from_unixtime(timestamp)) as date,
    COUNT(*) as total_readings,
    ROUND(AVG(CAST(value AS DOUBLE)), 2) as avg_value,
    ROUND(MIN(CAST(value AS DOUBLE)), 2) as min_value,
    ROUND(MAX(CAST(value AS DOUBLE)), 2) as max_value,
    ROUND(STDDEV(CAST(value AS DOUBLE)), 2) as std_dev
FROM infra_monitoring_db.raw_metrics
WHERE from_unixtime(timestamp) >= current_date - interval '7' day
GROUP BY metric_type, DATE(from_unixtime(timestamp))
ORDER BY date DESC, metric_type;
```

**Use Cases:**
- Weekly performance reports
- Capacity planning
- Trend identification
- Baseline establishment

---

### 2. High Utilization Alerts

**Purpose**: Identifies instances with >80% CPU, memory, or disk usage in the last 24 hours.

**Query:**
```sql
SELECT
    metric_type,
    instance_id,
    CAST(value AS DOUBLE) as value,
    collected_at,
    region
FROM infra_monitoring_db.raw_metrics
WHERE metric_type IN ('cpu_utilization', 'memory_usage', 'disk_usage')
  AND CAST(value AS DOUBLE) > 80.0
  AND from_unixtime(timestamp) >= current_timestamp - interval '24' hour
ORDER BY collected_at DESC, value DESC;
```

**Use Cases:**
- Performance bottleneck detection
- Resource allocation optimization
- Proactive incident prevention
- SLA compliance monitoring

---

### 3. Hourly Performance Trends

**Purpose**: Analyzes hourly averages by metric type for pattern detection.

**Query:**
```sql
SELECT
    metric_type,
    DATE_FORMAT(from_unixtime(timestamp), '%Y-%m-%d %H:00') as hour,
    COUNT(*) as readings,
    ROUND(AVG(CAST(value AS DOUBLE)), 2) as avg_value,
    ROUND(MIN(CAST(value AS DOUBLE)), 2) as min_value,
    ROUND(MAX(CAST(value AS DOUBLE)), 2) as max_value
FROM infra_monitoring_db.raw_metrics
WHERE from_unixtime(timestamp) >= current_timestamp - interval '24' hour
GROUP BY metric_type, DATE_FORMAT(from_unixtime(timestamp), '%Y-%m-%d %H:00')
ORDER BY hour DESC, metric_type;
```

**Use Cases:**
- Peak usage identification
- Workload pattern analysis
- Capacity planning
- Cost optimization

---

### 4. Instance Performance Summary

**Purpose**: Shows per-instance metrics summary for resource management.

**Query:**
```sql
SELECT
    instance_id,
    metric_type,
    COUNT(*) as readings,
    ROUND(AVG(CAST(value AS DOUBLE)), 2) as avg_value,
    ROUND(MAX(CAST(value AS DOUBLE)), 2) as max_value,
    MIN(collected_at) as first_seen,
    MAX(collected_at) as last_seen
FROM infra_monitoring_db.raw_metrics
WHERE from_unixtime(timestamp) >= current_timestamp - interval '24' hour
GROUP BY instance_id, metric_type
ORDER BY instance_id, metric_type;
```

**Use Cases:**
- Instance health monitoring
- Resource utilization tracking
- Right-sizing recommendations
- Cost allocation

---

### 5. Latest Metrics View

**Purpose**: Quick access to the most recent hour of data for operational dashboards.

**Query:**
```sql
CREATE OR REPLACE VIEW infra_monitoring_db.latest_metrics AS
SELECT
    metric_id,
    metric_type,
    instance_id,
    CAST(value AS DOUBLE) as value,
    collected_at,
    region,
    from_unixtime(timestamp) as timestamp_dt
FROM infra_monitoring_db.raw_metrics
WHERE from_unixtime(timestamp) >= current_timestamp - interval '1' hour
ORDER BY collected_at DESC;
```

**Usage:**
```sql
SELECT * FROM infra_monitoring_db.latest_metrics;
```

**Use Cases:**
- Real-time operational dashboards
- Quick health checks
- Recent anomaly detection
- Current state monitoring

---

## AWS Glue Crawler Configuration

### Crawler: `infra-metrics-crawler`

**Settings:**
- **Name**: `infra-metrics-crawler`
- **Data source**: S3 (`s3://infra-monitoring-pipeline-data/raw-metrics/`)
- **IAM role**: `AWSGlueServiceRole-DataPipelineLambdaRole`
- **Target database**: `infra_monitoring_db`
- **Schedule**: On demand (manual execution)
- **Crawler behavior**: Crawl all sub-folders

**Permissions Required:**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::infra-monitoring-pipeline-data",
                "arn:aws:s3:::infra-monitoring-pipeline-data/*"
            ]
        }
    ]
}
```

**Trust Relationship:**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "lambda.amazonaws.com",
                    "glue.amazonaws.com"
                ]
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

---

## Performance Optimization

### Query Optimization Tips

1. **Use Partitioning**: Add date-based partitions for faster queries
2. **Filter Early**: Apply WHERE clauses before aggregations
3. **Limit Results**: Use LIMIT for exploratory queries
4. **Cast Once**: Convert value to DOUBLE in subqueries, not repeatedly
5. **Use Views**: Create views for frequently used query patterns

### Cost Optimization

**Athena Pricing**: $5 per TB of data scanned

**Optimization Strategies:**
- ✅ Use columnar formats (Parquet) for large datasets
- ✅ Partition data by date for time-range queries
- ✅ Use LIMIT to reduce data scanned during development
- ✅ Compress files (GZIP) to reduce storage and scan costs
- ✅ Use views to encapsulate complex queries

**Current Cost**: ~$0.01/month (scanning ~2GB/month)

---

## Troubleshooting

### Common Issues

**Issue 1: HIVE_CURSOR_ERROR**
- **Cause**: JSON array format not supported by SerDe
- **Solution**: Use JSON Lines format (one object per line)

**Issue 2: Empty Query Results**
- **Cause**: Table not refreshed after new files added
- **Solution**: Run `MSCK REPAIR TABLE infra_monitoring_db.raw_metrics;`

**Issue 3: Schema Mismatch**
- **Cause**: Mixed file formats in S3 location
- **Solution**: Separate old and new data into different folders

**Issue 4: Slow Queries**
- **Cause**: Full table scans without partitioning
- **Solution**: Add date-based partitions and use WHERE clauses

---

## Key Achievements

- ✅ **Implemented JSON Lines format** for reliable Athena parsing (eliminated HIVE_CURSOR_ERROR)
- ✅ **Created 5 analytical queries** covering daily summaries, alerts, trends, and instance performance
- ✅ **Configured AWS Glue Crawler** for automatic schema detection and table cataloging
- ✅ **Reduced file count by 75%** (288 files/day vs 1,152 files/day)
- ✅ **Achieved $0 Glue costs** (well within 1M objects/month Free Tier)
- ✅ **Maintained ~$0.50/month total cost** for entire infrastructure monitoring pipeline
- ✅ **Enabled historical analytics** beyond CloudWatch's 15-day retention limit
- ✅ **Provided SQL-based querying** for flexible data analysis and reporting

---

## Cost Summary

**Phase 9 Components:**
- **AWS Glue Crawler**: $0.00 (FREE - under 1M objects/month)
- **Athena Queries**: ~$0.01/month (scanning ~2GB/month)
- **S3 Storage**: Included in overall project cost (~$0.40/month)

**Total Phase 9 Cost**: ~$0.01/month

**Overall Project Cost**: ~$0.50/month (unchanged)

---

## Next Steps

**Potential Enhancements:**
1. **Add Partitioning**: Implement date-based partitions for faster queries
2. **Convert to Parquet**: Use columnar format for better compression and performance
3. **Create Dashboards**: Build QuickSight dashboards for visual analytics
4. **Automate Reports**: Schedule Athena queries with Lambda for automated reporting
5. **Add Data Retention**: Implement S3 lifecycle policies to archive old data
6. **Expand Metrics**: Add additional metric types (network latency, error rates, etc.)

---

## References

- [Amazon Athena Documentation](https://docs.aws.amazon.com/athena/)
- [AWS Glue Crawler Documentation](https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html)
- [JSON Lines Format Specification](https://jsonlines.org/)
- [Athena Query Optimization](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning.html)

---
### Query Results

![Basic Verification Query](../screenshots/phase9-athena/query-basic-verification.png)
*Basic verification query showing all 4 metric types with counts and averages*

### AWS Glue Crawler

![Glue Crawler Configuration](../screenshots/phase9-athena/glue-crawler-config.png)
*AWS Glue Crawler configuration for automatic schema detection*


**Phase 9 Status**: ✅ Complete  
**Documentation Last Updated**: February 11, 2026, 2:29 PM UTC
