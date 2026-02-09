
import unittest
import json
import os
from unittest.mock import patch, MagicMock, call
from decimal import Decimal
import lambda_function

class TestLogProcessor(unittest.TestCase):
    """Unit tests for log-processor Lambda function"""
    
    def setUp(self):
        """Set up test fixtures"""
        os.environ['DYNAMODB_TABLE'] = 'InfraMetrics'
        os.environ['AWS_REGION'] = 'us-east-1'
        
        self.sample_metric = {
            'metric_id': 'test-123',
            'timestamp': 1738675200,
            'metric_type': 'cpu_utilization',
            'value': 75.5,
            'unit': 'percent',
            'hostname': 'server-001',
            'region': 'us-east-1',
            'environment': 'production'
        }
        
        self.sample_s3_event = {
            'Records': [
                {
                    'eventName': 'ObjectCreated:Put',
                    's3': {
                        'bucket': {'name': 'test-bucket'},
                        'object': {'key': 'metrics/test.json'}
                    }
                }
            ]
        }
    
    def test_validate_metrics_valid(self):
        """Test validation of valid metrics"""
        metrics = [self.sample_metric]
        validated = lambda_function.validate_metrics(metrics)
        
        self.assertEqual(len(validated), 1)
        self.assertEqual(validated[0]['metric_id'], 'test-123')
        self.assertEqual(validated[0]['timestamp'], 1738675200)
        self.assertEqual(validated[0]['value'], 75.5)
    
    def test_validate_metrics_missing_fields(self):
        """Test validation filters out metrics with missing required fields"""
        invalid_metric = {'metric_id': 'test-123'}  # Missing required fields
        metrics = [invalid_metric, self.sample_metric]
        
        validated = lambda_function.validate_metrics(metrics)
        
        self.assertEqual(len(validated), 1)  # Only valid metric passes
        self.assertEqual(validated[0]['metric_id'], 'test-123')
    
    def test_validate_metrics_invalid_types(self):
        """Test validation filters out metrics with invalid data types"""
        invalid_metric = self.sample_metric.copy()
        invalid_metric['timestamp'] = 'not-a-number'
        metrics = [invalid_metric, self.sample_metric]
        
        validated = lambda_function.validate_metrics(metrics)
        
        self.assertEqual(len(validated), 1)  # Only valid metric passes
    
    def test_prepare_dynamodb_item(self):
        """Test DynamoDB item preparation"""
        item = lambda_function.prepare_dynamodb_item(self.sample_metric)
        
        self.assertEqual(item['metric_id'], 'test-123')
        self.assertEqual(item['timestamp'], 1738675200)
        self.assertEqual(item['metric_type'], 'cpu_utilization')
        self.assertIsInstance(item['value'], Decimal)
        self.assertEqual(float(item['value']), 75.5)
        self.assertIn('ttl', item)
        self.assertGreater(item['ttl'], 1738675200)
    
    @patch('lambda_function.s3_client')
    def test_download_and_parse_json_success(self, mock_s3):
        """Test successful JSON download and parsing"""
        mock_response = {
            'Body': MagicMock(read=lambda: json.dumps([self.sample_metric]).encode('utf-8'))
        }
        mock_s3.get_object.return_value = mock_response
        
        metrics = lambda_function.download_and_parse_json('test-bucket', 'test.json')
        
        self.assertEqual(len(metrics), 1)
        self.assertEqual(metrics[0]['metric_id'], 'test-123')
        mock_s3.get_object.assert_called_once_with(Bucket='test-bucket', Key='test.json')
    
    @patch('lambda_function.s3_client')
    def test_download_and_parse_json_invalid_json(self, mock_s3):
        """Test handling of invalid JSON"""
        mock_response = {
            'Body': MagicMock(read=lambda: b'invalid json{')
        }
        mock_s3.get_object.return_value = mock_response
        
        with self.assertRaises(json.JSONDecodeError):
            lambda_function.download_and_parse_json('test-bucket', 'test.json')
    
    @patch('lambda_function.table')
    def test_write_to_dynamodb_batch_success(self, mock_table):
        """Test successful batch write to DynamoDB"""
        metrics = [self.sample_metric] * 3
        mock_batch_writer = MagicMock()
        mock_table.batch_writer.return_value.__enter__.return_value = mock_batch_writer
        
        success, failure = lambda_function.write_to_dynamodb_batch(metrics)
        
        self.assertEqual(success, 3)
        self.assertEqual(failure, 0)
        self.assertEqual(mock_batch_writer.put_item.call_count, 3)
    
    @patch('lambda_function.table')
    @patch('lambda_function.time.sleep')
    def test_write_to_dynamodb_batch_throttling(self, mock_sleep, mock_table):
        """Test retry logic on DynamoDB throttling"""
        from botocore.exceptions import ClientError
        
        metrics = [self.sample_metric]
        
        # Simulate throttling on first attempt, success on second
        mock_batch_writer = MagicMock()
        mock_batch_writer.put_item.side_effect = [
            ClientError(
                {'Error': {'Code': 'ProvisionedThroughputExceededException'}},
                'BatchWriteItem'
            ),
            None  # Success on retry
        ]
        mock_table.batch_writer.return_value.__enter__.return_value = mock_batch_writer
        
        success, failure = lambda_function.write_to_dynamodb_batch(metrics)
        
        # Should retry and eventually succeed
        mock_sleep.assert_called()  # Verify backoff was used
    
    @patch('lambda_function.cloudwatch')
    def test_publish_processing_metrics(self, mock_cloudwatch):
        """Test CloudWatch metrics publishing"""
        summary = {
            'total_files': 1,
            'total_metrics': 50,
            'successful_writes': 48,
            'failed_writes': 2
        }
        
        lambda_function.publish_processing_metrics(summary)
        
        mock_cloudwatch.put_metric_data.assert_called_once()
        call_args = mock_cloudwatch.put_metric_data.call_args
        
        self.assertEqual(call_args[1]['Namespace'], 'InfraMonitoring/Pipeline')
        self.assertEqual(len(call_args[1]['MetricData']), 4)
    
    @patch('lambda_function.process_s3_record')
    @patch('lambda_function.publish_processing_metrics')
    def test_lambda_handler_success(self, mock_publish, mock_process):
        """Test successful Lambda handler execution"""
        mock_process.return_value = None
        
        response = lambda_function.lambda_handler(self.sample_s3_event, None)
        
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('message', response)
        mock_process.assert_called_once()
        mock_publish.assert_called_once()
    
    def test_lambda_handler_no_records(self):
        """Test Lambda handler with empty event"""
        empty_event = {'Records': []}
        
        response = lambda_function.lambda_handler(empty_event, None)
        
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('No S3 records', response['message'])
    
    def test_create_response(self):
        """Test response creation"""
        response = lambda_function.create_response(200, 'Success', {'count': 10})
        
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['message'], 'Success')
        self.assertEqual(response['data']['count'], 10)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)

