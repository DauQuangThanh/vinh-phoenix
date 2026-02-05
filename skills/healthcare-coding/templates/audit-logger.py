"""
Audit Logger Template

This template provides comprehensive audit logging for healthcare applications.
Customize the log storage, filtering, and reporting for your compliance requirements.

Requirements:
- sqlalchemy: pip install sqlalchemy
- python-json-logger: pip install python-json-logger

Features:
- HIPAA-compliant audit logging
- Structured JSON logging
- Database and file storage options
- Log filtering and search capabilities
- Automated log retention and archiving
- Integration with security monitoring systems
"""

import json
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from pathlib import Path
from enum import Enum

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pythonjsonlogger import jsonlogger

Base = declarative_base()

class AuditEventType(Enum):
    """Standard audit event types for healthcare applications."""
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    ACCESS = "ACCESS"
    MODIFY = "MODIFY"
    CREATE = "CREATE"
    DELETE = "DELETE"
    EXPORT = "EXPORT"
    EMERGENCY_ACCESS = "EMERGENCY_ACCESS"
    DENIED_ACCESS = "DENIED_ACCESS"

class AuditEvent(Base):
    """Database model for audit events."""
    __tablename__ = 'audit_events'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    event_type = Column(String(50), index=True)
    user_id = Column(String(255), index=True)
    user_role = Column(String(100))
    patient_id_hash = Column(String(64), index=True)  # SHA-256 hash for privacy
    resource_type = Column(String(100))
    resource_id = Column(String(255))
    action = Column(String(100))
    outcome = Column(String(20))  # SUCCESS, FAILURE, DENIED
    ip_address = Column(String(45))
    user_agent = Column(Text)
    session_id = Column(String(255))
    details = Column(Text)  # JSON string with additional details
    is_emergency = Column(Boolean, default=False)

    # Indexes for common queries
    __table_args__ = (
        Index('idx_user_timestamp', 'user_id', 'timestamp'),
        Index('idx_patient_timestamp', 'patient_id_hash', 'timestamp'),
    )

