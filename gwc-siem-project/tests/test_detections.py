
import unittest
from datetime import datetime, timedelta
from core.detections.brute_force import detect_brute_force
from core.detections.http_5xx_burst import detect_http_5xx_burst

class TestBruteForceDetection(unittest.TestCase):

    def test_detect_brute_force(self):
        events = [
            {'timestamp': datetime(2023, 1, 1, 12, 0, 0), 'process': 'sshd', 'message': 'Failed password for invalid user user from 1.1.1.1 port 12345 ssh2'},
            {'timestamp': datetime(2023, 1, 1, 12, 1, 0), 'process': 'sshd', 'message': 'Failed password for invalid user user from 1.1.1.1 port 12345 ssh2'},
            {'timestamp': datetime(2023, 1, 1, 12, 2, 0), 'process': 'sshd', 'message': 'Failed password for invalid user user from 1.1.1.1 port 12345 ssh2'},
            {'timestamp': datetime(2023, 1, 1, 12, 3, 0), 'process': 'sshd', 'message': 'Failed password for invalid user user from 1.1.1.1 port 12345 ssh2'},
            {'timestamp': datetime(2023, 1, 1, 12, 4, 0), 'process': 'sshd', 'message': 'Failed password for invalid user user from 1.1.1.1 port 12345 ssh2'},
        ]
        alerts = detect_brute_force(events)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]['type'], 'brute_force')
        self.assertEqual(alerts[0]['ip'], '1.1.1.1')

    def test_detect_brute_force_no_attack(self):
        events = [
            {'timestamp': datetime(2023, 1, 1, 12, 0, 0), 'process': 'sshd', 'message': 'Failed password for invalid user user from 1.1.1.1 port 12345 ssh2'},
            {'timestamp': datetime(2023, 1, 1, 12, 1, 0), 'process': 'sshd', 'message': 'Failed password for invalid user user from 1.1.1.1 port 12345 ssh2'},
            {'timestamp': datetime(2023, 1, 1, 12, 6, 0), 'process': 'sshd', 'message': 'Failed password for invalid user user from 1.1.1.1 port 12345 ssh2'},
        ]
        alerts = detect_brute_force(events)
        self.assertEqual(len(alerts), 0)


class TestHttp5xxBurstDetection(unittest.TestCase):

    def test_detect_http_5xx_burst(self):
        events = [
            {'timestamp': datetime(2023, 1, 1, 12, 0, 0), 'ip': '1.1.1.1', 'status': 500},
            {'timestamp': datetime(2023, 1, 1, 12, 0, 10), 'ip': '1.1.1.1', 'status': 502},
            {'timestamp': datetime(2023, 1, 1, 12, 0, 20), 'ip': '1.1.1.1', 'status': 503},
            {'timestamp': datetime(2023, 1, 1, 12, 0, 30), 'ip': '1.1.1.1', 'status': 500},
            {'timestamp': datetime(2023, 1, 1, 12, 0, 40), 'ip': '1.1.1.1', 'status': 500},
            {'timestamp': datetime(2023, 1, 1, 12, 0, 50), 'ip': '1.1.1.1', 'status': 500},
            {'timestamp': datetime(2023, 1, 1, 12, 1, 0), 'ip': '1.1.1.1', 'status': 500},
            {'timestamp': datetime(2023, 1, 1, 12, 1, 10), 'ip': '1.1.1.1', 'status': 500},
            {'timestamp': datetime(2023, 1, 1, 12, 1, 20), 'ip': '1.1.1.1', 'status': 500},
            {'timestamp': datetime(2023, 1, 1, 12, 0, 59), 'ip': '1.1.1.1', 'status': 500},
        ]
        events.sort(key=lambda x: x['timestamp'])
        alerts = detect_http_5xx_burst(events)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]['type'], 'http_5xx_burst')
        self.assertEqual(alerts[0]['ip'], '1.1.1.1')

    def test_detect_http_5xx_burst_no_attack(self):
        events = [
            {'timestamp': datetime(2023, 1, 1, 12, 0, 0), 'ip': '1.1.1.1', 'status': 200},
            {'timestamp': datetime(2023, 1, 1, 12, 1, 0), 'ip': '1.1.1.1', 'status': 200},
            {'timestamp': datetime(2023, 1, 1, 12, 6, 0), 'ip': '1.1.1.1', 'status': 500},
        ]
        alerts = detect_http_5xx_burst(events)
        self.assertEqual(len(alerts), 0)

if __name__ == '__main__':
    unittest.main()
