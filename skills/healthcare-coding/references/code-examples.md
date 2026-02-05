# Healthcare Code Examples and Implementation Patterns

This document provides detailed code examples and implementation patterns for common healthcare application scenarios.

## Secure Patient Data Storage (Python)

### Complete Implementation

```python
import hashlib
import os
from cryptography.fernet import Fernet
from typing import Dict, Any, Optional
import logging
import json
from datetime import datetime
from pathlib import Path

class SecurePatientStorage:
    """
    HIPAA-compliant secure storage for patient medical data.
    
    Features:
    - AES-256 encryption for data at rest
    - SHA-256 hashing for patient ID indexing
    - Comprehensive audit logging
    - Role-based access control
    - Data integrity verification
    """
    
    def __init__(self, key_file: Optional[str] = None, db_path: str = "patient_data.db"):
        self.key_file = key_file or "encryption.key"
        self.db_path = Path(db_path)
        self.db_path.mkdir(exist_ok=True)
        
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)
        self.logger = logging.getLogger(__name__)
        
        # Initialize audit log
        self.audit_log = []
        
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
            return key
    
    def encrypt_patient_data(self, patient_id: str, medical_data: Dict[str, Any]) -> str:
        """
        Encrypt patient medical data with audit logging.
        
        Args:
            patient_id: Unique patient identifier (e.g., SSN, MRN)
            medical_data: Dictionary containing medical information
            
        Returns:
            Hashed patient ID for storage reference
            
        Raises:
            ValueError: If patient_id or medical_data is invalid
        """
        if not patient_id or not medical_data:
            raise ValueError("Patient ID and medical data are required")
        
        # Hash patient ID for privacy-preserving indexing
        hashed_id = hashlib.sha256(patient_id.encode()).hexdigest()
        
        # Add metadata
        data_with_metadata = {
            "data": medical_data,
            "created_at": datetime.utcnow().isoformat(),
            "version": "1.0",
            "hash": hashed_id
        }
        
        # Convert to JSON and encrypt
        data_str = json.dumps(data_with_metadata, sort_keys=True)
        encrypted_data = self.cipher.encrypt(data_str.encode())
        
        # Store with audit trail
        self._store_with_audit(hashed_id, encrypted_data)
        
        # Log the encryption event
        self._log_audit_event("ENCRYPT", hashed_id, "Patient data encrypted")
        
        return hashed_id
    
    def decrypt_patient_data(self, hashed_id: str) -> Dict[str, Any]:
        """
        Decrypt and retrieve patient medical data.
        
        Args:
            hashed_id: Hashed patient identifier
            
        Returns:
            Decrypted medical data dictionary
            
        Raises:
            PermissionError: If access is denied
            ValueError: If data is corrupted or not found
        """
        # Verify access permissions (HIPAA compliance)
        if not self._check_access_permissions(hashed_id):
            self._log_audit_event("ACCESS_DENIED", hashed_id, "Unauthorized access attempt")
            raise PermissionError("Unauthorized access to patient data")
        
        encrypted_data = self._retrieve_data(hashed_id)
        if not encrypted_data:
            raise ValueError(f"Patient data not found for ID: {hashed_id[:8]}...")
        
        try:
            decrypted_data = self.cipher.decrypt(encrypted_data).decode()
            data_with_metadata = json.loads(decrypted_data)
            
            # Verify data integrity
            if data_with_metadata.get("hash") != hashed_id:
                raise ValueError("Data integrity check failed")
            
            # Log successful access
            self._log_audit_event("DECRYPT", hashed_id, "Patient data accessed")
            
            return data_with_metadata["data"]
        except Exception as e:
            self._log_audit_event("DECRYPT_FAILED", hashed_id, f"Decryption failed: {str(e)}")
            raise ValueError("Failed to decrypt patient data")
    
    def _store_with_audit(self, hashed_id: str, encrypted_data: bytes) -> None:
        """Store encrypted data with audit logging."""
        data_file = self.db_path / f"{hashed_id}.enc"
        with open(data_file, 'wb') as f:
            f.write(encrypted_data)
    
    def _retrieve_data(self, hashed_id: str) -> Optional[bytes]:
        """Retrieve encrypted data from storage."""
        data_file = self.db_path / f"{hashed_id}.enc"
        if data_file.exists():
            with open(data_file, 'rb') as f:
                return f.read()
        return None
    
    def _check_access_permissions(self, hashed_id: str) -> bool:
        """
        Check if current user has access permissions.
        
        In a real implementation, this would:
        - Check user authentication and authorization
        - Verify role-based permissions (doctor, nurse, admin)
        - Check patient consent status
        - Validate emergency access if applicable
        """
        current_user = self._get_current_user()
        if not current_user:
            return False
            
        patient_consent = self._check_patient_consent(hashed_id)
        user_permissions = self._get_user_permissions(current_user, hashed_id)
        
        return patient_consent and user_permissions
    
    def _get_current_user(self) -> Optional[str]:
        """Get current authenticated user ID."""
        return os.getenv("CURRENT_USER_ID")
    
    def _check_patient_consent(self, hashed_id: str) -> bool:
        """Check if patient has consented to data access."""
        # In a real app, this would check a consent database
        return True  # Placeholder
    
    def _get_user_permissions(self, user_id: str, hashed_id: str) -> bool:
        """Check user permissions for specific patient data."""
        # In a real app, this would check role-based permissions
        return True  # Placeholder
    
    def _log_audit_event(self, action: str, patient_id: str, details: str) -> None:
        """Log audit event for HIPAA compliance."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "patient_id": patient_id[:8] + "...",  # Partial ID for privacy
            "user": self._get_current_user() or "unknown",
            "details": details,
            "ip_address": self._get_client_ip()
        }
        
        self.audit_log.append(event)
        self.logger.info(f"Audit: {action} - {patient_id[:8]}... - {details}")
    
    def _get_client_ip(self) -> str:
        """Get client IP address for audit logging."""
        # In a real app, this would get the actual client IP
        return "127.0.0.1"
    
    def get_audit_log(self, patient_id: Optional[str] = None) -> list:
        """Get audit log entries, optionally filtered by patient."""
        if patient_id:
            hashed_id = hashlib.sha256(patient_id.encode()).hexdigest()
            return [entry for entry in self.audit_log if entry["patient_id"].startswith(hashed_id[:8])]
        return self.audit_log

# Example usage
if __name__ == "__main__":
    # Initialize secure storage
    storage = SecurePatientStorage()
    
    # Sample patient data
    patient_data = {
        "name": "John Doe",
        "date_of_birth": "1980-01-01",
        "conditions": ["Hypertension", "Type 2 Diabetes"],
        "medications": [
            {"name": "Lisinopril", "dosage": "10mg", "frequency": "daily"},
            {"name": "Metformin", "dosage": "500mg", "frequency": "twice daily"}
        ],
        "allergies": ["Penicillin"],
        "last_visit": "2024-01-15"
    }
    
    try:
        # Encrypt and store
        patient_hash = storage.encrypt_patient_data("patient123", patient_data)
        print(f"Patient data stored securely with hash: {patient_hash}")
        
        # Retrieve and decrypt
        retrieved_data = storage.decrypt_patient_data(patient_hash)
        print(f"Retrieved patient data: {retrieved_data['name']}")
        
        # Show audit log
        audit_entries = storage.get_audit_log("patient123")
        print(f"Audit entries: {len(audit_entries)}")
        
    except Exception as e:
        print(f"Error: {e}")
```

