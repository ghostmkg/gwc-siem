
import unittest
from datetime import datetime
from app.models import Event
from app.detector import GeoIPBlocklistDetector

class TestGeoIPBlocklistDetector(unittest.TestCase):

    def test_blocklisted_ip(self):
        # Arrange
        detector = GeoIPBlocklistDetector()
        event = Event(
            timestamp=datetime.now(),
            source_ip="1.2.3.4",  # This IP is in the hardcoded blocklist
            message="Any message",
            raw_log="Any raw log"
        )

        # Act
        alerts = detector.detect([event])

        # Assert
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].rule_name, "GeoIP Blocklist")
        self.assertEqual(alerts[0].source_ip, "1.2.3.4")

    def test_non_blocklisted_ip(self):
        # Arrange
        detector = GeoIPBlocklistDetector()
        event = Event(
            timestamp=datetime.now(),
            source_ip="100.100.100.100",  # This IP is not in the blocklist
            message="Any message",
            raw_log="Any raw log"
        )

        # Act
        alerts = detector.detect([event])

        # Assert
        self.assertEqual(len(alerts), 0)

if __name__ == '__main__':
    unittest.main()
