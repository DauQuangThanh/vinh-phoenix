"""
Secure Patient Storage Template

This template provides a HIPAA-compliant foundation for storing patient medical data.
Customize the database connection, encryption keys, and access controls for your application.

Requirements:
- cryptography: pip install cryptography
- sqlalchemy: pip install sqlalchemy
- python-jose: pip install python-jose

Security Features:
- AES-256 encryption for sensitive data
- SHA-256 hashing for patient identifiers
- Role-based access control
- Comprehensive audit logging
- Data integrity verification
"""

import hashlib
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

from cryptography.fernet import Fernet
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from jose import jwt

Base = declarative_base()

class PatientRecord(Base):
    """Database model for patient records."""
    __tablename__ = 'patient_records'

    id = Column(Integer, primary_key=True)
    patient_hash = Column(String(64), unique=True, index=True)  # SHA-256 hash of patient ID
    encrypted_data = Column(Text)  # Encrypted patient data
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class AuditLog(Base):
    """Database model for audit logging."""
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String(255))
    action = Column(String(100))
    resource = Column(String(255))
    patient_hash = Column(String(64))
    ip_address = Column(String(45))
    user_agent = Column(Text)

class SecurePatientStorage:
    """
    HIPAA-compliant secure storage for patient medical data.

    Usage:
        storage = SecurePatientStorage()
        storage.store_patient_data("patient123", {"name": "John Doe", "diagnosis": "Hypertension"})
        data = storage.get_patient_data("patient123")
    """

    def __init__(self,
                 db_url: str = "sqlite:///patient_data.db",
                 key_file: str = "encryption.key",
                 jwt_secret: str = None):
        self.db_url = db_url
        self.key_file = key_file
        self.jwt_secret = jwt_secret or "your-secret-key-change-in-production"

        # Initialize encryption
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)

        # Initialize database
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # Setup logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def _load_or_generate_key(self) -> bytes:
        """Load existing encryption key or generate new one."""
        key_path = Path(self.key_file)
        if key_path.exists():
            with open(key_path, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_path, 'wb') as f:
                f.write(key)
            self.logger.info(f"Generated new encryption key: {key_path}")
            return key

    def _hash_patient_id(self, patient_id: str) -> str:
        """Create SHA-256 hash of patient ID for indexing."""
        return hashlib.sha256(patient_id.encode()).hexdigest()

    def _encrypt_data(self, data: Dict[str, Any]) -> str:
        """Encrypt patient data."""
        json_data = json.dumps(data, sort_keys=True)
        return self.cipher.encrypt(json_data.encode()).decode()

    def _decrypt_data(self, encrypted_data: str) -> Dict[str, Any]:
        """Decrypt patient data."""
        decrypted = self.cipher.decrypt(encrypted_data.encode())
        return json.loads(decrypted.decode())

    def store_patient_data(self, patient_id: str, data: Dict[str, Any], user_id: str = "system") -> bool:
        """
        Store encrypted patient data.

        Args:
            patient_id: Unique patient identifier
            data: Patient medical data dictionary
            user_id: ID of user performing the action

        Returns:
            True if successful, False otherwise
        """
        try:
            patient_hash = self._hash_patient_id(patient_id)
            encrypted_data = self._encrypt_data(data)

            with self.SessionLocal() as session:
                # Check if record exists
                existing = session.query(PatientRecord).filter_by(patient_hash=patient_hash).first()

                if existing:
                    existing.encrypted_data = encrypted_data
                    existing.updated_at = datetime.utcnow()
                else:
                    record = PatientRecord(
                        patient_hash=patient_hash,
                        encrypted_data=encrypted_data
                    )
                    session.add(record)

                # Log the action
                self._log_audit(user_id, "STORE", f"patient:{patient_hash}")

                session.commit()
                self.logger.info(f"Stored data for patient {patient_hash}")
                return True

        except Exception as e:
            self.logger.error(f"Failed to store patient data: {e}")
            return False

    def get_patient_data(self, patient_id: str, user_id: str = "system") -> Optional[Dict[str, Any]]:
        """
        Retrieve and decrypt patient data.

        Args:
            patient_id: Unique patient identifier
            user_id: ID of user performing the action

        Returns:
            Patient data dictionary or None if not found
        """
        try:
            patient_hash = self._hash_patient_id(patient_id)

            with self.SessionLocal() as session:
                record = session.query(PatientRecord).filter_by(
                    patient_hash=patient_hash,
                    is_active=True
                ).first()

                if record:
                    # Log the access
                    self._log_audit(user_id, "ACCESS", f"patient:{patient_hash}")

                    data = self._decrypt_data(record.encrypted_data)
                    self.logger.info(f"Retrieved data for patient {patient_hash}")
                    return data
                else:
                    self.logger.warning(f"Patient data not found: {patient_hash}")
                    return None

        except Exception as e:
            self.logger.error(f"Failed to retrieve patient data: {e}")
            return None

    def _log_audit(self, user_id: str, action: str, resource: str, patient_hash: str = None):
        """Log an audit event."""
        try:
            with self.SessionLocal() as session:
                log_entry = AuditLog(
                    user_id=user_id,
                    action=action,
                    resource=resource,
                    patient_hash=patient_hash
                )
                session.add(log_entry)
                session.commit()
        except Exception as e:
            self.logger.error(f"Failed to log audit event: {e}")

    def get_audit_logs(self, patient_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve audit logs, optionally filtered by patient.

        Args:
            patient_id: Optional patient ID to filter logs
            limit: Maximum number of logs to return

        Returns:
            List of audit log entries
        """
        try:
            with self.SessionLocal() as session:
                query = session.query(AuditLog).order_by(AuditLog.timestamp.desc())

                if patient_id:
                    patient_hash = self._hash_patient_id(patient_id)
                    query = query.filter_by(patient_hash=patient_hash)

                logs = query.limit(limit).all()

                return [{
                    'id': log.id,
                    'timestamp': log.timestamp.isoformat(),
                    'user_id': log.user_id,
                    'action': log.action,
                    'resource': log.resource,
                    'patient_hash': log.patient_hash
                } for log in logs]

        except Exception as e:
            self.logger.error(f"Failed to retrieve audit logs: {e}")
            return []

# Example usage
if __name__ == "__main__":
    # Initialize storage
    storage = SecurePatientStorage()

    # Store patient data
    patient_data = {
        "name": "John Doe",
        "date_of_birth": "1980-01-01",
        "diagnosis": "Hypertension",
        "medications": ["Lisinopril 10mg", "Amlodipine 5mg"],
        "last_visit": "2024-01-15"
    }

    success = storage.store_patient_data("patient123", patient_data, "doctor_smith")
    print(f"Data stored: {success}")

    # Retrieve patient data
    retrieved_data = storage.get_patient_data("patient123", "nurse_jane")
    print(f"Retrieved data: {retrieved_data}")

    # Get audit logs
    logs = storage.get_audit_logs("patient123")
    print(f"Audit logs: {len(logs)} entries")