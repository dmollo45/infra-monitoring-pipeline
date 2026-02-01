# Database Schema

## DynamoDB Table: InfraMetrics

### Primary Key Design
- **Partition Key**: `metric_id` (String)
  - Format: `{metric_type}-{timestamp}-{host_id}`
  - Example: `cpu-1738440000-host-001`
- **Sort Key**: `timestamp` (Number)
  - Unix timestamp in seconds
  - Example: `1738440000`

### Attributes
| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| metric_id | String | Unique identifier (PK) | `cpu-1738440000-host-001` |
| timestamp | Number | Unix timestamp (SK) | `1738440000` |
| metric_type | String | Type of metric | `cpu`, `memory`, `disk`, `network` |
| value | Number | Metric value | `45.5` |
| host_id | String | Server identifier | `host-001` |
| region | String | AWS region | `us-east-1` |
| ttl | Number | Expiration timestamp | `[CREDIT_DEBIT_CARD_EXPIRY]` |

### Global Secondary Index
**Index Name**: `metric_type-timestamp-index`
- Allows querying all metrics of a specific type
- Example query: "Get all CPU metrics from the last hour"

### Data Retention
- **S3**: 30 days (lifecycle policy)
- **DynamoDB**: 30 days (TTL)
