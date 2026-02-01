# Phase 2: S3 & DynamoDB Setup
**Date**: February 1, 2026
**Status**: ✅ Complete

## Resources Created

### S3 Bucket
- **Bucket Name**: `infra-monitoring-pipeline-data`
- **Region**: [your-region, e.g., us-east-1]
- **Lifecycle Policy**: 30-day automatic deletion
- **Purpose**: Store raw metric JSON files from data-collector Lambda

### DynamoDB Table
- **Table Name**: `InfraMetrics`
- **Partition Key**: `metric_id` (String)
- **Sort Key**: `timestamp` (Number)
- **Billing Mode**: On-demand
- **Purpose**: Store processed metrics for querying

### Global Secondary Index
- **Index Name**: `metric_type-timestamp-index`
- **Partition Key**: `metric_type` (String)
- **Sort Key**: `timestamp` (Number)
- **Projection**: ALL attributes

### TTL Configuration
- **Enabled**: Yes
- **TTL Attribute**: `ttl`
- **Retention**: 30 days

## Testing Completed
- ✅ Manual S3 file upload
- ✅ Manual DynamoDB item creation
- ✅ Lifecycle policy verified
- ✅ GSI verified as Active
- ✅ TTL enabled and verified



