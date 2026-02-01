import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path to import lambda function
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../lambda/data-collector')))

import lambda_function

class TestDataCollector(unittest.TestCase):
    """Unit tests for data collector Lambda function"""

    def test_generate_metric_cpu(self):
        """Test CPU metric generation"""
        metric = lambda_function.generate_metric('cpu', 'host-001', 1738440000)

        self.assertEqual(metric['metric_type'], 'cpu')
        self.assertEqual(metric['host_id'], 'host-001')
        self.assertEqual(metric['timestamp'], 1738440000)
        self.assertGreaterEqual(metric['value'], 10.0)
        self.assertLessEqual(metric['value'], 95.0)
        self.assertIn('metric_id', metric)
        self.assertIn('ttl', metric)

    def test_generate_metric_memory(self):
        """Test memory metric generation"""
        metric = lambda_function.generate_metric('memory', 'host-002', 1738440000)

        self.assertEqual(metric['metric_type'], 'memory')
        self.assertGreaterEqual(metric['value'], 20.0)
        self.assertLessEqual(metric['value'], 90.0)

    def test_generate_metrics_batch(self):
        """Test batch metric generation"""
        metrics = lambda_function.generate_metrics_batch()

        # Should generate 5 hosts × 4 metric types = 20 metrics
        self.assertEqual(len(metrics), 20)

        # Verify all metric types are present
        metric_types = set(m['metric_type'] for m in metrics)
        self.assertEqual(metric_types, {'cpu', 'memory', 'disk', 'network'})

        # Verify all hosts are present
        host_ids = set(m['host_id'] for m in metrics)
        self.assertEqual(len(host_ids), 5)

    @patch('lambda_function.s3_client')
    def test_upload_to_s3(self, mock_s3):
        """Test S3 upload functionality"""
        metrics = [{'metric_id': 'test-001', 'value': 50.0}]
        timestamp = 1738440000

        s3_key = lambda_function.upload_to_s3(metrics, timestamp)

        # Verify S3 client was called
        mock_s3.put_object.assert_called_once()

        # Verify filename format
        self.assertIn('metrics/', s3_key)
        self.assertIn('.json', s3_key)

    @patch('lambda_function.upload_to_s3')
    @patch('lambda_function.generate_metrics_batch')
    def test_lambda_handler_success(self, mock_generate, mock_upload):
        """Test successful Lambda execution"""
        # Mock return values
        mock_generate.return_value = [{'metric_id': 'test-001'}]
        mock_upload.return_value = 'metrics/2026/02/03/metrics-1738440000.json'

        # Call handler
        result = lambda_function.lambda_handler({}, None)

        # Verify success response
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('message', result['body'])

if __name__ == '__main__':
    unittest.main()