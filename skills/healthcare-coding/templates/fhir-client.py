"""
FHIR Client Template

This template provides a foundation for integrating with FHIR servers for healthcare data exchange.
Customize the server URL, authentication, and resource handling for your application.

Requirements:
- requests: pip install requests
- requests-oauthlib: pip install requests-oauthlib

Features:
- OAuth2 authentication
- FHIR resource CRUD operations
- Search and query capabilities
- Error handling and retry logic
- FHIR version R4 support
"""

import json
import logging
from typing import Dict, Any, Optional, List
from urllib.parse import urlencode

import requests
from requests_oauthlib import OAuth2Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class FHIRClient:
    """
    FHIR API client for healthcare data exchange.

    Usage:
        client = FHIRClient("https://fhir.example.com", client_id="your-client-id")
        patient = client.get_patient("12345")
        client.create_observation(observation_data)
    """

    def __init__(self,
                 base_url: str,
                 client_id: Optional[str] = None,
                 client_secret: Optional[str] = None,
                 token_url: Optional[str] = None,
                 timeout: int = 30):
        """
        Initialize FHIR client.

        Args:
            base_url: Base URL of the FHIR server
            client_id: OAuth2 client ID
            client_secret: OAuth2 client secret
            token_url: OAuth2 token endpoint URL
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.timeout = timeout

        # Setup logging
        self.logger = logging.getLogger(__name__)

        # Setup session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # FHIR headers
        self.session.headers.update({
            'Accept': 'application/fhir+json',
            'Content-Type': 'application/fhir+json',
            'User-Agent': 'Healthcare-App/1.0'
        })

        # OAuth2 setup
        if client_id and client_secret and token_url:
            self.oauth = OAuth2Session(client_id=client_id, redirect_uri=None)
            self._authenticate()
        else:
            self.oauth = None

    def _authenticate(self):
        """Perform OAuth2 authentication."""
        try:
            token = self.oauth.fetch_token(
                token_url=self.token_url,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            self.session.headers.update({
                'Authorization': f'Bearer {token["access_token"]}'
            })
            self.logger.info("OAuth2 authentication successful")
        except Exception as e:
            self.logger.error(f"OAuth2 authentication failed: {e}")
            raise

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs.setdefault('timeout', self.timeout)

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {method} {url} - {e}")
            raise

    def get_patient(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a patient resource by ID.

        Args:
            patient_id: FHIR patient ID

        Returns:
            Patient resource dictionary or None if not found
        """
        try:
            response = self._make_request('GET', f'Patient/{patient_id}')
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                self.logger.warning(f"Patient {patient_id} not found")
                return None
            raise

    def search_patients(self, search_params: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Search for patients using FHIR search parameters.

        Args:
            search_params: Dictionary of search parameters
                e.g., {'family': 'Doe', 'given': 'John', 'birthdate': '1980-01-01'}

        Returns:
            List of patient resources
        """
        query_string = urlencode(search_params)
        response = self._make_request('GET', f'Patient?{query_string}')
        data = response.json()

        # Extract entries from bundle
        entries = data.get('entry', [])
        return [entry['resource'] for entry in entries]

    def create_patient(self, patient_data: Dict[str, Any]) -> str:
        """
        Create a new patient resource.

        Args:
            patient_data: Patient resource data

        Returns:
            ID of the created patient
        """
        response = self._make_request('POST', 'Patient', json=patient_data)
        location = response.headers.get('Location', '')
        patient_id = location.split('/')[-1] if location else 'unknown'
        self.logger.info(f"Created patient {patient_id}")
        return patient_id

    def update_patient(self, patient_id: str, patient_data: Dict[str, Any]) -> bool:
        """
        Update an existing patient resource.

        Args:
            patient_id: FHIR patient ID
            patient_data: Updated patient resource data

        Returns:
            True if successful
        """
        self._make_request('PUT', f'Patient/{patient_id}', json=patient_data)
        self.logger.info(f"Updated patient {patient_id}")
        return True

    def get_observation(self, observation_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an observation resource by ID.

        Args:
            observation_id: FHIR observation ID

        Returns:
            Observation resource dictionary or None if not found
        """
        try:
            response = self._make_request('GET', f'Observation/{observation_id}')
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                self.logger.warning(f"Observation {observation_id} not found")
                return None
            raise

    def create_observation(self, observation_data: Dict[str, Any]) -> str:
        """
        Create a new observation resource.

        Args:
            observation_data: Observation resource data

        Returns:
            ID of the created observation
        """
        response = self._make_request('POST', 'Observation', json=observation_data)
        location = response.headers.get('Location', '')
        observation_id = location.split('/')[-1] if location else 'unknown'
        self.logger.info(f"Created observation {observation_id}")
        return observation_id

    def search_observations(self, patient_id: str, code: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for observations for a specific patient.

        Args:
            patient_id: Patient ID to search observations for
            code: Optional LOINC code to filter observations

        Returns:
            List of observation resources
        """
        search_params = {'subject': f'Patient/{patient_id}'}
        if code:
            search_params['code'] = code

        query_string = urlencode(search_params)
        response = self._make_request('GET', f'Observation?{query_string}')
        data = response.json()

        # Extract entries from bundle
        entries = data.get('entry', [])
        return [entry['resource'] for entry in entries]

    def get_capability_statement(self) -> Dict[str, Any]:
        """
        Retrieve the FHIR server's capability statement.

        Returns:
            Capability statement resource
        """
        response = self._make_request('GET', 'metadata')
        return response.json()

    def validate_resource(self, resource: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a FHIR resource against the server's validation endpoint.

        Args:
            resource: FHIR resource to validate

        Returns:
            Validation result
        """
        response = self._make_request('POST', '$validate', json=resource)
        return response.json()

# Example usage
if __name__ == "__main__":
    # Initialize client (without OAuth for example)
    client = FHIRClient("https://hapi.fhir.org/baseR4")

    # Get capability statement
    capability = client.get_capability_statement()
    print(f"FHIR Version: {capability.get('fhirVersion')}")

    # Search for patients
    patients = client.search_patients({'family': 'Smith'})
    print(f"Found {len(patients)} patients with family name Smith")

    # Example patient data
    patient_data = {
        "resourceType": "Patient",
        "name": [{
            "family": "Doe",
            "given": ["John"]
        }],
        "gender": "male",
        "birthDate": "1980-01-01"
    }

    # Create patient (would require authentication in real scenario)
    # patient_id = client.create_patient(patient_data)
    # print(f"Created patient: {patient_id}")

    # Example observation data
    observation_data = {
        "resourceType": "Observation",
        "status": "final",
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "8480-6",
                "display": "Systolic blood pressure"
            }]
        },
        "subject": {
            "reference": "Patient/example"
        },
        "valueQuantity": {
            "value": 120,
            "unit": "mmHg",
            "system": "http://unitsofmeasure.org",
            "code": "mm[Hg]"
        }
    }

    # Create observation (would require authentication in real scenario)
    # observation_id = client.create_observation(observation_data)
    # print(f"Created observation: {observation_id}")