## FHIR API Integration (JavaScript/Node.js)

### Complete Implementation

```javascript
const axios = require('axios');
const { v4: uuidv4 } = require('uuid');

/**
 * FHIR Client for healthcare data exchange
 * Supports FHIR R4 specification with HIPAA-compliant security
 */
class FHIRClient {
    /**
     * @param {string} baseUrl - FHIR server base URL
     * @param {object} authConfig - Authentication configuration
     */
    constructor(baseUrl, authConfig = {}) {
        this.baseUrl = baseUrl;
        this.authConfig = authConfig;
        
        this.client = axios.create({
            baseURL: baseUrl,
            timeout: 30000,
            headers: {
                'Content-Type': 'application/fhir+json',
                'Accept': 'application/fhir+json'
            }
        });
        
        // Add request interceptor for authentication
        this.client.interceptors.request.use(
            (config) => this._addAuthHeaders(config),
            (error) => Promise.reject(error)
        );
        
        // Add response interceptor for error handling
        this.client.interceptors.response.use(
            (response) => response,
            (error) => this._handleFHIRError(error)
        );
    }
    
    /**
     * Add authentication headers to requests
     * @param {object} config - Axios request config
     * @returns {object} Modified config with auth headers
     */
    async _addAuthHeaders(config) {
        if (this.authConfig.type === 'bearer') {
            const token = await this._getAuthToken();
            config.headers.Authorization = `Bearer ${token}`;
        } else if (this.authConfig.type === 'basic') {
            const credentials = Buffer.from(
                `${this.authConfig.username}:${this.authConfig.password}`
            ).toString('base64');
            config.headers.Authorization = `Basic ${credentials}`;
        }
        return config;
    }
    
    /**
     * Get authentication token
     * @returns {string} Auth token
     */
    async _getAuthToken() {
        // In production, implement OAuth2 flow or token refresh
        if (this.authConfig.token) {
            return this.authConfig.token;
        }
        if (this.authConfig.tokenEndpoint) {
            return this._refreshToken();
        }
        throw new Error('Authentication token not available');
    }
    
    /**
     * Get patient resource by ID
     * @param {string} patientId - Patient resource ID
     * @returns {Promise<object>} Patient resource
     */
    async getPatient(patientId) {
        if (!patientId) {
            throw new Error('Patient ID is required');
        }
        
        const response = await this.client.get(`/Patient/${patientId}`);
        return this._validateFHIRResource(response.data);
    }
    
    /**
     * Search patients with filters
     * @param {object} searchParams - Search parameters
     * @returns {Promise<object>} Bundle of patient resources
     */
    async searchPatients(searchParams = {}) {
        const params = new URLSearchParams(searchParams);
        const response = await this.client.get(`/Patient?${params}`);
        return response.data;
    }
    
    /**
     * Create new patient
     * @param {object} patientData - Patient resource data
     * @returns {Promise<object>} Created patient resource
     */
    async createPatient(patientData) {
        const patient = {
            resourceType: 'Patient',
            id: uuidv4(),
            meta: {
                profile: ['http://hl7.org/fhir/StructureDefinition/Patient']
            },
            ...patientData
        };
        
        const response = await this.client.post('/Patient', patient);
        return response.data;
    }
    
    /**
     * Create observation for patient
     * @param {string} patientId - Patient ID
     * @param {object} observationData - Observation data
     * @returns {Promise<object>} Created observation resource
     */
    async createObservation(patientId, observationData) {
        if (!patientId || !observationData) {
            throw new Error('Patient ID and observation data are required');
        }
        
        const observation = {
            resourceType: 'Observation',
            id: uuidv4(),
            subject: { reference: `Patient/${patientId}` },
            meta: {
                profile: ['http://hl7.org/fhir/StructureDefinition/Observation']
            },
            ...observationData
        };
        
        const response = await this.client.post('/Observation', observation);
        return response.data;
    }
    
    /**
     * Get patient's observations
     * @param {string} patientId - Patient ID
     * @param {object} filters - Optional filters
     * @returns {Promise<object>} Bundle of observation resources
     */
    async getPatientObservations(patientId, filters = {}) {
        const params = new URLSearchParams({
            subject: `Patient/${patientId}`,
            ...filters
        });
        
        const response = await this.client.get(`/Observation?${params}`);
        return response.data;
    }
    
    /**
     * Update patient resource
     * @param {string} patientId - Patient ID
     * @param {object} updates - Updated patient data
     * @returns {Promise<object>} Updated patient resource
     */
    async updatePatient(patientId, updates) {
        const currentPatient = await this.getPatient(patientId);
        const updatedPatient = { ...currentPatient, ...updates };
        
        const response = await this.client.put(`/Patient/${patientId}`, updatedPatient);
        return response.data;
    }
    
    /**
     * Validate FHIR resource structure
     * @param {object} resource - FHIR resource to validate
     * @returns {object} Validated resource
     */
    _validateFHIRResource(resource) {
        if (!resource.resourceType) {
            throw new Error('Invalid FHIR resource: missing resourceType');
        }
        
        if (!resource.id) {
            throw new Error('Invalid FHIR resource: missing id');
        }
        
        // Additional validation logic can be added here
        // Check required fields based on resource type
        if (resource.resourceType === 'Patient' && !resource.name) {
            console.warn('Patient resource missing name field');
        }
        
        return resource;
    }
    
    /**
     * Handle FHIR-specific errors
     * @param {Error} error - Axios error object
     */
    _handleFHIRError(error) {
        if (error.response) {
            const { status, data } = error.response;
            
            switch (status) {
                case 400:
                    throw new Error(`Bad Request: ${data?.issue?.[0]?.diagnostics || 'Invalid request'}`);
                case 401:
                    throw new Error('Unauthorized: Authentication required');
                case 403:
                    throw new Error('Forbidden: Insufficient permissions');
                case 404:
                    throw new Error('Not Found: Resource does not exist');
                case 409:
                    throw new Error('Conflict: Resource already exists or version conflict');
                case 422:
                    throw new Error(`Unprocessable Entity: ${data?.issue?.[0]?.diagnostics || 'Validation error'}`);
                case 500:
                    throw new Error('Internal Server Error: FHIR server error');
                default:
                    throw new Error(`FHIR Server Error: ${status} - ${data?.issue?.[0]?.diagnostics || 'Unknown error'}`);
            }
        } else if (error.request) {
            throw new Error('Network Error: Unable to reach FHIR server');
        } else {
            throw new Error(`Request Error: ${error.message}`);
        }
    }
    
    /**
     * Refresh authentication token
     * @returns {string} New auth token
     */
    async _refreshToken() {
        // Implement OAuth2 token refresh
        try {
            const response = await axios.post(this.authConfig.tokenEndpoint, {
                grant_type: 'refresh_token',
                refresh_token: this.authConfig.refreshToken,
                client_id: this.authConfig.clientId,
                client_secret: this.authConfig.clientSecret
            });
            
            this.authConfig.token = response.data.access_token;
            return this.authConfig.token;
        } catch (error) {
            throw new Error('Failed to refresh authentication token');
        }
    }
}

// Example usage
if (require.main === module) {
    const client = new FHIRClient('https://fhir.example.com/fhir', {
        type: 'bearer',
        token: process.env.FHIR_AUTH_TOKEN
        // For OAuth2:
        // type: 'oauth2',
        // tokenEndpoint: 'https://auth.example.com/oauth/token',
        // clientId: process.env.CLIENT_ID,
        // clientSecret: process.env.CLIENT_SECRET,
        // refreshToken: process.env.REFRESH_TOKEN
    });
    
    // Example: Get patient
    client.getPatient('12345')
        .then(patient => console.log('Patient:', patient.name?.[0]?.text))
        .catch(error => console.error('Error:', error.message));
        
    // Example: Create observation
    const observationData = {
        status: 'final',
        code: {
            coding: [{
                system: 'http://loinc.org',
                code: '8480-6',
                display: 'Systolic blood pressure'
            }]
        },
        valueQuantity: {
            value: 120,
            unit: 'mmHg',
            system: 'http://unitsofmeasure.org',
            code: 'mm[Hg]'
        },
        effectiveDateTime: new Date().toISOString()
    };
    
    client.createObservation('12345', observationData)
        .then(obs => console.log('Observation created:', obs.id))
        .catch(error => console.error('Error:', error.message));
}

module.exports = FHIRClient;
```

