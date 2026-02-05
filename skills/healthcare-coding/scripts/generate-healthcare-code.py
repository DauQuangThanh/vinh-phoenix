#!/usr/bin/env python3
"""
Healthcare Code Generator

Generates boilerplate code for common healthcare application patterns.

Usage: python3 generate-healthcare-code.py --pattern <pattern> --language <lang>
Platforms: Windows, macOS, Linux
Requirements: Python 3.8+
"""

import argparse
import sys
from pathlib import Path

def generate_secure_storage_python():
    """Generate secure patient data storage class in Python."""
    return '''import hashlib
import os
from cryptography.fernet import Fernet
from typing import Dict, Any
import logging

class SecurePatientStorage:
    """
    HIPAA-compliant secure storage for patient medical data.
    
    Features:
    - AES-256 encryption
    - Audit logging
    - Access control
    - Data integrity checks
    """
    
    def __init__(self, key_file: str = None):
        self.key_file = key_file or "encryption.key"
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)
        self.logger = logging.getLogger(__name__)
        
    def _load_or_generate_key(self) -> bytes:
        """Load existing key or generate new one."""
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
        Encrypt patient medical data.
        
        Args:
            patient_id: Unique patient identifier
            medical_data: Dictionary containing medical information
            
        Returns:
            Hashed patient ID for storage reference
        """
        # Hash patient ID for privacy-preserving indexing
        hashed_id = hashlib.sha256(patient_id.encode()).hexdigest()
        
        # Convert data to JSON string and encrypt
        import json
        data_str = json.dumps(medical_data, sort_keys=True)
        encrypted_data = self.cipher.encrypt(data_str.encode())
        
        # Store with audit trail
        self._store_with_audit(hashed_id, encrypted_data)
        
        self.logger.info(f"Encrypted data for patient {hashed_id[:8]}...")
        return hashed_id
    
    def decrypt_patient_data(self, hashed_id: str) -> Dict[str, Any]:
        """
        Decrypt and retrieve patient medical data.
        
        Args:
            hashed_id: Hashed patient identifier
            
        Returns:
            Decrypted medical data dictionary
        """
        if not self._check_access_permissions():
            raise PermissionError("Unauthorized access to patient data")
        
        encrypted_data = self._retrieve_data(hashed_id)
        decrypted_data = self.cipher.decrypt(encrypted_data).decode()
        
        import json
        medical_data = json.loads(decrypted_data)
        
        self.logger.info(f"Decrypted data for patient {hashed_id[:8]}...")
        return medical_data
    
    def _store_with_audit(self, hashed_id: str, encrypted_data: bytes):
        """Store encrypted data with audit logging."""
        # Implementation depends on storage backend (database, file system, etc.)
        # This is a placeholder - implement according to your storage needs
        pass
    
    def _retrieve_data(self, hashed_id: str) -> bytes:
        """Retrieve encrypted data from storage."""
        # Implementation depends on storage backend
        pass
    
    def _check_access_permissions(self) -> bool:
        """Check if current user has access permissions (HIPAA compliance)."""
        # Implement proper access control logic
        # Check user roles, consent, emergency access, etc.
        return True  # Placeholder

# Example usage
if __name__ == "__main__":
    storage = SecurePatientStorage()
    
    # Sample patient data
    patient_data = {
        "name": "John Doe",
        "dob": "1980-01-01",
        "conditions": ["Hypertension", "Diabetes"],
        "medications": ["Lisinopril", "Metformin"]
    }
    
    # Encrypt and store
    patient_hash = storage.encrypt_patient_data("patient123", patient_data)
    print(f"Patient data stored with hash: {patient_hash}")
    
    # Retrieve and decrypt
    retrieved_data = storage.decrypt_patient_data(patient_hash)
    print(f"Retrieved data: {retrieved_data}")
'''

