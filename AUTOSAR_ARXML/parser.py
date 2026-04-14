"""
AUTOSAR ARXML Parser Module

This module contains functions for parsing AUTOSAR ARXML files and extracting
relevant information for the viewer application.
"""

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
import os


class ARXMLParser:
    """Main parser class for AUTOSAR ARXML files."""

    def __init__(self):
        self.root = None
        self.namespaces = {}
        self.parsed_data = {
            'ecu_info': [],
            'signals': [],
            'ports': [],
            'runnables': [],
            'software_components': [],
            'xml_tree': None
        }

    def load_file(self, file_path):
        """Load and parse an ARXML file."""
        try:
            # Register namespaces
            self.namespaces = {
                'autosar': 'http://autosar.org/schema/r4.0',
                'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
            }

            # Parse the XML file
            tree = ET.parse(file_path)
            self.root = tree.getroot()

            # Extract data
            self._extract_all_data()

            return True, "File loaded and parsed successfully"

        except ParseError as e:
            return False, f"XML parsing error: {str(e)}"
        except FileNotFoundError:
            return False, "File not found"
        except Exception as e:
            return False, f"Error loading file: {str(e)}"

    def _extract_all_data(self):
        """Extract all relevant data from the parsed XML."""
        if self.root is None:
            return

        # Extract different types of data
        self.parsed_data['ecu_info'] = self._parse_ecu_info()
        self.parsed_data['signals'] = self._parse_signals()
        self.parsed_data['ports'] = self._parse_ports()
        self.parsed_data['runnables'] = self._parse_runnables()
        self.parsed_data['software_components'] = self._parse_software_components()
        self.parsed_data['xml_tree'] = self._build_xml_tree()

    def _parse_ecu_info(self):
        """Parse ECU-related information."""
        ecu_data = []

        # Look for ECU instances
        for elem in self.root.iter():
            tag = self._strip_namespace(elem.tag)

            if tag in ['ECU-INSTANCE', 'ECU']:
                ecu_info = {}

                # Get ECU name
                short_name = self._find_child_text(elem, 'SHORT-NAME')
                if short_name:
                    ecu_info['name'] = short_name

                # Get ECU references if available
                ecu_ref = self._find_child_text(elem, 'ECU-REF')
                if ecu_ref:
                    ecu_info['reference'] = ecu_ref

                # Get description if available
                desc = self._find_child_text(elem, 'DESC')
                if desc:
                    ecu_info['description'] = desc

                if ecu_info:
                    ecu_data.append(ecu_info)

        return ecu_data

    def _parse_signals(self):
        """Parse signal information."""
        signals = []

        for elem in self.root.iter():
            tag = self._strip_namespace(elem.tag)

            if tag in ['SIGNAL', 'I-SIGNAL', 'SYSTEM-SIGNAL']:
                signal_info = {}

                # Signal name
                short_name = self._find_child_text(elem, 'SHORT-NAME')
                if short_name:
                    signal_info['name'] = short_name

                # Data type
                data_type = self._find_child_text(elem, 'DATA-TYPE')
                if data_type:
                    signal_info['data_type'] = data_type

                # Length
                length = self._find_child_text(elem, 'LENGTH')
                if length:
                    signal_info['length'] = length

                # Initial value
                init_value = self._find_child_text(elem, 'INIT-VALUE')
                if init_value:
                    signal_info['initial_value'] = init_value

                # Description
                desc = self._find_child_text(elem, 'DESC')
                if desc:
                    signal_info['description'] = desc

                if signal_info:
                    signals.append(signal_info)

        return signals

    def _parse_ports(self):
        """Parse port information."""
        ports = []

        for elem in self.root.iter():
            tag = self._strip_namespace(elem.tag)

            if tag in ['P-PORT-PROTOTYPE', 'R-PORT-PROTOTYPE', 'PORT-PROTOTYPE']:
                port_info = {}

                # Port name
                short_name = self._find_child_text(elem, 'SHORT-NAME')
                if short_name:
                    port_info['name'] = short_name

                # Port type (provided/required)
                if 'P-PORT' in tag:
                    port_info['type'] = 'Provided'
                elif 'R-PORT' in tag:
                    port_info['type'] = 'Required'
                else:
                    port_info['type'] = 'Unknown'

                # Interface reference
                interface_ref = self._find_child_text(elem, 'INTERFACE-REF')
                if interface_ref:
                    port_info['interface'] = interface_ref

                # Description
                desc = self._find_child_text(elem, 'DESC')
                if desc:
                    port_info['description'] = desc

                if port_info:
                    ports.append(port_info)

        return ports

    def _parse_runnables(self):
        """Parse runnable information."""
        runnables = []

        for elem in self.root.iter():
            tag = self._strip_namespace(elem.tag)

            if tag == 'RUNNABLE-ENTITY':
                runnable_info = {}

                # Runnable name
                short_name = self._find_child_text(elem, 'SHORT-NAME')
                if short_name:
                    runnable_info['name'] = short_name

                # Symbol
                symbol = self._find_child_text(elem, 'SYMBOL')
                if symbol:
                    runnable_info['symbol'] = symbol

                # Event reference
                event_ref = self._find_child_text(elem, 'EVENT-REF')
                if event_ref:
                    runnable_info['event_ref'] = event_ref

                if runnable_info:
                    runnables.append(runnable_info)

        return runnables

    def _parse_software_components(self):
        """Parse software component information."""
        components = []

        for elem in self.root.iter():
            tag = self._strip_namespace(elem.tag)

            if tag in ['APPLICATION-SW-COMPONENT-TYPE', 'SW-COMPONENT-TYPE', 'COMPOSITION-SW-COMPONENT-TYPE']:
                comp_info = {}

                # Component name
                short_name = self._find_child_text(elem, 'SHORT-NAME')
                if short_name:
                    comp_info['name'] = short_name

                # Component type
                if 'APPLICATION' in tag:
                    comp_info['type'] = 'Application'
                elif 'COMPOSITION' in tag:
                    comp_info['type'] = 'Composition'
                else:
                    comp_info['type'] = 'Generic'

                # Internal behaviors
                behaviors = []
                for behavior in elem.iter():
                    if self._strip_namespace(behavior.tag) == 'INTERNAL-BEHAVIOR':
                        behavior_name = self._find_child_text(behavior, 'SHORT-NAME')
                        if behavior_name:
                            behaviors.append(behavior_name)

                if behaviors:
                    comp_info['internal_behaviors'] = ', '.join(behaviors)

                if comp_info:
                    components.append(comp_info)

        return components

    def _build_xml_tree(self):
        """Build a tree structure for XML visualization."""
        def build_tree(element, path=""):
            """Recursively build tree from XML element."""
            tag = self._strip_namespace(element.tag)
            current_path = f"{path}/{tag}" if path else tag

            node = {
                'tag': tag,
                'path': current_path,
                'text': element.text.strip() if element.text else "",
                'children': []
            }

            for child in element:
                child_node = build_tree(child, current_path)
                if child_node:
                    node['children'].append(child_node)

            return node

        if self.root is not None:
            return build_tree(self.root)
        return None

    def _strip_namespace(self, tag):
        """Remove namespace from XML tag."""
        if '}' in tag:
            return tag.split('}', 1)[1]
        return tag

    def _find_child_text(self, parent, child_tag):
        """Find text content of a child element."""
        for child in parent:
            if self._strip_namespace(child.tag) == child_tag:
                return child.text
        return None

    def get_summary_counts(self):
        """Get summary counts for dashboard."""
        return {
            'ecu_count': len(self.parsed_data['ecu_info']),
            'signals_count': len(self.parsed_data['signals']),
            'ports_count': len(self.parsed_data['ports']),
            'runnables_count': len(self.parsed_data['runnables']),
            'components_count': len(self.parsed_data['software_components']),
            'xml_nodes_count': self._count_xml_nodes()
        }

    def _count_xml_nodes(self):
        """Count total XML nodes."""
        def count_nodes(element):
            count = 1  # Count current element
            for child in element:
                count += count_nodes(child)
            return count

        if self.root is not None:
            return count_nodes(self.root)
        return 0

    def search_data(self, keyword):
        """Search across all parsed data for a keyword."""
        results = {
            'ecu_info': [],
            'signals': [],
            'ports': [],
            'runnables': [],
            'software_components': []
        }

        keyword_lower = keyword.lower()

        # Search ECU info
        for item in self.parsed_data['ecu_info']:
            if any(keyword_lower in str(value).lower() for value in item.values()):
                results['ecu_info'].append(item)

        # Search signals
        for item in self.parsed_data['signals']:
            if any(keyword_lower in str(value).lower() for value in item.values()):
                results['signals'].append(item)

        # Search ports
        for item in self.parsed_data['ports']:
            if any(keyword_lower in str(value).lower() for value in item.values()):
                results['ports'].append(item)

        # Search runnables
        for item in self.parsed_data['runnables']:
            if any(keyword_lower in str(value).lower() for value in item.values()):
                results['runnables'].append(item)

        # Search software components
        for item in self.parsed_data['software_components']:
            if any(keyword_lower in str(value).lower() for value in item.values()):
                results['software_components'].append(item)

        return results

    def validate_arxml(self):
        """Validate the ARXML file for common AUTOSAR issues."""
        validation_results = []

        # Check for basic structure
        if self.root is None:
            validation_results.append({"type": "error", "message": "No valid XML structure found"})
            return validation_results

        # Check for ECU information
        ecu_count = len(self.parsed_data['ecu_info'])
        if ecu_count == 0:
            validation_results.append({"type": "warning", "message": "No ECU information found"})
        else:
            validation_results.append({"type": "ok", "message": f"{ecu_count} ECU(s) detected"})

        # Check for signals
        signal_count = len(self.parsed_data['signals'])
        if signal_count == 0:
            validation_results.append({"type": "warning", "message": "No signals configured"})
        else:
            validation_results.append({"type": "ok", "message": f"{signal_count} signal(s) found"})

        # Check for runnables
        runnable_count = len(self.parsed_data['runnables'])
        if runnable_count == 0:
            validation_results.append({"type": "warning", "message": "No runnables defined"})
        else:
            validation_results.append({"type": "ok", "message": f"{runnable_count} runnable(s) available"})

        # Check for duplicate names
        duplicates = self._find_duplicates()
        if duplicates:
            validation_results.append({"type": "error", "message": f"Duplicate names found in: {', '.join(duplicates)}"})
        else:
            validation_results.append({"type": "ok", "message": "No duplicate names detected"})

        return validation_results

    def _find_duplicates(self):
        """Find duplicate names across different data types."""
        duplicates = []

        # Check signals
        signal_names = [s.get('name') for s in self.parsed_data['signals'] if s.get('name')]
        if len(signal_names) != len(set(signal_names)):
            duplicates.append("signals")

        # Check ports
        port_names = [p.get('name') for p in self.parsed_data['ports'] if p.get('name')]
        if len(port_names) != len(set(port_names)):
            duplicates.append("ports")

        # Check runnables
        runnable_names = [r.get('name') for r in self.parsed_data['runnables'] if r.get('name')]
        if len(runnable_names) != len(set(runnable_names)):
            duplicates.append("runnables")

        # Check components
        component_names = [c.get('name') for c in self.parsed_data['software_components'] if c.get('name')]
        if len(component_names) != len(set(component_names)):
            duplicates.append("components")

        return duplicates