## HL7 v2 Message Processing (Python)

### ADT Message Parser

```python
import re
from typing import Dict, List, Optional
from datetime import datetime

class HL7v2MessageParser:
    """
    Parser for HL7 v2.x messages with support for ADT messages
    """
    
    def __init__(self):
        self.segment_patterns = {
            'MSH': self._parse_msh,
            'PID': self._parse_pid,
            'PV1': self._parse_pv1,
            'OBR': self._parse_obr,
            'OBX': self._parse_obx
        }
    
    def parse_message(self, hl7_message: str) -> Dict[str, any]:
        """
        Parse HL7 v2 message into structured data
        
        Args:
            hl7_message: Raw HL7 message string
            
        Returns:
            Dictionary containing parsed message data
        """
        lines = hl7_message.strip().split('\r')
        parsed_data = {
            'segments': [],
            'message_type': None,
            'patient_info': {},
            'visit_info': {},
            'observations': []
        }
        
        for line in lines:
            if not line.strip():
                continue
                
            segment_type = line[:3]
            segment_data = line[4:]  # Skip segment type and separator
            
            parsed_segment = self._parse_segment(segment_type, segment_data)
            parsed_data['segments'].append({
                'type': segment_type,
                'data': parsed_segment
            })
            
            # Extract key information
            if segment_type == 'MSH':
                parsed_data['message_type'] = parsed_segment.get('message_type')
            elif segment_type == 'PID':
                parsed_data['patient_info'] = parsed_segment
            elif segment_type == 'PV1':
                parsed_data['visit_info'] = parsed_segment
            elif segment_type == 'OBX':
                parsed_data['observations'].append(parsed_segment)
        
        return parsed_data
    
    def _parse_segment(self, segment_type: str, data: str) -> Dict[str, any]:
        """Parse individual HL7 segment"""
        if segment_type in self.segment_patterns:
            return self.segment_patterns[segment_type](data)
        else:
            # Generic parsing for unknown segments
            fields = data.split('|')
            return {f'field_{i}': field for i, field in enumerate(fields)}
    
    def _parse_msh(self, data: str) -> Dict[str, any]:
        """Parse MSH (Message Header) segment"""
        fields = data.split('|')
        return {
            'encoding_characters': fields[0] if len(fields) > 0 else None,
            'sending_application': fields[2] if len(fields) > 2 else None,
            'sending_facility': fields[3] if len(fields) > 3 else None,
            'receiving_application': fields[4] if len(fields) > 4 else None,
            'receiving_facility': fields[5] if len(fields) > 5 else None,
            'message_datetime': self._parse_datetime(fields[6] if len(fields) > 6 else None),
            'security': fields[7] if len(fields) > 7 else None,
            'message_type': fields[8] if len(fields) > 8 else None,
            'message_control_id': fields[9] if len(fields) > 9 else None,
            'processing_id': fields[10] if len(fields) > 10 else None,
            'version_id': fields[11] if len(fields) > 11 else None
        }
    
    def _parse_pid(self, data: str) -> Dict[str, any]:
        """Parse PID (Patient Identification) segment"""
        fields = data.split('|')
        return {
            'set_id': fields[0] if len(fields) > 0 else None,
            'external_id': self._parse_composite_id(fields[1] if len(fields) > 1 else None),
            'internal_id': self._parse_composite_id(fields[2] if len(fields) > 2 else None),
            'alternate_id': self._parse_composite_id(fields[3] if len(fields) > 3 else None),
            'patient_name': self._parse_person_name(fields[4] if len(fields) > 4 else None),
            'mothers_maiden_name': self._parse_person_name(fields[5] if len(fields) > 5 else None),
            'birth_datetime': self._parse_datetime(fields[6] if len(fields) > 6 else None),
            'sex': fields[7] if len(fields) > 7 else None,
            'patient_alias': self._parse_person_name(fields[8] if len(fields) > 8 else None),
            'race': fields[9] if len(fields) > 9 else None,
            'patient_address': self._parse_address(fields[10] if len(fields) > 10 else None),
            'county_code': fields[11] if len(fields) > 11 else None,
            'phone_home': self._parse_phone(fields[12] if len(fields) > 12 else None),
            'phone_business': self._parse_phone(fields[13] if len(fields) > 13 else None),
            'primary_language': fields[14] if len(fields) > 14 else None,
            'marital_status': fields[15] if len(fields) > 15 else None,
            'religion': fields[16] if len(fields) > 16 else None,
            'patient_account_number': fields[17] if len(fields) > 17 else None,
            'ssn': fields[18] if len(fields) > 18 else None,
            'drivers_license': fields[19] if len(fields) > 19 else None
        }
    
    def _parse_pv1(self, data: str) -> Dict[str, any]:
        """Parse PV1 (Patient Visit) segment"""
        fields = data.split('|')
        return {
            'set_id': fields[0] if len(fields) > 0 else None,
            'patient_class': fields[1] if len(fields) > 1 else None,
            'assigned_location': self._parse_location(fields[2] if len(fields) > 2 else None),
            'admission_type': fields[3] if len(fields) > 3 else None,
            'preadmit_number': fields[4] if len(fields) > 4 else None,
            'prior_location': self._parse_location(fields[5] if len(fields) > 5 else None),
            'attending_doctor': self._parse_provider(fields[6] if len(fields) > 6 else None),
            'referring_doctor': self._parse_provider(fields[7] if len(fields) > 7 else None),
            'consulting_doctor': self._parse_provider(fields[8] if len(fields) > 8 else None),
            'hospital_service': fields[9] if len(fields) > 9 else None,
            'temporary_location': self._parse_location(fields[10] if len(fields) > 10 else None),
            'preadmit_test_indicator': fields[11] if len(fields) > 11 else None,
            'readmission_indicator': fields[12] if len(fields) > 12 else None,
            'admit_source': fields[13] if len(fields) > 13 else None,
            'ambulatory_status': fields[14] if len(fields) > 14 else None,
            'vip_indicator': fields[15] if len(fields) > 15 else None,
            'admitting_doctor': self._parse_provider(fields[16] if len(fields) > 16 else None),
            'patient_type': fields[17] if len(fields) > 17 else None,
            'visit_number': fields[18] if len(fields) > 18 else None,
            'financial_class': fields[19] if len(fields) > 19 else None,
            'charge_price_indicator': fields[20] if len(fields) > 20 else None,
            'courtesy_code': fields[21] if len(fields) > 21 else None,
            'credit_rating': fields[22] if len(fields) > 22 else None,
            'contract_code': fields[23] if len(fields) > 23 else None,
            'contract_effective_date': self._parse_datetime(fields[24] if len(fields) > 24 else None),
            'contract_amount': fields[25] if len(fields) > 25 else None,
            'contract_period': fields[26] if len(fields) > 26 else None,
            'interest_code': fields[27] if len(fields) > 27 else None,
            'transfer_to_bad_debt_code': fields[28] if len(fields) > 28 else None,
            'transfer_to_bad_debt_date': self._parse_datetime(fields[29] if len(fields) > 29 else None),
            'bad_debt_agency_code': fields[30] if len(fields) > 30 else None,
            'bad_debt_transfer_amount': fields[31] if len(fields) > 31 else None,
            'bad_debt_recovery_amount': fields[32] if len(fields) > 32 else None,
            'delete_account_indicator': fields[33] if len(fields) > 33 else None,
            'delete_account_date': self._parse_datetime(fields[34] if len(fields) > 34 else None),
            'discharge_disposition': fields[35] if len(fields) > 35 else None,
            'discharged_to_location': self._parse_location(fields[36] if len(fields) > 36 else None),
            'diet_type': fields[37] if len(fields) > 37 else None,
            'servicing_facility': fields[38] if len(fields) > 38 else None,
            'bed_status': fields[39] if len(fields) > 39 else None,
            'account_status': fields[40] if len(fields) > 40 else None,
            'pending_location': self._parse_location(fields[41] if len(fields) > 41 else None),
            'prior_temporary_location': self._parse_location(fields[42] if len(fields) > 42 else None),
            'admit_date_time': self._parse_datetime(fields[43] if len(fields) > 43 else None),
            'discharge_date_time': self._parse_datetime(fields[44] if len(fields) > 44 else None),
            'current_patient_balance': fields[45] if len(fields) > 45 else None,
            'total_charges': fields[46] if len(fields) > 46 else None,
            'total_adjustments': fields[47] if len(fields) > 47 else None,
            'total_payments': fields[48] if len(fields) > 48 else None,
            'alternate_visit_id': fields[49] if len(fields) > 49 else None,
            'visit_indicator': fields[50] if len(fields) > 50 else None,
            'other_healthcare_provider': self._parse_provider(fields[51] if len(fields) > 51 else None)
        }
    
    def _parse_obr(self, data: str) -> Dict[str, any]:
        """Parse OBR (Observation Request) segment"""
        fields = data.split('|')
        return {
            'set_id': fields[0] if len(fields) > 0 else None,
            'placer_order_number': fields[1] if len(fields) > 1 else None,
            'filler_order_number': fields[2] if len(fields) > 2 else None,
            'universal_service_id': self._parse_coded_element(fields[3] if len(fields) > 3 else None),
            'priority': fields[4] if len(fields) > 4 else None,
            'requested_datetime': self._parse_datetime(fields[5] if len(fields) > 5 else None),
            'observation_datetime': self._parse_datetime(fields[6] if len(fields) > 6 else None),
            'observation_end_datetime': self._parse_datetime(fields[7] if len(fields) > 7 else None),
            'collection_volume': self._parse_quantity(fields[8] if len(fields) > 8 else None),
            'collector_identifier': self._parse_provider(fields[9] if len(fields) > 9 else None),
            'specimen_action_code': fields[10] if len(fields) > 10 else None,
            'danger_code': fields[11] if len(fields) > 11 else None,
            'relevant_clinical_info': fields[12] if len(fields) > 12 else None,
            'specimen_received_datetime': self._parse_datetime(fields[13] if len(fields) > 13 else None),
            'specimen_source': self._parse_specimen_source(fields[14] if len(fields) > 14 else None),
            'ordering_provider': self._parse_provider(fields[15] if len(fields) > 15 else None),
            'order_callback_phone_number': self._parse_phone(fields[16] if len(fields) > 16 else None),
            'placer_field_1': fields[17] if len(fields) > 17 else None,
            'placer_field_2': fields[18] if len(fields) > 18 else None,
            'filler_field_1': fields[19] if len(fields) > 19 else None,
            'filler_field_2': fields[20] if len(fields) > 20 else None,
            'results_status_change_datetime': self._parse_datetime(fields[21] if len(fields) > 21 else None),
            'charge_to_practice': self._parse_money(fields[22] if len(fields) > 22 else None),
            'diagnostic_serv_sect_id': fields[23] if len(fields) > 23 else None,
            'result_status': fields[24] if len(fields) > 24 else None,
            'parent_result': self._parse_parent_result(fields[25] if len(fields) > 25 else None),
            'quantity_timing': self._parse_timing_quantity(fields[26] if len(fields) > 26 else None),
            'result_copies_to': self._parse_provider(fields[27] if len(fields) > 27 else None),
            'parent_number': self._parse_parent_result(fields[28] if len(fields) > 28 else None),
            'transportation_mode': fields[29] if len(fields) > 29 else None,
            'reason_for_study': self._parse_coded_element(fields[30] if len(fields) > 30 else None),
            'principal_result_interpreter': self._parse_provider(fields[31] if len(fields) > 31 else None),
            'assistant_result_interpreter': self._parse_provider(fields[32] if len(fields) > 32 else None),
            'technician': self._parse_provider(fields[33] if len(fields) > 33 else None),
            'transcriptionist': self._parse_provider(fields[34] if len(fields) > 34 else None),
            'scheduled_datetime': self._parse_datetime(fields[35] if len(fields) > 35 else None)
        }
    
    def _parse_obx(self, data: str) -> Dict[str, any]:
        """Parse OBX (Observation Result) segment"""
        fields = data.split('|')
        return {
            'set_id': fields[0] if len(fields) > 0 else None,
            'value_type': fields[1] if len(fields) > 1 else None,
            'observation_identifier': self._parse_coded_element(fields[2] if len(fields) > 2 else None),
            'observation_sub_id': fields[3] if len(fields) > 3 else None,
            'observation_value': self._parse_observation_value(fields[4] if len(fields) > 4 else None, fields[1] if len(fields) > 1 else None),
            'units': self._parse_coded_element(fields[5] if len(fields) > 5 else None),
            'reference_range': fields[6] if len(fields) > 6 else None,
            'abnormal_flags': fields[7] if len(fields) > 7 else None,
            'probability': fields[8] if len(fields) > 8 else None,
            'nature_of_abnormal_test': fields[9] if len(fields) > 9 else None,
            'observation_result_status': fields[10] if len(fields) > 10 else None,
            'effective_date_of_reference_range': self._parse_datetime(fields[11] if len(fields) > 11 else None),
            'user_defined_access_checks': fields[12] if len(fields) > 12 else None,
            'datetime_of_the_observation': self._parse_datetime(fields[13] if len(fields) > 13 else None),
            'producers_id': self._parse_coded_element(fields[14] if len(fields) > 14 else None),
            'responsible_observer': self._parse_provider(fields[15] if len(fields) > 15 else None),
            'observation_method': self._parse_coded_element(fields[16] if len(fields) > 16 else None),
            'equipment_instance_identifier': self._parse_equipment_instance(fields[17] if len(fields) > 17 else None),
            'datetime_of_the_analysis': self._parse_datetime(fields[18] if len(fields) > 18 else None)
        }
    
    # Helper parsing methods
    def _parse_composite_id(self, field: str) -> Optional[Dict[str, str]]:
        """Parse composite ID field (e.g., ID^CheckDigit^Code^AssigningAuthority)"""
        if not field:
            return None
        parts = field.split('^')
        return {
            'id': parts[0] if len(parts) > 0 else None,
            'check_digit': parts[1] if len(parts) > 1 else None,
            'code': parts[2] if len(parts) > 2 else None,
            'assigning_authority': parts[3] if len(parts) > 3 else None
        }
    
    def _parse_person_name(self, field: str) -> Optional[Dict[str, str]]:
        """Parse person name field (e.g., Family^Given^Middle^Suffix^Prefix)"""
        if not field:
            return None
        parts = field.split('^')
        return {
            'family_name': parts[0] if len(parts) > 0 else None,
            'given_name': parts[1] if len(parts) > 1 else None,
            'middle_name': parts[2] if len(parts) > 2 else None,
            'suffix': parts[3] if len(parts) > 3 else None,
            'prefix': parts[4] if len(parts) > 4 else None
        }
    
    def _parse_datetime(self, field: str) -> Optional[datetime]:
        """Parse HL7 datetime field"""
        if not field:
            return None
        try:
            # HL7 datetime format: YYYYMMDDHHMMSS
            if len(field) >= 8:
                year = int(field[0:4])
                month = int(field[4:6])
                day = int(field[6:8])
                hour = int(field[8:10]) if len(field) >= 10 else 0
                minute = int(field[10:12]) if len(field) >= 12 else 0
                second = int(field[12:14]) if len(field) >= 14 else 0
                return datetime(year, month, day, hour, minute, second)
        except (ValueError, IndexError):
            pass
        return None
    
    def _parse_address(self, field: str) -> Optional[Dict[str, str]]:
        """Parse address field"""
        if not field:
            return None
        parts = field.split('^')
        return {
            'street_address': parts[0] if len(parts) > 0 else None,
            'other_designation': parts[1] if len(parts) > 1 else None,
            'city': parts[2] if len(parts) > 2 else None,
            'state': parts[3] if len(parts) > 3 else None,
            'zip_code': parts[4] if len(parts) > 4 else None,
            'country': parts[5] if len(parts) > 5 else None,
            'address_type': parts[6] if len(parts) > 6 else None,
            'other_geographic_designation': parts[7] if len(parts) > 7 else None
        }
    
    def _parse_phone(self, field: str) -> Optional[Dict[str, str]]:
        """Parse phone number field"""
        if not field:
            return None
        parts = field.split('^')
        return {
            'telephone_number': parts[0] if len(parts) > 0 else None,
            'telecommunication_use_code': parts[1] if len(parts) > 1 else None,
            'telecommunication_equipment_type': parts[2] if len(parts) > 2 else None,
            'email_address': parts[3] if len(parts) > 3 else None,
            'country_code': parts[4] if len(parts) > 4 else None,
            'area_code': parts[5] if len(parts) > 5 else None,
            'local_number': parts[6] if len(parts) > 6 else None,
            'extension': parts[7] if len(parts) > 7 else None,
            'any_text': parts[8] if len(parts) > 8 else None,
            'extension_prefix': parts[9] if len(parts) > 9 else None,
            'speed_dial_code': parts[10] if len(parts) > 10 else None
        }
    
    def _parse_coded_element(self, field: str) -> Optional[Dict[str, str]]:
        """Parse coded element field (e.g., Code^Text^System)"""
        if not field:
            return None
        parts = field.split('^')
        return {
            'identifier': parts[0] if len(parts) > 0 else None,
            'text': parts[1] if len(parts) > 1 else None,
            'name_of_coding_system': parts[2] if len(parts) > 2 else None,
            'alternate_identifier': parts[3] if len(parts) > 3 else None,
            'alternate_text': parts[4] if len(parts) > 4 else None,
            'name_of_alternate_coding_system': parts[5] if len(parts) > 5 else None
        }
    
    def _parse_location(self, field: str) -> Optional[Dict[str, str]]:
        """Parse location field"""
        if not field:
            return None
        parts = field.split('^')
        return {
            'point_of_care': parts[0] if len(parts) > 0 else None,
            'room': parts[1] if len(parts) > 1 else None,
            'bed': parts[2] if len(parts) > 2 else None,
            'facility': self._parse_hierarchic_designator(parts[3] if len(parts) > 3 else None),
            'location_status': parts[4] if len(parts) > 4 else None,
            'person_location_type': parts[5] if len(parts) > 5 else None,
            'building': parts[6] if len(parts) > 6 else None,
            'floor': parts[7] if len(parts) > 7 else None,
            'location_description': parts[8] if len(parts) > 8 else None
        }
    
    def _parse_provider(self, field: str) -> Optional[Dict[str, str]]:
        """Parse provider field"""
        if not field:
            return None
        parts = field.split('^')
        return {
            'id_number': parts[0] if len(parts) > 0 else None,
            'family_name': parts[1] if len(parts) > 1 else None,
            'given_name': parts[2] if len(parts) > 2 else None,
            'middle_name': parts[3] if len(parts) > 3 else None,
            'suffix': parts[4] if len(parts) > 4 else None,
            'prefix': parts[5] if len(parts) > 5 else None,
            'degree': parts[6] if len(parts) > 6 else None,
            'source_table': parts[7] if len(parts) > 7 else None,
            'assigning_authority': self._parse_hierarchic_designator(parts[8] if len(parts) > 8 else None),
            'name_type_code': parts[9] if len(parts) > 9 else None,
            'identifier_check_digit': parts[10] if len(parts) > 10 else None,
            'check_digit_scheme': parts[11] if len(parts) > 11 else None,
            'identifier_type_code': parts[12] if len(parts) > 12 else None,
            'assigning_facility': self._parse_hierarchic_designator(parts[13] if len(parts) > 13 else None),
            'name_representation_code': parts[14] if len(parts) > 14 else None,
            'name_context': self._parse_coded_element(parts[15] if len(parts) > 15 else None),
            'name_validity_range': parts[16] if len(parts) > 16 else None,
            'name_assembly_order': parts[17] if len(parts) > 17 else None,
            'effective_date': self._parse_datetime(parts[18] if len(parts) > 18 else None),
            'expiration_date': self._parse_datetime(parts[19] if len(parts) > 19 else None),
            'professional_suffix': parts[20] if len(parts) > 20 else None,
            'assigning_jurisdiction': self._parse_coded_element(parts[21] if len(parts) > 21 else None),
            'assigning_agency_or_department': self._parse_coded_element(parts[22] if len(parts) > 22 else None)
        }
    
    def _parse_hierarchic_designator(self, field: str) -> Optional[Dict[str, str]]:
        """Parse hierarchic designator field"""
        if not field:
            return None
        parts = field.split('^')
        return {
            'namespace_id': parts[0] if len(parts) > 0 else None,
            'universal_id': parts[1] if len(parts) > 1 else None,
            'universal_id_type': parts[2] if len(parts) > 2 else None
        }
    
    def _parse_quantity(self, field: str) -> Optional[Dict[str, str]]:
        """Parse quantity field"""
        if not field:
            return None
        parts = field.split('^')
        return {
            'quantity': parts[0] if len(parts) > 0 else None,
            'units': self._parse_coded_element(parts[1] if len(parts) > 1 else None)
        }
    
    def _parse_specimen_source(self, field: str) -> Optional[Dict[str, str]]:
        """Parse specimen source field"""
        if not field:
            return None
        parts = field.split('^')
        return {
            'specimen_source_name_or_code': self._parse_coded_element(parts[0] if len(parts) > 0 else None),
            'additives': parts[1] if len(parts) > 1 else None,
            'specimen_collection_method': parts[2] if len(parts) > 2 else None,
            'body_site': self._parse_coded_element(parts[3] if len(parts) > 3 else None),
            'site_modifier': self._parse_coded_element(parts[4] if len(parts) > 4 else None),
            'collection_method_modifier_code': self._parse_coded_element(parts[5] if len(parts) > 5 else None),
            'specimen_role': self._parse_coded_element(parts[6] if len(parts) > 6 else None)
        }
    
    def _parse_money(self, field: str) -> Optional[Dict[str, str]]:
        """Parse money field"""
        if not field:
            return None
        parts = field.split('^')
        return {
            'quantity': parts[0] if len(parts) > 0 else None,
            'denomination': parts[1] if len(parts) > 1 else None
        }
    
    def _parse_parent_result(self, field: str) -> Optional[Dict[str, str]]:
        """Parse parent result field"""
        if not field:
            return None
        parts = field.split('^')
        return {
            'parent_observation_identifier': self._parse_coded_element(parts[0] if len(parts) > 0 else None),
            'parent_observation_sub_identifier': parts[1] if len(parts) > 1 else None,
            'parent_observation_value_descriptor': parts[2] if len(parts) > 2 else None
        }
    
    def _parse_timing_quantity(self, field: str) -> Optional[Dict[str, str]]:
        """Parse timing quantity field"""
        if not field:
            return None
        parts = field.split('^')
        return {
            'quantity': parts[0] if len(parts) > 0 else None,
            'interval': parts[1] if len(parts) > 1 else None,
            'duration': parts[2] if len(parts) > 2 else None,
            'start_datetime': self._parse_datetime(parts[3] if len(parts) > 3 else None),
            'end_datetime': self._parse_datetime(parts[4] if len(parts) > 4 else None),
            'priority': parts[5] if len(parts) > 5 else None,
            'condition': parts[6] if len(parts) > 6 else None,
            'text': parts[7] if len(parts) > 7 else None,
            'conjunction': parts[8] if len(parts) > 8 else None,
            'order_sequencing': self._parse_order_sequencing(parts[9] if len(parts) > 9 else None)
        }
    
    def _parse_order_sequencing(self, field: str) -> Optional[Dict[str, str]]:
        """Parse order sequencing field"""
        if not field:
            return None
        parts = field.split('^')
        return {
            'sequence_results_flag': parts[0] if len(parts) > 0 else None,
            'placer_order_number': self._parse_entity_identifier(parts[1] if len(parts) > 1 else None),
            'filler_order_number': self._parse_entity_identifier(parts[2] if len(parts) > 2 else None),
            'sequence_condition_value': parts[3] if len(parts) > 3 else None,
            'maximum_number_of_repeats': parts[4] if len(parts) > 4 else None,
            'placer_order_number_namespace_id': parts[5] if len(parts) > 5 else None,
            'placer_order_number_universal_id': parts[6] if len(parts) > 6 else None,
            'placer_order_number_universal_id_type': parts[7] if len(parts) > 7 else None
        }
    
    def _parse_entity_identifier(self, field: str) -> Optional[Dict[str, str]]:
        """Parse entity identifier field"""
        if not field:
            return None
        parts = field.split('^')
        return {
            'entity_id': parts[0] if len(parts) > 0 else None,
            'namespace_id': parts[1] if len(parts) > 1 else None,
            'universal_id': parts[2] if len(parts) > 2 else None,
            'universal_id_type': parts[3] if len(parts) > 3 else None
        }
    
    def _parse_equipment_instance(self, field: str) -> Optional[Dict[str, str]]:
        """Parse equipment instance field"""
        if not field:
            return None
        parts = field.split('^')
        return {
            'equipment_instance_identifier': self._parse_entity_identifier(parts[0] if len(parts) > 0 else None),
            'event_datetime': self._parse_datetime(parts[1] if len(parts) > 1 else None),
            'equipment_state': self._parse_coded_element(parts[2] if len(parts) > 2 else None),
            'local_remote_control_state': self._parse_coded_element(parts[3] if len(parts) > 3 else None),
            'alert_level': parts[4] if len(parts) > 4 else None
        }
    
    def _parse_observation_value(self, field: str, value_type: str) -> any:
        """Parse observation value based on value type"""
        if not field:
            return None
        
        if value_type == 'NM':  # Numeric
            try:
                return float(field)
            except ValueError:
                return field
        elif value_type == 'ST':  # String
            return field
        elif value_type == 'DT':  # Date
            return self._parse_datetime(field)
        elif value_type == 'TM':  # Time
            return field  # Could be enhanced with time parsing
        elif value_type == 'TS':  # Timestamp
            return self._parse_datetime(field)
        elif value_type == 'FT':  # Formatted text
            return field
        elif value_type == 'TX':  # Text
            return field
        elif value_type == 'CE':  # Coded element
            return self._parse_coded_element(field)
        else:
            return field  # Default to string

# Example usage
if __name__ == "__main__":
    parser = HL7v2MessageParser()
    
    # Sample ADT A01 message (Admission)
    sample_message = """MSH|^~\\&|SENDING_APP|SENDING_FACILITY|RECEIVING_APP|RECEIVING_FACILITY|20240101120000||ADT^A01|MSG00001|P|2.5
EVN|A01|20240101120000
PID|1||123456^^^MR||DOE^JOHN^A||19800101|M|||123 MAIN ST^^ANYTOWN^NY^12345||(555)123-4567|||S||123456789
PV1|1|I|2000^2012^01||||12345^DOCTOR^JOHN^S^^MD|||||||||||123456|||||||||||||||||||||||||20240101120000"""
    
    parsed = parser.parse_message(sample_message)
    print("Message Type:", parsed['message_type'])
    print("Patient Name:", parsed['patient_info']['patient_name'])
    print("Visit Info:", parsed['visit_info']['patient_class'])
```
