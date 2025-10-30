

import json
import logging
from datetime import datetime
from typing import List, Dict
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== SECURITY EVENT CLASS ====================

class SecurityEvent:
    """Represents a security event in the SIEM system"""
    
    def __init__(self, event_id: str, event_type: str, severity: str, 
                 source_ip: str, destination_ip: str, description: str):
        self.event_id = event_id
        self.event_type = event_type
        self.severity = severity
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.description = description
        self.timestamp = datetime.now().isoformat()
        self.investigated = False
        self.response_actions = []
    
    def to_dict(self):
        """Convert event to dictionary"""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "severity": self.severity,
            "source_ip": self.source_ip,
            "destination_ip": self.destination_ip,
            "description": self.description,
            "timestamp": self.timestamp,
            "investigated": self.investigated,
            "response_actions": self.response_actions
        }
    
    def __repr__(self):
        return f"SecurityEvent({self.event_id}, {self.severity}, {self.event_type})"

# ==================== EVENT LOGGER ====================

class EventLogger:
    """Logs security events to file"""
    
    def __init__(self, log_file="siem_events.log"):
        self.log_file = log_file
    
    def log_event(self, event: SecurityEvent):
        """Log a security event"""
        logger.info(f"EVENT: {event.event_id} | TYPE: {event.event_type} | SEVERITY: {event.severity}")
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(event.to_dict()) + '\n')
    
    def read_logs(self) -> List[Dict]:
        """Read all logged events"""
        events = []
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    events.append(json.loads(line))
        except FileNotFoundError:
            logger.warning("Log file not found")
        return events

# ==================== THREAT DETECTOR ====================

class ThreatDetector:
    """Detects potential threats based on event patterns"""
    
    # Known malicious IPs
    BLACKLISTED_IPS = [
        "192.168.1.100",
        "10.0.0.50",
        "203.0.113.45"
    ]
    
    # Suspicious keywords
    SUSPICIOUS_KEYWORDS = [
        "brute force", "sql injection", "malware", 
        "ransomware", "ddos", "exploit"
    ]
    
    SEVERITY_LEVELS = {
        "critical": 1,
        "high": 2,
        "medium": 3,
        "low": 4
    }
    
    def is_ip_blacklisted(self, ip: str) -> bool:
        """Check if IP is blacklisted"""
        return ip in self.BLACKLISTED_IPS
    
    def is_suspicious_description(self, description: str) -> bool:
        """Check if description contains suspicious keywords"""
        desc_lower = description.lower()
        return any(keyword in desc_lower for keyword in self.SUSPICIOUS_KEYWORDS)
    
    def calculate_threat_score(self, event: SecurityEvent) -> int:
        """Calculate threat score (0-100)"""
        score = 0
        
        # Check blacklist
        if self.is_ip_blacklisted(event.source_ip):
            score += 30
        
        # Check keywords
        if self.is_suspicious_description(event.description):
            score += 25
        
        # Check severity
        severity_score = self.SEVERITY_LEVELS.get(event.severity.lower(), 4)
        score += (5 - severity_score) * 10
        
        return min(score, 100)
    
    def detect_threats(self, events: List[SecurityEvent]) -> List[Dict]:
        """Detect threats from events"""
        threats = []
        for event in events:
            threat_score = self.calculate_threat_score(event)
            if threat_score >= 50:
                threats.append({
                    "event": event.to_dict(),
                    "threat_score": threat_score,
                    "risk_level": "HIGH" if threat_score >= 75 else "MEDIUM"
                })
        return threats

# ==================== INCIDENT RESPONDER ====================

class IncidentResponder:
    """Handles incident response actions"""
    
    RESPONSE_TEMPLATES = {
        "brute_force": [
            "Block source IP",
            "Enable MFA",
            "Reset user passwords",
            "Review access logs"
        ],
        "malware": [
            "Isolate affected system",
            "Scan system with antivirus",
            "Check for data exfiltration",
            "Restore from backup if needed"
        ],
        "ddos": [
            "Activate DDoS protection",
            "Rate limit incoming traffic",
            "Reroute traffic through CDN",
            "Notify ISP"
        ],
        "sql_injection": [
            "Patch vulnerable application",
            "Review database logs",
            "Check for data breach",
            "Implement input validation"
        ]
    }
    
    def generate_response_plan(self, event: SecurityEvent) -> List[str]:
        """Generate response plan based on event type"""
        event_type_lower = event.event_type.lower()
        
        for threat_type, actions in self.RESPONSE_TEMPLATES.items():
            if threat_type in event_type_lower:
                return actions
        
        # Default response
        return [
            "Investigate the incident",
            "Document findings",
            "Notify security team",
            "Monitor for similar events"
        ]
    
    def execute_response(self, event: SecurityEvent) -> bool:
        """Execute incident response"""
        actions = self.generate_response_plan(event)
        
        print(f"\n🚨 INCIDENT RESPONSE PLAN FOR {event.event_id}")
        print("=" * 60)
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action}")
        print("=" * 60)
        
        event.response_actions = actions
        event.investigated = True
        logger.info(f"Response plan executed for {event.event_id}")
        return True