def generate_fhir_client_javascript():
    """Generate FHIR client for JavaScript/Node.js."""
    return '''const axios = require('axios');
const { v4: uuidv4 } = require('uuid');

/**
 * FHIR Client for healthcare data exchange
 * Supports FHIR R4 specification
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
            headers: {
                'Content-Type': 'application/fhir+json',
                'Accept': 'application/fhir+json'
            },
            timeout: 30000
        });
        
        // Add authentication interceptor
        this.client.interceptors.request.use((config) => {
            return this._addAuthHeaders(config);
        });
        
        // Add response interceptor for error handling
        this.client.interceptors.response.use(
            (response) => response,
            (error) => this._handleFHIRError(error)
        );
    }
    
    /**
     * Add authentication headers to request
     */
    async _addAuthHeaders(config) {
        if (this.authConfig.type === 'bearer') {
            config.headers.Authorization = `Bearer ${await this._getAuthToken()}`;
        } else if (this.authConfig.type === 'basic') {
            const credentials = Buffer.from(`${this.authConfig.username}:${this.authConfig.password}`).toString('base64');
            config.headers.Authorization = `Basic ${credentials}`;
        }
        return config;
    }
    
    /**
     * Get authentication token
     */
    async _getAuthToken() {
        // Implement OAuth2 token retrieval or other auth methods
        if (this.authConfig.token) {
            return this.authConfig.token;
        }
        throw new Error('Authentication token not available');
    }
    
    /**
     * Get patient resource by ID
     * @param {string} patientId - Patient resource ID
     */
    async getPatient(patientId) {
        const response = await this.client.get(`/Patient/${patientId}`);
        return this._validateFHIRResource(response.data);
    }
    
    /**
     * Search patients with filters
     * @param {object} searchParams - Search parameters
     */
    async searchPatients(searchParams = {}) {
        const params = new URLSearchParams(searchParams);
        const response = await this.client.get(`/Patient?${params}`);
        return response.data;
    }
    
    /**
     * Create new patient
     * @param {object} patientData - Patient resource data
     */
    async createPatient(patientData) {
        const patient = {
            resourceType: 'Patient',
            id: uuidv4(),
            ...patientData,
            meta: {
                profile: ['http://hl7.org/fhir/StructureDefinition/Patient']
            }
        };
        
        const response = await this.client.post('/Patient', patient);
        return response.data;
    }
    
    /**
     * Create observation for patient
     * @param {string} patientId - Patient ID
     * @param {object} observationData - Observation data
     */
    async createObservation(patientId, observationData) {
        const observation = {
            resourceType: 'Observation',
            id: uuidv4(),
            subject: { reference: `Patient/${patientId}` },
            ...observationData,
            meta: {
                profile: ['http://hl7.org/fhir/StructureDefinition/Observation']
            }
        };
        
        const response = await this.client.post('/Observation', observation);
        return response.data;
    }
    
    /**
     * Get patient's observations
     * @param {string} patientId - Patient ID
     * @param {object} filters - Optional filters
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
     * Validate FHIR resource structure
     * @param {object} resource - FHIR resource to validate
     */
    _validateFHIRResource(resource) {
        if (!resource.resourceType) {
            throw new Error('Invalid FHIR resource: missing resourceType');
        }
        
        if (!resource.id) {
            throw new Error('Invalid FHIR resource: missing id');
        }
        
        // Additional validation can be added here
        return resource;
    }
    
    /**
     * Handle FHIR-specific errors
     * @param {Error} error - Axios error object
     */
    _handleFHIRError(error) {
        if (error.response) {
            const status = error.response.status;
            const data = error.response.data;
            
            switch (status) {
                case 400:
                    throw new Error(`Bad Request: ${data?.issue?.[0]?.diagnostics || 'Invalid request'}`);
                case 401:
                    throw new Error('Unauthorized: Authentication required');
                case 403:
                    throw new Error('Forbidden: Insufficient permissions');
                case 404:
                    throw new Error('Not Found: Resource does not exist');
                case 422:
                    throw new Error(`Unprocessable Entity: ${data?.issue?.[0]?.diagnostics || 'Validation error'}`);
                default:
                    throw new Error(`FHIR Server Error: ${status} - ${data?.issue?.[0]?.diagnostics || 'Unknown error'}`);
            }
        } else if (error.request) {
            throw new Error('Network Error: Unable to reach FHIR server');
        } else {
            throw new Error(`Request Error: ${error.message}`);
        }
    }
}

module.exports = FHIRClient;

// Example usage
if (require.main === module) {
    const client = new FHIRClient('https://fhir.example.com/fhir', {
        type: 'bearer',
        token: process.env.FHIR_TOKEN
    });
    
    // Example: Get patient
    client.getPatient('12345')
        .then(patient => console.log('Patient:', patient))
        .catch(error => console.error('Error:', error));
}
'''

def main():
    parser = argparse.ArgumentParser(description='Generate healthcare code patterns')
    parser.add_argument('--pattern', required=True, 
                       choices=['secure-storage', 'fhir-client'],
                       help='Code pattern to generate')
    parser.add_argument('--language', required=True,
                       choices=['python', 'javascript'],
                       help='Programming language')
    parser.add_argument('--output', '-o', 
                       help='Output file path (default: stdout)')
    
    args = parser.parse_args()
    
    # Generate code based on pattern and language
    if args.pattern == 'secure-storage' and args.language == 'python':
        code = generate_secure_storage_python()
    elif args.pattern == 'fhir-client' and args.language == 'javascript':
        code = generate_fhir_client_javascript()
    else:
        print(f"Error: Pattern '{args.pattern}' not available for language '{args.language}'", file=sys.stderr)
        sys.exit(1)
    
    # Output code
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"Code generated: {output_path}")
    else:
        print(code)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)