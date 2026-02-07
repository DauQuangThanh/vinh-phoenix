---
name: healthcare-coding
description: Generates and implements code for healthcare applications with emphasis on code simplicity, maintainability, and readability, ensuring compliance with medical standards, security requirements, and regulatory frameworks. Use when developing healthcare software, implementing medical data handling, creating patient management systems, or when user mentions healthcare coding, medical apps, HIPAA, HL7, or FHIR.
license: MIT
metadata:
  author: Dau Quang Thanh
  version: "1.1"
  last_updated: "2026-02-07"
---

# Healthcare Coding

## Overview

This skill provides comprehensive guidance for developing secure, compliant code for healthcare-related applications with emphasis on simplicity, maintainability, and readability. It covers medical data handling, regulatory compliance (HIPAA, GDPR), security best practices, and integration with healthcare standards like HL7 and FHIR. The skill ensures that healthcare software meets industry standards for patient safety, data privacy, and interoperability while maintaining high code quality.

## When to Use

- Developing healthcare software applications and systems
- Implementing patient data management and electronic health records (EHR)
- Creating medical device software or mobile health apps
- Ensuring compliance with healthcare regulations and standards
- Writing secure code for handling sensitive medical information
- Integrating with healthcare APIs and data exchange formats
- When user mentions healthcare coding, medical apps, patient data, HIPAA, HL7, FHIR, or healthcare compliance

## Prerequisites

- Programming knowledge in relevant languages (Python, JavaScript, Java, etc.)
- Understanding of healthcare regulations (HIPAA, GDPR, local health data laws)
- Familiarity with secure coding practices and data encryption
- Knowledge of healthcare standards (HL7, FHIR, DICOM)
- Access to healthcare standards documentation and testing tools

## Instructions

### Step 1: Assess Healthcare Requirements

1. Identify the type of healthcare application (EHR, telemedicine, medical device, etc.)
2. Determine data types (patient records, medical images, sensor data)
3. Review applicable regulations (HIPAA for US, GDPR for EU, etc.)
4. Define security and privacy requirements

### Step 2: Choose Technology Stack

1. Select programming language based on application needs and team expertise
2. Choose appropriate frameworks and libraries that promote clean code
3. Plan for scalability and performance requirements
4. Consider maintainability and readability of the chosen technologies
5. Ensure the stack supports healthcare-specific security and compliance features

### Step 3: Establish Code Quality Standards

1. Define coding conventions for simplicity and readability
2. Implement consistent naming conventions for healthcare domain objects
3. Set up code review processes focusing on maintainability
4. Establish automated testing and code quality checks
5. Document code quality guidelines specific to healthcare applications

### Step 4: Implement Security and Compliance

1. Implement data encryption for sensitive information
2. Add access controls and authentication mechanisms
3. Include audit logging for all data access
4. Ensure data anonymization where required

### Step 5: Integrate Healthcare Standards

1. Implement HL7 messaging for data exchange
2. Use FHIR APIs for interoperability
3. Handle DICOM for medical imaging if needed
4. Validate data formats and standards compliance

### Step 6: Test and Validate

1. Perform security testing and penetration testing
2. Validate compliance with regulations
3. Test interoperability with other healthcare systems
4. Conduct user acceptance testing with medical professionals
5. Review code for simplicity, maintainability, and readability
6. Run automated code quality checks and linting

## Examples

### Example 1: Secure Patient Data Storage

**Input:** Need to store patient medical records securely with HIPAA compliance

**Key Implementation Points:**

- Use AES-256 encryption for data at rest
- Implement SHA-256 hashing for patient ID indexing
- Add comprehensive audit logging
- Include role-based access control
- Ensure data integrity verification
- Write clear, well-documented code with meaningful variable names
- Implement error handling that maintains data security

**See [references/code-examples.md](references/code-examples.md) for complete implementation**

### Example 2: FHIR API Integration

**Input:** Integrate with FHIR server for patient data exchange

**Key Implementation Points:**

- Use proper FHIR content-type headers (`application/fhir+json`)
- Implement OAuth2 authentication for secure access
- Handle FHIR-specific error responses
- Validate FHIR resource structure
- Support FHIR R4 specification
- Structure code with clear separation of concerns for maintainability
- Add comprehensive logging and error messages for debugging

**See [references/code-examples.md](references/code-examples.md) for complete implementation**

### Example 3: HL7 v2 Message Processing

**Input:** Parse HL7 v2 messages for healthcare data exchange

**Key Implementation Points:**

- Parse MSH, PID, PV1, OBR, OBX segments
- Handle HL7 encoding characters (^~\&)
- Validate message structure and required fields
- Support ADT, ORU, and other message types
- Implement proper error handling for malformed messages
- Use descriptive function and variable names for healthcare domain clarity
- Implement modular parsing functions for better maintainability

**See [references/code-examples.md](references/code-examples.md) for complete implementation**

## Edge Cases

### Case 1: Handling Large Medical Images (DICOM)

**Handling:** Use streaming for large files, implement progressive loading, ensure secure transmission with TLS 1.3+

### Case 2: International Patient Data (Multi-Region Compliance)

**Handling:** Implement region-specific encryption, handle different regulatory requirements, use geo-fencing for data storage

### Case 3: Real-Time Medical Device Data

**Handling:** Implement low-latency processing, ensure data integrity, handle device authentication and authorization

### Case 4: Legacy System Integration

**Handling:** Create adapters for old formats, implement data migration scripts, maintain backward compatibility

## Error Handling

### Data Privacy Breach Prevention

**Solution:** Implement end-to-end encryption, regular security audits, automated data masking for logs

### FHIR Validation Errors

**Solution:** Use FHIR validation libraries, implement retry logic with exponential backoff, log validation failures

### Regulatory Compliance Failures

**Solution:** Regular compliance checks, automated reporting, integration with compliance monitoring tools

### Performance Issues with Large Datasets

**Solution:** Implement pagination, caching strategies, database optimization for medical queries

## Scripts

Use `scripts/generate-healthcare-code.py` to generate boilerplate code for common healthcare patterns.

```bash
python3 scripts/generate-healthcare-code.py --pattern secure-storage --language python
```

## References

See [references/healthcare-standards.md](references/healthcare-standards.md) for detailed healthcare standards documentation.

See [references/security-best-practices.md](references/security-best-practices.md) for healthcare security guidelines.

## Validation

Run `scripts/validate-healthcare-code.py` to check code against healthcare compliance rules.

```bash
python3 scripts/validate-healthcare-code.py --file patient_storage.py
```
