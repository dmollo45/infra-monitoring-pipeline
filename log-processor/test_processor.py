import unittest
import json
from decimal import Decimal
from datetime import datetime

# Mock the Lambda function logic locally
def prepare_dynamodb_items(metrics_data):
    items = []
    timestamp = metrics_data.get('timestamp')
    server_id = metrics_data.get('server_id')

    for metric in metrics_data.get('metrics', []):
        item = {
            'metric_id': f"{server_id}#{metric['metric_type']}#{timestamp}",
            'timestamp': timestamp,
            'server_id': server_id,
            'metric_type': metric['metric_type'],
            'value': Decimal(str(metric['value'])),
            'unit': metric.get('unit', 'percent'),
            'ttl': int(datetime.now().timestamp()) + (30 * 24 * 60 * 60)
        }
        items.append(item)

    return items

class TestLogProcessor(unittest.TestCase):

    def test_prepare_dynamodb_items(self):
        """Test metric conversion to DynamoDB format"""
        sample_data = {
            'timestamp': '2026-01-31T12:00:00Z',
            'server_id': 'server-001',
            'metrics': [
                {'metric_type': 'cpu_usage', 'value': 45.2, 'unit': 'percent'},
                {'metric_type': 'memory_usage', 'value': 62.8, 'unit': 'percent'}
            ]
        }

        items = prepare_dynamodb_items(sample_data)

        self.assertEqual(len(items), 2)
        self.assertEqual(items['server_id'], 'server-001')
        self.assertEqual(items['metric_type'], 'cpu_usage')
        self.assertIsInstance(items['value'], Decimal)

    def test_metric_id_format(self):
        """Test metric_id composite key format"""
        sample_data = {
            'timestamp': '2026-01-31T12:00:00Z',
            'server_id': 'server-002',
            'metrics': [
                {'metric_type': 'disk_usage', 'value': 78.5, 'unit': 'percent'}
            ]
        }

        items = prepare_dynamodb_items(sample_data)
        expected_id = 'server-002#disk_usage#2026-01-31T12:00:00Z'

        self.assertEqual(items['metric_id'], expected_id)

    def test_ttl_calculation(self):
        """Test TTL is set to 30 days from now"""
        sample_data = {
            'timestamp': '2026-01-31T12:00:00Z',
            'server_id': 'server-003',
            'metrics': [
                {'metric_type': 'network_in', 'value': 1024.5, 'unit': 'mbps'}
            ]
        }

        items = prepare_dynamodb_items(sample_data)
        current_time = int(datetime.now().timestamp())
        ttl_30_days = 30 * 24 * 60 * 60

        self.assertGreater(items['ttl'], current_time)
        self.assertLess(items['ttl'], current_time + ttl_30_days + 100)

if __name__ == '__main__':
    unittest.main()
