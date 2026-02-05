# Healthcare API Contract: [Endpoint Name]

**Version**: 1.0
**Date**: [YYYY-MM-DD]
**Author**: [Name]
**Related Healthcare Design**: [Link to design.md]
**PHI Level**: 🔴 High / 🟡 Medium / 🟢 Low Risk
**HIPAA Compliance**: ✅ Compliant / ⚠️ Review Required

---

## Healthcare Endpoint Overview

**Path**: `/api/v1/healthcare/[resource]/[action]`
**Method**: GET | POST | PUT | PATCH | DELETE
**Clinical Purpose**: [What clinical workflow or patient care function this supports]

**Use Case**: [When and why healthcare providers/patients would call this endpoint]

**Patient Safety Impact**: [High/Medium/Low - how critical this is to patient care]

---

## HIPAA Compliance & Security

### PHI Data Handling

**PHI Level**: 🔴 **High Risk** / 🟡 **Medium Risk** / 🟢 **Low Risk**

**PHI Data Elements**:

- [List specific PHI fields accessed/modified by this endpoint]
- [Note encryption requirements and access controls]

**Consent Requirements**:

- [Patient consent needed: Yes/No]
- [Consent scope required]
- [Consent verification method]

### Authentication Required

- **Required**: Yes (all healthcare endpoints require authentication)
- **Method**: Multi-Factor Authentication (MFA) + Bearer Token (JWT)
- **Token Location**: Header `Authorization: Bearer <token>`
- **MFA Required**: Yes for PHI access / No for low-risk data

### Authorization Rules

**Required Permissions**:

- `[healthcare.permission.resource.action]` (e.g., `healthcare.patient.record.read`)
- Clinical role-based access control (RBAC)

**Required Roles**:

- `[physician, nurse, admin]` - clinical care providers
- `[patient]` - patient access to own data
- `[billing]` - limited access for billing purposes

**Resource Ownership**:

- Patients can only access their own PHI
- Providers can access assigned patients' data
- Admins can access all data with audit logging

**Emergency Access**:

- Break-glass procedures for clinical emergencies
- Requires secondary authorization and audit logging