# ==================== SIEM DASHBOARD ====================

class SIEMDashboard:
    """Main SIEM dashboard"""
    
    def __init__(self):
        self.events: List[SecurityEvent] = []
        self.logger = EventLogger()
        self.detector = ThreatDetector()
        self.responder = IncidentResponder()
    
    def add_event(self, event: SecurityEvent):
        """Add security event"""
        self.events.append(event)
        self.logger.log_event(event)
        logger.info(f"Event added: {event.event_id}")
    
    def show_dashboard(self):
        """Display SIEM dashboard"""
        print("\n" + "=" * 80)
        print("🛡️  GWC SIEM DASHBOARD")
        print("=" * 80)
        print(f"Total Events: {len(self.events)}")
        print(f"Critical Events: {len([e for e in self.events if e.severity == 'Critical'])}")
        print(f"Investigated: {len([e for e in self.events if e.investigated])}")
        
        threats = self.detector.detect_threats(self.events)
        print(f"Active Threats: {len(threats)}")
        print("=" * 80 + "\n")
    
    def show_events(self):
        """Show all events"""
        if not self.events:
            print("No events logged yet")
            return
        
        print("\n📋 SECURITY EVENTS")
        print("=" * 80)
        for i, event in enumerate(self.events, 1):
            status = "✅" if event.investigated else "⏳"
            print(f"{i}. {status} {event.event_id} | {event.severity} | {event.event_type}")
            print(f"   From: {event.source_ip} → To: {event.destination_ip}")
            print(f"   {event.description}\n")
        print("=" * 80 + "\n")
    
    def show_threats(self):
        """Show detected threats"""
        threats = self.detector.detect_threats(self.events)
        
        if not threats:
            print("✅ No threats detected")
            return
        
        print("\n⚠️  DETECTED THREATS")
        print("=" * 80)
        for threat in threats:
            event = threat['event']
            print(f"🔴 {event['event_id']}")
            print(f"   Threat Score: {threat['threat_score']}/100 ({threat['risk_level']})")
            print(f"   Type: {event['event_type']}")
            print(f"   Source: {event['source_ip']}\n")
        print("=" * 80 + "\n")
    
    def handle_incident(self, event_id: str):
        """Handle specific incident"""
        for event in self.events:
            if event.event_id == event_id:
                self.responder.execute_response(event)
                return
        print("Event not found")

# ==================== MAIN MENU ====================

def main():
    """Main application loop"""
    dashboard = SIEMDashboard()
    
    print("=" * 80)
    print("🛡️  WELCOME TO GWC SIEM SYSTEM")
    print("Security Information and Event Management")
    print("=" * 80)
    
    while True:
        print("\n📊 MAIN MENU:")
        print("1. Add Security Event")
        print("2. View Dashboard")
        print("3. View All Events")
        print("4. Detect Threats")
        print("5. Handle Incident")
        print("6. Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == '1':
            print("\n➕ ADD SECURITY EVENT")
            event_id = input("Event ID: ").strip()
            event_type = input("Event Type (e.g., Brute Force, SQL Injection, DDoS): ").strip()
            print("Severity: 1.Critical  2.High  3.Medium  4.Low")
            severity_choice = input("Choose severity (1-4): ").strip()
            severity_map = {'1': 'Critical', '2': 'High', '3': 'Medium', '4': 'Low'}
            severity = severity_map.get(severity_choice, 'Medium')
            
            source_ip = input("Source IP: ").strip()
            dest_ip = input("Destination IP: ").strip()
            description = input("Description: ").strip()
            
            event = SecurityEvent(event_id, event_type, severity, source_ip, dest_ip, description)
            dashboard.add_event(event)
        
        elif choice == '2':
            dashboard.show_dashboard()
        
        elif choice == '3':
            dashboard.show_events()
        
        elif choice == '4':
            dashboard.show_threats()
        
        elif choice == '5':
            event_id = input("Enter Event ID to handle: ").strip()
            dashboard.handle_incident(event_id)
        
        elif choice == '6':
            print("\n🛡️  Secure the world! Goodbye! 👋")
            break
        
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
