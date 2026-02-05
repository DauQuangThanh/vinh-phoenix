#!/usr/bin/env python3
"""
Healthcare Code Validator

Validates healthcare application code against security and compliance standards.

Usage: python3 validate-healthcare-code.py --file <file> [--standards hipaa,fhir]
Platforms: Windows, macOS, Linux
Requirements: Python 3.8+, ast, re modules
"""

import argparse
import ast
import re
import sys
from pathlib import Path
from typing import List, Dict, Set

class HealthcareCodeValidator:
    """Validator for healthcare application code compliance."""
    
    def __init__(self):
        self.issues: List[Dict] = []
        self.hipaa_patterns = {
            'encryption': re.compile(r'(?i)(encrypt|decrypt|cipher|fernet|aes)'),
            'logging': re.compile(r'(?i)(log|audit|logger)'),
            'access_control': re.compile(r'(?i)(permission|authorize|access|role)'),
            'sensitive_data': re.compile(r'(?i)(patient|medical|health|diagnosis|treatment)'),
        }
        
        self.fhir_patterns = {
            'resource_type': re.compile(r'resourceType\s*:\s*[\'"](Patient|Observation|Condition|Medication)[\'"]'),
            'fhir_headers': re.compile(r'application/fhir\+json'),
            'fhir_validation': re.compile(r'(?i)(validate.*fhir|fhir.*validate)'),
        }
    
    def validate_file(self, file_path: str, standards: List[str]) -> bool:
        """Validate a code file against specified standards."""
        path = Path(file_path)
        if not path.exists():
            self.issues.append({
                'type': 'error',
                'message': f'File not found: {file_path}',
                'line': 0
            })
            return False
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse Python AST if it's a Python file
            if path.suffix == '.py':
                self._validate_python_ast(content, standards)
            
            # Check for required patterns
            self._validate_patterns(content, standards)
            
            # Language-specific validations
            if path.suffix == '.py':
                self._validate_python_security(content)
            elif path.suffix in ['.js', '.ts']:
                self._validate_javascript_security(content)
            
            return len([i for i in self.issues if i['type'] == 'error']) == 0
            
        except Exception as e:
            self.issues.append({
                'type': 'error',
                'message': f'Failed to parse file: {str(e)}',
                'line': 0
            })
            return False
    
    def _validate_python_ast(self, content: str, standards: List[str]):
        """Validate Python code using AST analysis."""
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                # Check for insecure practices
                if isinstance(node, ast.Import):
                    self._check_insecure_imports(node)
                elif isinstance(node, ast.Call):
                    self._check_insecure_calls(node)
                elif isinstance(node, ast.Str):
                    self._check_hardcoded_secrets(node)
                    
        except SyntaxError as e:
            self.issues.append({
                'type': 'error',
                'message': f'Syntax error: {e.msg}',
                'line': e.lineno or 0
            })
    
    def _check_insecure_imports(self, node: ast.Import):
        """Check for potentially insecure imports."""
        insecure_modules = {'pickle', 'eval', 'exec'}
        for alias in node.names:
            if alias.name in insecure_modules:
                self.issues.append({
                    'type': 'warning',
                    'message': f'Insecure import detected: {alias.name}. Consider safer alternatives.',
                    'line': node.lineno
                })
    
    def _check_insecure_calls(self, node: ast.Call):
        """Check for potentially insecure function calls."""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name == 'eval':
                self.issues.append({
                    'type': 'error',
                    'message': 'Use of eval() detected. This is a security risk.',
                    'line': node.lineno
                })
            elif func_name == 'exec':
                self.issues.append({
                    'type': 'error',
                    'message': 'Use of exec() detected. This is a security risk.',
                    'line': node.lineno
                })
    
    def _check_hardcoded_secrets(self, node: ast.Str):
        """Check for potentially hardcoded secrets."""
        suspicious_patterns = [
            r'password\s*=\s*[\'"][^\'"]+[\'"]',
            r'secret\s*=\s*[\'"][^\'"]+[\'"]',
            r'key\s*=\s*[\'"][^\'"]+[\'"]',
            r'token\s*=\s*[\'"][^\'"]+[\'"]',
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, node.s, re.IGNORECASE):
                self.issues.append({
                    'type': 'warning',
                    'message': 'Potential hardcoded secret detected. Use environment variables or secure key management.',
                    'line': node.lineno
                })
    
    def _validate_patterns(self, content: str, standards: List[str]):
        """Validate content against required patterns for standards."""
        lines = content.split('\n')
        
        for standard in standards:
            if standard.lower() == 'hipaa':
                self._validate_hipaa_patterns(content, lines)
            elif standard.lower() == 'fhir':
                self._validate_fhir_patterns(content, lines)
    
    def _validate_hipaa_patterns(self, content: str, lines: List[str]):
        """Validate HIPAA compliance patterns."""
        required_patterns = {
            'encryption': 'Encryption mechanisms for sensitive data',
            'logging': 'Audit logging for data access',
            'access_control': 'Access control mechanisms',
        }
        
        for pattern_name, description in required_patterns.items():
            pattern = self.hipaa_patterns.get(pattern_name)
            if pattern and not pattern.search(content):
                self.issues.append({
                    'type': 'warning',
                    'message': f'Missing HIPAA requirement: {description}',
                    'line': 0
                })
    
    def _validate_fhir_patterns(self, content: str, lines: List[str]):
        """Validate FHIR compliance patterns."""
        required_patterns = {
            'resource_type': 'Proper FHIR resource types',
            'fhir_headers': 'FHIR content-type headers',
        }
        
        for pattern_name, description in required_patterns.items():
            pattern = self.fhir_patterns.get(pattern_name)
            if pattern and not pattern.search(content):
                self.issues.append({
                    'type': 'warning',
                    'message': f'Missing FHIR requirement: {description}',
                    'line': 0
                })
    
    def _validate_python_security(self, content: str):
        """Python-specific security validations."""
        # Check for SQL injection vulnerabilities
        sql_patterns = [
            r'cursor\.execute\s*\(\s*[\'"][^\'"]*\%[^\'"]*[\'"]',
            r'cursor\.execute\s*\(\s*f[\'"]',
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                self.issues.append({
                    'type': 'error',
                    'message': 'Potential SQL injection vulnerability. Use parameterized queries.',
                    'line': 0
                })
    
    def _validate_javascript_security(self, content: str):
        """JavaScript-specific security validations."""
        # Check for XSS vulnerabilities
        xss_patterns = [
            r'innerHTML\s*=',
            r'document\.write\s*\(',
            r'eval\s*\(',
        ]
        
        for pattern in xss_patterns:
            if re.search(pattern, content):
                self.issues.append({
                    'type': 'warning',
                    'message': 'Potential XSS vulnerability detected.',
                    'line': 0
                })
    
    def print_report(self):
        """Print validation report."""
        if not self.issues:
            print("✅ No issues found. Code appears compliant.")
            return
        
        errors = [i for i in self.issues if i['type'] == 'error']
        warnings = [i for i in self.issues if i['type'] == 'warning']
        
        print(f"Validation Report: {len(errors)} errors, {len(warnings)} warnings")
        print("-" * 50)
        
        for issue in self.issues:
            marker = "❌" if issue['type'] == 'error' else "⚠️"
            line_info = f" (line {issue['line']})" if issue['line'] > 0 else ""
            print(f"{marker} {issue['message']}{line_info}")
    
    def get_summary(self) -> Dict:
        """Get validation summary."""
        return {
            'total_issues': len(self.issues),
            'errors': len([i for i in self.issues if i['type'] == 'error']),
            'warnings': len([i for i in self.issues if i['type'] == 'warning']),
            'issues': self.issues
        }

def main():
    parser = argparse.ArgumentParser(description='Validate healthcare code compliance')
    parser.add_argument('--file', '-f', required=True, help='Code file to validate')
    parser.add_argument('--standards', '-s', nargs='+', 
                       choices=['hipaa', 'fhir', 'gdpr'], 
                       default=['hipaa'], 
                       help='Compliance standards to check')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')
    
    args = parser.parse_args()
    
    validator = HealthcareCodeValidator()
    is_valid = validator.validate_file(args.file, args.standards)
    
    if args.json:
        import json
        print(json.dumps(validator.get_summary(), indent=2))
    else:
        validator.print_report()
    
    sys.exit(0 if is_valid else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)