
import unittest
from datetime import datetime, timezone, timedelta
from core.parsers.apache import parse_apache_log

class TestApacheParser(unittest.TestCase):

    def test_parse_apache_log(self):
        log_line = '127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326'
        expected_data = {
            'ip': '127.0.0.1',
            'timestamp': datetime(2000, 10, 10, 13, 55, 36, tzinfo=timezone(timedelta(hours=-7))),
            'method': 'GET',
            'url': '/apache_pb.gif',
            'status': 200,
            'size': 2326
        }
        self.assertEqual(parse_apache_log(log_line), expected_data)

    def test_parse_apache_log_with_no_size(self):
        log_line = '127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 -'
        expected_data = {
            'ip': '127.0.0.1',
            'timestamp': datetime(2000, 10, 10, 13, 55, 36, tzinfo=timezone(timedelta(hours=-7))),
            'method': 'GET',
            'url': '/apache_pb.gif',
            'status': 200,
            'size': 0
        }
        self.assertEqual(parse_apache_log(log_line), expected_data)

    def test_parse_apache_log_invalid_line(self):
        log_line = 'invalid log line'
        self.assertIsNone(parse_apache_log(log_line))

if __name__ == '__main__':
    unittest.main()
