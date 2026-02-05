"""
HL7 Parser Template

This template provides a foundation for parsing and processing HL7 v2 messages.
Customize the message types, field mappings, and processing logic for your application.

Requirements:
- hl7apy: pip install hl7apy

Features:
- HL7 v2 message parsing
- Support for common message types (ADT, ORU, ORM)
- Field validation and error handling
- Message acknowledgment generation
- Custom field mapping support
"""

import logging
import re
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

try:
    from hl7apy import parser
    from hl7apy.core import Message
    HL7APY_AVAILABLE = True
except ImportError:
    HL7APY_AVAILABLE = False
    print("Warning: hl7apy not installed. Install with: pip install hl7apy")

class HL7Parser:
    """
    HL7 v2 message parser and processor.

    Usage:
        parser = HL7Parser()
        message = parser.parse_hl7_message(hl7_text)
        patient_data = parser.extract_patient_info(message)
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # HL7 encoding characters (Segment^Field^Component^Subcomponent^Repetition^Escape)
        self.encoding_chars = "^~\\&"

        # Common HL7 message types
        self.message_types = {
            'ADT': 'Admit/Discharge/Transfer',
            'ORU': 'Observation Result Unsolicited',
            'ORM': 'Order Message',
            'ACK': 'Acknowledgment'
        }

    def parse_hl7_message(self, hl7_text: str) -> Optional[Message]:
        """
        Parse HL7 message text into structured format.

        Args:
            hl7_text: Raw HL7 message text

        Returns:
            Parsed HL7 message object or None if parsing fails
        """
        if not HL7APY_AVAILABLE:
            self.logger.error("hl7apy library not available")
            return None

        try:
            # Clean the message
            cleaned_message = self._clean_hl7_message(hl7_text)

            # Parse the message
            message = parser.parse_message(cleaned_message, encoding_chars=self.encoding_chars)

            self.logger.info(f"Parsed HL7 message: {message.msh.message_type.msh_9_1}")
            return message

        except Exception as e:
            self.logger.error(f"Failed to parse HL7 message: {e}")
            return None

    def _clean_hl7_message(self, hl7_text: str) -> str:
        """Clean and normalize HL7 message text."""
        # Remove any BOM or invisible characters
        cleaned = hl7_text.strip()

        # Ensure proper line endings
        cleaned = cleaned.replace('\r\n', '\r').replace('\n', '\r')

        # Remove empty lines
        lines = [line for line in cleaned.split('\r') if line.strip()]
        cleaned = '\r'.join(lines)

        return cleaned

    def extract_patient_info(self, message: Message) -> Dict[str, Any]:
        """
        Extract patient information from HL7 message.

        Args:
            message: Parsed HL7 message

        Returns:
            Dictionary containing patient information
        """
        patient_info = {}

        try:
            # Extract from PID segment
            if hasattr(message, 'pid'):
                pid = message.pid

                patient_info.update({
                    'patient_id': self._get_field_value(pid.pid_3),  # Patient ID
                    'patient_name': self._extract_patient_name(pid.pid_5),  # Patient Name
                    'date_of_birth': self._format_date(pid.pid_7),  # Date of Birth
                    'gender': self._get_field_value(pid.pid_8),  # Gender
                    'race': self._get_field_value(pid.pid_10),  # Race
                    'address': self._extract_address(pid.pid_11),  # Address
                    'phone': self._get_field_value(pid.pid_13),  # Phone
                    'marital_status': self._get_field_value(pid.pid_16),  # Marital Status
                })

            # Extract from PV1 segment (visit information)
            if hasattr(message, 'pv1'):
                pv1 = message.pv1

                patient_info.update({
                    'visit_number': self._get_field_value(pv1.pv1_19),  # Visit Number
                    'admission_type': self._get_field_value(pv1.pv1_2),  # Patient Class
                    'attending_doctor': self._extract_doctor_name(pv1.pv1_7),  # Attending Doctor
                    'admission_date': self._format_date(pv1.pv1_44),  # Admit Date/Time
                })

        except Exception as e:
            self.logger.error(f"Failed to extract patient info: {e}")

        return patient_info

    def extract_observation_info(self, message: Message) -> List[Dict[str, Any]]:
        """
        Extract observation/result information from HL7 message.

        Args:
            message: Parsed HL7 message

        Returns:
            List of observation dictionaries
        """
        observations = []

        try:
            if hasattr(message, 'orc'):
                # Order information
                orc = message.orc
                order_info = {
                    'order_control': self._get_field_value(orc.orc_1),
                    'placer_order_number': self._get_field_value(orc.orc_2),
                    'filler_order_number': self._get_field_value(orc.orc_3),
                    'order_status': self._get_field_value(orc.orc_5),
                }

            # Extract from OBR segments
            obr_segments = getattr(message, 'obr', [])
            if not isinstance(obr_segments, list):
                obr_segments = [obr_segments]

            for obr in obr_segments:
                obr_info = {
                    'set_id': self._get_field_value(obr.obr_1),
                    'placer_order_number': self._get_field_value(obr.obr_2),
                    'filler_order_number': self._get_field_value(obr.obr_3),
                    'universal_service_id': self._extract_coded_element(obr.obr_4),
                    'observation_date_time': self._format_date(obr.obr_7),
                    'specimen_received_date_time': self._format_date(obr.obr_14),
                    'ordering_provider': self._extract_doctor_name(obr.obr_16),
                }

                # Extract results from OBX segments
                obx_segments = getattr(message, 'obx', [])
                if not isinstance(obx_segments, list):
                    obx_segments = [obx_segments]

                results = []
                for obx in obx_segments:
                    result = {
                        'set_id': self._get_field_value(obx.obx_1),
                        'value_type': self._get_field_value(obx.obx_2),
                        'observation_id': self._extract_coded_element(obx.obx_3),
                        'observation_value': self._get_field_value(obx.obx_5),
                        'units': self._get_field_value(obx.obx_6),
                        'reference_range': self._get_field_value(obx.obx_7),
                        'abnormal_flags': self._get_field_value(obx.obx_8),
                        'observation_date_time': self._format_date(obx.obx_14),
                    }
                    results.append(result)

                obr_info['results'] = results
                observations.append(obr_info)

        except Exception as e:
            self.logger.error(f"Failed to extract observation info: {e}")

        return observations

    def _get_field_value(self, field) -> str:
        """Extract value from HL7 field."""
        if field and hasattr(field, 'value'):
            return str(field.value).strip()
        return ""

    def _extract_coded_element(self, field) -> Dict[str, str]:
        """Extract coded element (identifier^text^coding_system)."""
        value = self._get_field_value(field)
        if '^' in value:
            parts = value.split('^')
            return {
                'identifier': parts[0] if len(parts) > 0 else "",
                'text': parts[1] if len(parts) > 1 else "",
                'coding_system': parts[2] if len(parts) > 2 else "",
            }
        return {'identifier': value, 'text': "", 'coding_system': ""}

    def _extract_patient_name(self, field) -> str:
        """Extract patient name from PID-5 field."""
        value = self._get_field_value(field)
        if '^' in value:
            parts = value.split('^')
            # Last^First^Middle^Suffix
            last = parts[0] if len(parts) > 0 else ""
            first = parts[1] if len(parts) > 1 else ""
            middle = parts[2] if len(parts) > 2 else ""
            suffix = parts[3] if len(parts) > 3 else ""

            name_parts = [first, middle, last]
            full_name = ' '.join([p for p in name_parts if p])
            if suffix:
                full_name += f", {suffix}"
            return full_name.strip()
        return value

    def _extract_address(self, field) -> Dict[str, str]:
        """Extract address from PID-11 field."""
        value = self._get_field_value(field)
        if '^' in value:
            parts = value.split('^')
            return {
                'street': parts[0] if len(parts) > 0 else "",
                'city': parts[2] if len(parts) > 2 else "",
                'state': parts[3] if len(parts) > 3 else "",
                'zip': parts[4] if len(parts) > 4 else "",
                'country': parts[5] if len(parts) > 5 else "",
            }
        return {'street': value}

    def _extract_doctor_name(self, field) -> str:
        """Extract doctor name from doctor fields."""
        value = self._get_field_value(field)
        if '^' in value:
            parts = value.split('^')
            # ID^Last^First^Middle^Suffix^Prefix
            last = parts[1] if len(parts) > 1 else ""
            first = parts[2] if len(parts) > 2 else ""
            middle = parts[3] if len(parts) > 3 else ""
            suffix = parts[4] if len(parts) > 4 else ""
            prefix = parts[5] if len(parts) > 5 else ""

            name_parts = [prefix, first, middle, last]
            full_name = ' '.join([p for p in name_parts if p])
            if suffix:
                full_name += f", {suffix}"
            return full_name.strip()
        return value

    def _format_date(self, field) -> Optional[str]:
        """Format HL7 date/time field to ISO format."""
        value = self._get_field_value(field)
        if not value:
            return None

        try:
            # HL7 date formats: YYYYMMDDHHMMSS, YYYYMMDDHHMM, YYYYMMDD
            if len(value) >= 8:
                if len(value) >= 14:
                    # YYYYMMDDHHMMSS
                    dt = datetime.strptime(value[:14], '%Y%m%d%H%M%S')
                elif len(value) >= 12:
                    # YYYYMMDDHHMM
                    dt = datetime.strptime(value[:12], '%Y%m%d%H%M')
                else:
                    # YYYYMMDD
                    dt = datetime.strptime(value[:8], '%Y%m%d')
                return dt.isoformat()
        except ValueError:
            pass

        return value

    def generate_ack(self, original_message: Message, ack_code: str = 'AA') -> str:
        """
        Generate HL7 acknowledgment message.

        Args:
            original_message: Original HL7 message
            ack_code: Acknowledgment code (AA=Accept, AE=Error, AR=Reject)

        Returns:
            HL7 acknowledgment message as string
        """
        if not HL7APY_AVAILABLE:
            return ""

        try:
            # Create ACK message
            ack = Message("ACK")

            # Copy MSH from original
            original_msh = original_message.msh
            ack.msh.msh_3 = "YOUR_APP"  # Sending Application
            ack.msh.msh_4 = "YOUR_FACILITY"  # Sending Facility
            ack.msh.msh_5 = original_msh.msh_3.value  # Receiving Application
            ack.msh.msh_6 = original_msh.msh_4.value  # Receiving Facility
            ack.msh.msh_7 = datetime.now().strftime('%Y%m%d%H%M%S')  # Date/Time
            ack.msh.msh_9 = "ACK"  # Message Type
            ack.msh.msh_10 = f"{original_msh.msh_10.value}_ACK"  # Message Control ID
            ack.msh.msh_11 = "P"  # Processing ID
            ack.msh.msh_12 = "2.5"  # Version ID

            # MSA segment
            ack.add_segment("MSA")
            ack.msa.msa_1 = ack_code  # Acknowledgment Code
            ack.msa.msa_2 = original_msh.msh_10.value  # Message Control ID

            return str(ack)

        except Exception as e:
            self.logger.error(f"Failed to generate ACK: {e}")
            return ""

# Example usage
if __name__ == "__main__":
    # Example HL7 ADT message
    sample_hl7 = """MSH|^~\\&|SENDING_APP|SENDING_FACILITY|RECEIVING_APP|RECEIVING_FACILITY|20240101120000||ADT^A01|MSG123|P|2.5
EVN|A01|20240101120000
PID|1||PAT123^^^MR||DOE^JOHN^M^^||19800101|M|||123 MAIN ST^^ANYTOWN^NY^12345^USA||(555)123-4567|||||PAT123
PV1|1|I|WARD01^BEDS||R|||DR_SMITH^^^^^^^^^^NPI|||||||||ADM001|||||||||||||||||||||||||20240101120000
"""

    parser = HL7Parser()
    message = parser.parse_hl7_message(sample_hl7)

    if message:
        patient_info = parser.extract_patient_info(message)
        print("Patient Info:", patient_info)

        # Generate acknowledgment
        ack_message = parser.generate_ack(message)
        print("ACK Message:", ack_message)