**Example Authorization Header**:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
X-MFA-Token: 123456
```

---

## Audit Logging Requirements

### PHI Access Logging

**Audit Events**:

- User ID, timestamp, patient ID, endpoint accessed
- Business purpose justification
- IP address and user agent
- Success/failure status

**Retention**: 7 years minimum (HIPAA requirement)

### Clinical Safety Logging

**Clinical Events**:

- All patient data modifications
- Critical value notifications
- Clinical decision support interactions

---

## Request Specification

### URL Parameters

| Parameter | Type | Required | PHI Level | Description | Validation | Example |
|-----------|------|----------|-----------|-------------|------------|---------|
| `patientId` | UUID | Yes | 🔴 High | Patient medical record identifier | Must be valid patient ID, access controlled | `550e8400-e29b-41d4-a716-446655440000` |
| `encounterId` | UUID | No | 🟡 Medium | Clinical encounter identifier | Must belong to authorized patient | `550e8400-e29b-41d4-a716-446655440001` |
| `providerId` | UUID | No | 🟡 Medium | Healthcare provider identifier | Must be valid, licensed provider | `550e8400-e29b-41d4-a716-446655440002` |

**Example URL**:

```
/api/v1/healthcare/patients/550e8400-e29b-41d4-a716-446655440000/records
```

### Query Parameters

| Parameter | Type | Required | Default | PHI Level | Constraints | Description |
|-----------|------|----------|---------|-----------|-------------|-------------|
| `page` | Integer | No | 1 | 🟢 Low | Min: 1 | Page number for clinical data pagination |
| `limit` | Integer | No | 20 | 🟢 Low | Min: 1, Max: 100 | Items per page (rate limited for PHI) |
| `dateFrom` | Date | No | 30 days ago | 🟡 Medium | Valid date, not future | Filter clinical records from date |
| `dateTo` | Date | No | Today | 🟡 Medium | Valid date, after dateFrom | Filter clinical records to date |
| `status` | Enum | No | - | 🟢 Low | ACTIVE, INACTIVE, ARCHIVED | Clinical record status filter |
| `category` | String | No | - | 🟢 Low | Max 50 chars | Clinical category filter |

**Example Query String**:

```
?page=1&limit=50&dateFrom=2024-01-01&dateTo=2024-01-31&status=ACTIVE
```

### Request Headers

| Header | Required | PHI Impact | Description | Example |
|--------|----------|------------|-------------|---------|
| `Content-Type` | Yes | 🟢 Low | Request content type | `application/json` |
| `Accept` | No | 🟢 Low | Accepted response type | `application/fhir+json` |
| `X-Request-ID` | Yes | 🟢 Low | Request tracking for audit | `req-uuid-healthcare-12345` |
| `X-Purpose` | Yes | 🟡 Medium | Business purpose for PHI access | `TREATMENT` |
| `X-Emergency-Access` | No | 🔴 High | Emergency override (requires approval) | `APPROVED-BY-DR-SMITH` |
| `X-Consent-Verified` | Yes (for PHI) | 🟡 Medium | Patient consent verification | `consent-uuid-67890` |

### Request Body

**Content-Type**: `application/json` or `application/fhir+json`

#### Schema (Patient Record Creation)

```json
{
  "resourceType": "Bundle",
  "type": "transaction",
  "entry": [
    {
      "resource": {
        "resourceType": "Patient",
        "id": "patient-123",
        "identifier": [
          {
            "system": "http://hospital.org/mrn",
            "value": "MRN-123456",
            "type": {
              "coding": [
                {
                  "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                  "code": "MR",
                  "display": "Medical Record Number"
                }
              ]
            }
          }
        ],
        "name": [
          {
            "family": "Smith",
            "given": ["John"],
            "use": "official"
          }
        ],
        "gender": "male",
        "birthDate": "1980-01-01",
        "address": [
          {
            "use": "home",
            "line": ["123 Main St"],
            "city": "Anytown",
            "state": "CA",
            "postalCode": "12345",
            "country": "US"
          }
        ],
        "telecom": [
          {
            "system": "phone",
            "value": "+1-555-0123",
            "use": "home"
          }
        ],
        "contact": [
          {
            "relationship": [
              {
                "coding": [
                  {
                    "system": "http://terminology.hl7.org/CodeSystem/v2-0131",
                    "code": "C",
                    "display": "Emergency Contact"
                  }
                ]
              }
            ],
            "name": {
              "family": "Smith",
              "given": ["Jane"],
              "use": "official"
            },
            "telecom": [
              {
                "system": "phone",
                "value": "+1-555-0987",
                "use": "home"
              }
            ]
          }
        ]
      }
    }
  ],
  "meta": {
    "security": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/v3-Confidentiality",
        "code": "R",
        "display": "Restricted"
      }
    ],
    "tag": [
      {
        "system": "http://hospital.org/tags",
        "code": "HIPAA-COMPLIANT",
        "display": "HIPAA Compliant"
      }
    ]
  }
}
```

#### Field Validations

**Patient Resource**:

- `identifier`: Must include valid MRN, validated against hospital format
- `name`: Required for clinical identification, no special characters
- `birthDate`: Must be valid date in past, used for age calculations
- `gender`: Must be valid HL7 gender code
- `address`: Must include complete address for emergency contact
- `telecom`: Must be valid phone/email format
- `contact`: Emergency contact required for clinical safety

**Clinical Safety Validations**:

- Patient age must be appropriate for clinical context
- Emergency contact must include reachable phone number
- Address must be valid for emergency services

---

## Response Specification

### Success Response

**Status Code**: 200 OK / 201 Created

**Content-Type**: `application/json` or `application/fhir+json`

#### Schema

```json
{
  "resourceType": "Bundle",
  "id": "bundle-response-123",
  "type": "searchset",
  "total": 1,
  "link": [
    {
      "relation": "self",
      "url": "https://api.hospital.org/fhir/Patient?_id=patient-123"
    }
  ],
  "entry": [
    {
      "resource": {
        "resourceType": "Patient",
        "id": "patient-123",
        "meta": {
          "versionId": "1",
          "lastUpdated": "2024-01-15T10:30:00Z",
          "security": [
            {
              "system": "http://terminology.hl7.org/CodeSystem/v3-Confidentiality",
              "code": "R",
              "display": "Restricted"
            }
          ]
        },
        "identifier": [
          {
            "system": "http://hospital.org/mrn",
            "value": "MRN-123456"
          }
        ],
        "name": [
          {
            "family": "Smith",
            "given": ["John"]
          }
        ],
        "gender": "male",
        "birthDate": "1980-01-01",
        "address": [
          {
            "use": "home",
            "line": ["123 Main St"],
            "city": "Anytown",
            "state": "CA",
            "postalCode": "12345"
          }
        ],
        "telecom": [
          {
            "system": "phone",
            "value": "+1-555-0123"
          }
        ]
      },
      "search": {
        "mode": "match",
        "score": 1.0
      }
    }
  ]
}
```

### Response Headers

| Header | Description | Example |
|--------|-------------|---------|
| `X-Request-ID` | Echoed request ID for tracking | `req-uuid-healthcare-12345` |
| `X-PHI-Access-Logged` | Confirms PHI access was audited | `true` |
| `X-Consent-Verified` | Confirms patient consent was checked | `consent-uuid-67890` |
| `ETag` | Resource version for optimistic locking | `"W/\"1\""` |
| `Last-Modified` | When resource was last modified | `Mon, 15 Jan 2024 10:30:00 GMT` |

### Error Responses

#### 400 Bad Request (Clinical Data Validation Error)

```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "invalid",
      "details": {
        "text": "Invalid patient birth date - cannot be in future"
      },
      "expression": ["Patient.birthDate"]
    }
  ]
}
```

#### 401 Unauthorized (Authentication Failure)

```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "login",
      "details": {
        "text": "Multi-factor authentication required for PHI access"
      }
    }
  ]
}
```

#### 403 Forbidden (Authorization Failure)

```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "forbidden",
      "details": {
        "text": "Access denied: Provider not assigned to this patient"
      },
      "expression": ["Patient"]
    }
  ]
}
```

#### 404 Not Found (Patient Not Found)

```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Patient not found or access denied"
      }
    }
  ]
}
```

#### 422 Unprocessable Entity (Consent Required)

```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "business-rule",
      "details": {
        "text": "Patient consent required for this operation"
      },
      "expression": ["Patient"]
    }
  ]
}
```

#### 500 Internal Server Error (System Failure)

```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "exception",
      "details": {
        "text": "Clinical system temporarily unavailable - contact IT support"
      }
    }
  ]
}
```

### Error Response Headers

| Header | Description | Example |
|--------|-------------|---------|
| `X-Error-ID` | Unique error identifier for support | `err-healthcare-67890` |
| `X-PHI-Access-Logged` | Error was logged for audit | `true` |
| `Retry-After` | Seconds to wait before retry (for 503) | `300` |

---

## Clinical Safety Considerations

### Patient Safety Validations

1. **Data Integrity Checks**:
   - All patient identifiers validated before processing
   - Clinical data ranges verified (e.g., blood pressure within safe limits)
   - Medication contraindications checked against patient allergies

2. **Emergency Access Procedures**:
   - Break-glass access requires secondary provider authorization
   - All emergency access logged with clinical justification
   - Automatic audit alert generated for compliance review

3. **Fail-Safe Mechanisms**:
   - System degrades gracefully during outages
   - Critical patient data cached locally when possible
   - Clinical workflows continue with paper backup if needed

### Clinical Workflow Integration

**Supported Workflows**:

- Patient admission and registration
- Clinical assessment and documentation
- Order entry and management
- Medication administration
- Discharge planning

**Workflow Safety Checks**:

- Required clinical fields validated before workflow progression
- Clinical decision support triggered for high-risk orders
- Provider credentials verified before critical actions

---

## Performance Requirements

### Response Time SLAs

| Operation Type | Target Response Time | PHI Impact |
|----------------|---------------------|------------|
| Patient lookup | <100ms | Low |
| Clinical record retrieval | <500ms | High |
| FHIR resource creation | <1s | High |
| Bulk data export | <30s | High |

### Rate Limiting

**Authenticated Users**:

- 100 requests per minute for PHI operations
- 1000 requests per minute for non-PHI operations

**Emergency Override**:

- No rate limiting during declared emergencies
- Requires emergency access token

---

## Interoperability Standards

### HL7 FHIR Compliance

**Supported FHIR Versions**: R4, R4B

**Key Profiles**:

- US Core Patient Profile
- US Core Encounter Profile
- US Core Condition Profile

**Extensions Used**:

- Clinical safety extensions
- Privacy consent extensions
- Audit logging extensions

### Data Exchange Formats

**Supported Formats**:

- FHIR JSON (preferred)
- FHIR XML
- Legacy HL7 v2 (for EHR integration)

**Content Negotiation**:

- Accept header determines response format
- Default to FHIR JSON for new integrations

---

## Testing and Validation

### Clinical Safety Testing

**Required Test Cases**:

- Patient data integrity validation
- Emergency access procedures
- Clinical workflow completion
- Error handling and recovery

### HIPAA Compliance Testing

**Security Testing**:

- PHI encryption validation
- Access control verification
- Audit logging accuracy
- Consent management testing

### Interoperability Testing

**Integration Testing**:

- FHIR resource validation
- HL7 message processing
- EHR system connectivity
- Data exchange accuracy

---

## Implementation Notes

### Security Implementation

**PHI Encryption**:

- All PHI fields encrypted at rest using AES-256-GCM
- TLS 1.3 required for data in transit
- Separate encryption keys for different data classifications

**Access Control Implementation**:

- OAuth 2.0 with clinical scopes
- Role-based permissions with clinical context
- Attribute-based access control for complex rules

### Audit Implementation

**Logging Framework**:

- Structured logging with PHI-safe formatting
- Centralized audit log storage
- Real-time alerting for suspicious activities

**Retention and Archival**:

- 7-year retention for clinical audit logs
- Automated archival to secure storage
- Regular integrity checking

---

## Revision History

| Date | Version | Author | Changes | Compliance Impact |
|------|---------|--------|---------|-------------------|
| [Date] | 1.0 | [Name] | Initial healthcare API contract | [HIPAA compliance established] |
| [Date] | 1.1 | [Name] | [Clinical safety enhancements] | [Improved patient safety validations] |