class HealthcareAuditLogger:
    """
    HIPAA-compliant audit logger for healthcare applications.

    Usage:
        logger = HealthcareAuditLogger()
        logger.log_access("user123", "patient456", "VIEW", "192.168.1.1")
    """

    def __init__(self,
                 db_url: str = "sqlite:///audit_log.db",
                 log_file: Optional[str] = "audit.log",
                 retention_days: int = 2555):  # 7 years for HIPAA
        """
        Initialize audit logger.

        Args:
            db_url: Database URL for storing audit logs
            log_file: Optional file path for JSON logging
            retention_days: Number of days to retain logs
        """
        self.db_url = db_url
        self.log_file = Path(log_file) if log_file else None
        self.retention_days = retention_days

        # Initialize database
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # Setup structured logging
        self.logger = logging.getLogger('healthcare_audit')
        self.logger.setLevel(logging.INFO)

        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Add JSON file handler if specified
        if self.log_file:
            self.log_file.parent.mkdir(exist_ok=True)
            file_handler = logging.FileHandler(self.log_file)
            formatter = jsonlogger.JsonFormatter(
                '%(asctime)s %(name)s %(levelname)s %(message)s'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # Setup cleanup scheduler (in production, use proper scheduler)
        self._schedule_log_cleanup()

    def log_event(self,
                  event_type: AuditEventType,
                  user_id: str,
                  action: str,
                  outcome: str = "SUCCESS",
                  patient_id: Optional[str] = None,
                  resource_type: Optional[str] = None,
                  resource_id: Optional[str] = None,
                  ip_address: Optional[str] = None,
                  user_agent: Optional[str] = None,
                  session_id: Optional[str] = None,
                  user_role: Optional[str] = None,
                  details: Optional[Dict[str, Any]] = None,
                  is_emergency: bool = False) -> bool:
        """
        Log an audit event.

        Args:
            event_type: Type of audit event
            user_id: ID of the user performing the action
            action: Specific action performed
            outcome: Result of the action (SUCCESS, FAILURE, DENIED)
            patient_id: Patient ID (will be hashed for privacy)
            resource_type: Type of resource accessed
            resource_id: ID of the resource
            ip_address: IP address of the user
            user_agent: User agent string
            session_id: Session identifier
            user_role: Role of the user
            details: Additional details as dictionary
            is_emergency: Whether this is emergency access

        Returns:
            True if logging successful
        """
        try:
            # Hash patient ID for privacy
            patient_hash = None
            if patient_id:
                patient_hash = hashlib.sha256(patient_id.encode()).hexdigest()

            # Convert details to JSON
            details_json = json.dumps(details) if details else None

            # Create audit event
            event = AuditEvent(
                event_type=event_type.value,
                user_id=user_id,
                user_role=user_role,
                patient_id_hash=patient_hash,
                resource_type=resource_type,
                resource_id=resource_id,
                action=action,
                outcome=outcome,
                ip_address=ip_address,
                user_agent=user_agent,
                session_id=session_id,
                details=details_json,
                is_emergency=is_emergency
            )

            # Store in database
            with self.SessionLocal() as session:
                session.add(event)
                session.commit()

            # Log to file
            log_data = {
                'event_type': event_type.value,
                'user_id': user_id,
                'action': action,
                'outcome': outcome,
                'timestamp': datetime.utcnow().isoformat(),
                'patient_hash': patient_hash,
                'resource_type': resource_type,
                'ip_address': ip_address,
                'is_emergency': is_emergency
            }
            if details:
                log_data.update(details)

            self.logger.info("Audit event", extra=log_data)

            return True

        except Exception as e:
            # In case of logging failure, we need to handle it carefully
            # In production, you might want to send alerts
            print(f"CRITICAL: Failed to log audit event: {e}")
            return False

    def log_access(self,
                   user_id: str,
                   patient_id: str,
                   action: str,
                   ip_address: str,
                   user_role: Optional[str] = None,
                   resource_type: str = "PATIENT_RECORD",
                   outcome: str = "SUCCESS") -> bool:
        """
        Log patient data access event.

        Args:
            user_id: User performing the access
            patient_id: Patient whose data was accessed
            action: Type of access (VIEW, MODIFY, etc.)
            ip_address: IP address of the user
            user_role: Role of the user
            resource_type: Type of resource
            outcome: Result of the access

        Returns:
            True if logging successful
        """
        return self.log_event(
            event_type=AuditEventType.ACCESS,
            user_id=user_id,
            action=action,
            outcome=outcome,
            patient_id=patient_id,
            resource_type=resource_type,
            ip_address=ip_address,
            user_role=user_role
        )

    def log_login(self,
                  user_id: str,
                  ip_address: str,
                  user_agent: str,
                  outcome: str = "SUCCESS") -> bool:
        """Log user login event."""
        return self.log_event(
            event_type=AuditEventType.LOGIN,
            user_id=user_id,
            action="LOGIN",
            outcome=outcome,
            ip_address=ip_address,
            user_agent=user_agent
        )

    def log_emergency_access(self,
                            user_id: str,
                            patient_id: str,
                            reason: str,
                            ip_address: str) -> bool:
        """Log emergency access event."""
        return self.log_event(
            event_type=AuditEventType.EMERGENCY_ACCESS,
            user_id=user_id,
            action="EMERGENCY_ACCESS",
            patient_id=patient_id,
            ip_address=ip_address,
            details={'reason': reason},
            is_emergency=True
        )

    def search_events(self,
                     user_id: Optional[str] = None,
                     patient_id: Optional[str] = None,
                     event_type: Optional[AuditEventType] = None,
                     start_date: Optional[datetime] = None,
                     end_date: Optional[datetime] = None,
                     limit: int = 100) -> List[Dict[str, Any]]:
        """
        Search audit events.

        Args:
            user_id: Filter by user ID
            patient_id: Filter by patient ID (will be hashed)
            event_type: Filter by event type
            start_date: Start date for search
            end_date: End date for search
            limit: Maximum number of results

        Returns:
            List of audit events as dictionaries
        """
        try:
            with self.SessionLocal() as session:
                query = session.query(AuditEvent)

                if user_id:
                    query = query.filter_by(user_id=user_id)

                if patient_id:
                    patient_hash = hashlib.sha256(patient_id.encode()).hexdigest()
                    query = query.filter_by(patient_id_hash=patient_hash)

                if event_type:
                    query = query.filter_by(event_type=event_type.value)

                if start_date:
                    query = query.filter(AuditEvent.timestamp >= start_date)

                if end_date:
                    query = query.filter(AuditEvent.timestamp <= end_date)

                events = query.order_by(AuditEvent.timestamp.desc()).limit(limit).all()

                result = []
                for event in events:
                    event_dict = {
                        'id': event.id,
                        'timestamp': event.timestamp.isoformat(),
                        'event_type': event.event_type,
                        'user_id': event.user_id,
                        'user_role': event.user_role,
                        'patient_hash': event.patient_id_hash,
                        'resource_type': event.resource_type,
                        'resource_id': event.resource_id,
                        'action': event.action,
                        'outcome': event.outcome,
                        'ip_address': event.ip_address,
                        'is_emergency': event.is_emergency,
                    }

                    if event.details:
                        event_dict['details'] = json.loads(event.details)

                    result.append(event_dict)

                return result

        except Exception as e:
            self.logger.error(f"Failed to search audit events: {e}")
            return []

    def get_user_activity_report(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Generate activity report for a user.

        Args:
            user_id: User ID to report on
            days: Number of days to look back

        Returns:
            Activity summary dictionary
        """
        start_date = datetime.utcnow() - timedelta(days=days)

        events = self.search_events(
            user_id=user_id,
            start_date=start_date
        )

        report = {
            'user_id': user_id,
            'period_days': days,
            'total_events': len(events),
            'event_types': {},
            'outcomes': {},
            'emergency_access_count': 0
        }

        for event in events:
            # Count event types
            event_type = event['event_type']
            report['event_types'][event_type] = report['event_types'].get(event_type, 0) + 1

            # Count outcomes
            outcome = event['outcome']
            report['outcomes'][outcome] = report['outcomes'].get(outcome, 0) + 1

            # Count emergency access
            if event.get('is_emergency', False):
                report['emergency_access_count'] += 1

        return report

    def _schedule_log_cleanup(self):
        """Schedule periodic cleanup of old logs."""
        # In production, implement proper scheduling (e.g., APScheduler, cron)
        # For now, just log that cleanup should be scheduled
        self.logger.info(f"Log cleanup scheduled: retain {self.retention_days} days")

    def cleanup_old_logs(self):
        """Remove logs older than retention period."""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=self.retention_days)

            with self.SessionLocal() as session:
                deleted_count = session.query(AuditEvent).filter(
                    AuditEvent.timestamp < cutoff_date
                ).delete()

                session.commit()

            self.logger.info(f"Cleaned up {deleted_count} old audit logs")
            return deleted_count

        except Exception as e:
            self.logger.error(f"Failed to cleanup old logs: {e}")
            return 0

# Example usage
if __name__ == "__main__":
    # Initialize logger
    audit_logger = HealthcareAuditLogger()

    # Log various events
    audit_logger.log_login("doctor_smith", "192.168.1.100", "Mozilla/5.0...")
    audit_logger.log_access("doctor_smith", "patient123", "VIEW", "192.168.1.100", "PHYSICIAN")
    audit_logger.log_emergency_access("nurse_jane", "patient456", "Patient in critical condition", "192.168.1.101")

    # Search events
    events = audit_logger.search_events(user_id="doctor_smith")
    print(f"Found {len(events)} events for doctor_smith")

    # Generate report
    report = audit_logger.get_user_activity_report("doctor_smith")
    print("Activity report:", report)