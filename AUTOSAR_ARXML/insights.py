"""
AUTOSAR ARXML Insights Module

This module generates intelligent insights and observations from parsed ARXML data.
"""

class ARXMLInsights:
    """Generates insights from ARXML data using Python logic."""

    def __init__(self, parsed_data, summary_counts):
        self.parsed_data = parsed_data
        self.summary_counts = summary_counts

    def generate_insights(self):
        """Generate comprehensive insights text."""
        insights = []

        # Basic counts
        insights.append(f"{self.summary_counts['ecu_count']} ECU{'s' if self.summary_counts['ecu_count'] != 1 else ''} detected in this ARXML file")
        insights.append(f"{self.summary_counts['signals_count']} signal{'s' if self.summary_counts['signals_count'] != 1 else ''} found")
        insights.append(f"{self.summary_counts['ports_count']} port{'s' if self.summary_counts['ports_count'] != 1 else ''} configured")
        insights.append(f"{self.summary_counts['runnables_count']} runnable{'s' if self.summary_counts['runnables_count'] != 1 else ''} available")
        insights.append(f"{self.summary_counts['components_count']} software component{'s' if self.summary_counts['components_count'] != 1 else ''} identified")

        insights.append("")  # Empty line

        # Configuration type analysis
        config_type = self._analyze_configuration_type()
        insights.append(f"This ARXML appears to describe a {config_type} AUTOSAR configuration")

        insights.append("")  # Empty line
        insights.append("⚠ WARNINGS:")
        insights.append("-" * 12)

        # Enhanced warnings
        warnings = self._generate_warnings()
        insights.extend(warnings)

        insights.append("")  # Empty line
        insights.append("💡 RECOMMENDATIONS:")
        insights.append("-" * 18)

        # Add recommendations
        recommendations = self._generate_recommendations()
        insights.extend(recommendations)

        insights.append("")  # Empty line
        insights.append("📊 OBSERVATIONS:")
        insights.append("-" * 15)

        # Detailed observations
        observations = self._generate_observations()
        insights.extend(observations)

        return "\n".join(insights)

    def _analyze_configuration_type(self):
        """Analyze the type of AUTOSAR configuration."""
        signals = self.summary_counts['signals_count']
        ports = self.summary_counts['ports_count']
        runnables = self.summary_counts['runnables_count']
        components = self.summary_counts['components_count']

        # Simple heuristic-based analysis
        if signals > ports and runnables > 0:
            return "communication-oriented"
        elif components > signals:
            return "component-focused"
        elif runnables == 0 and signals > 0:
            return "signal-definition"
        elif ports > signals:
            return "interface-heavy"
        else:
            return "balanced"

    def _generate_observations(self):
        """Generate detailed observations."""
        observations = []

        # Signal analysis
        if self.summary_counts['signals_count'] > 50:
            observations.append("Large number of signals detected - complex communication system")
        elif self.summary_counts['signals_count'] == 0:
            observations.append("No signals found - may be a component-only configuration")
        elif self.summary_counts['signals_count'] < 10:
            observations.append("Limited signal configuration - simple system")

        # Runnable analysis
        if self.summary_counts['runnables_count'] == 0:
            observations.append("No runnables found - may be a static configuration")
        elif self.summary_counts['runnables_count'] > 20:
            observations.append("High number of runnables - complex software architecture")

        # Port analysis
        if self.summary_counts['ports_count'] == 0:
            observations.append("No ports configured - internal component only")
        elif self.summary_counts['ports_count'] < 5:
            observations.append("Port configuration appears limited - minimal interfaces")
        elif self.summary_counts['ports_count'] > 30:
            observations.append("Extensive port configuration - highly interconnected system")

        # Component analysis
        if self.summary_counts['components_count'] == 0:
            observations.append("No software components found - basic ECU configuration")
        elif self.summary_counts['components_count'] > 10:
            observations.append("Multiple software components - modular architecture")

        # ECU analysis
        if self.summary_counts['ecu_count'] == 0:
            observations.append("No ECU information found - may be a partial configuration")
        elif self.summary_counts['ecu_count'] > 5:
            observations.append("Multiple ECUs detected - distributed system")

        # Data type diversity
        signal_types = set()
        for signal in self.parsed_data['signals']:
            if 'data_type' in signal and signal['data_type']:
                signal_types.add(signal['data_type'])

        if len(signal_types) > 5:
            observations.append("Diverse signal data types - mixed signal processing")
        elif len(signal_types) <= 2:
            observations.append("Limited signal data types - specialized application")

        # Port type balance
        provided_ports = sum(1 for port in self.parsed_data['ports'] if port.get('type') == 'Provided')
        required_ports = sum(1 for port in self.parsed_data['ports'] if port.get('type') == 'Required')

        if provided_ports > required_ports * 2:
            observations.append("More provided than required ports - service-oriented component")
        elif required_ports > provided_ports * 2:
            observations.append("More required than provided ports - client-oriented component")

        # Component complexity
        avg_behaviors = 0
        if self.parsed_data['software_components']:
            total_behaviors = sum(len(comp.get('internal_behaviors', '').split(', ')) if comp.get('internal_behaviors') else 0
                                for comp in self.parsed_data['software_components'])
            avg_behaviors = total_behaviors / len(self.parsed_data['software_components'])

        if avg_behaviors > 3:
            observations.append("Components have multiple internal behaviors - complex implementations")
        elif avg_behaviors == 0:
            observations.append("Components lack internal behavior definitions - basic implementations")

        # If no specific observations, add a general one
        if not observations:
            observations.append("Standard AUTOSAR configuration detected")

        return observations

    def _generate_warnings(self):
        """Generate warnings based on configuration analysis."""
        warnings = []

        if self.summary_counts['runnables_count'] == 0:
            warnings.append("No runnables detected → incomplete configuration")

        if self.summary_counts['signals_count'] == 0:
            warnings.append("No signals found → communication configuration missing")

        if self.summary_counts['ecu_count'] == 0:
            warnings.append("No ECU information → basic configuration only")

        # Check for unconnected ports (simplified check)
        unconnected_ports = sum(1 for port in self.parsed_data['ports'] if not port.get('interface'))
        if unconnected_ports > 0:
            warnings.append(f"{unconnected_ports} ports without interface references → incomplete port configuration")

        # Check for components without behaviors
        components_without_behaviors = sum(1 for comp in self.parsed_data['software_components']
                                         if not comp.get('internal_behaviors'))
        if components_without_behaviors > 0:
            warnings.append(f"{components_without_behaviors} components lack internal behavior definitions")

        if not warnings:
            warnings.append("No critical issues detected")

        return warnings

    def _generate_recommendations(self):
        """Generate recommendations for improvement."""
        recommendations = []

        if self.summary_counts['runnables_count'] == 0:
            recommendations.append("Consider verifying runnable configurations for complete software architecture")

        if self.summary_counts['signals_count'] > 20:
            recommendations.append("High signal count detected - review signal routing efficiency")

        if self.summary_counts['ports_count'] < 5:
            recommendations.append("Limited port configuration - consider expanding interface definitions")

        if self.summary_counts['components_count'] > 10:
            recommendations.append("Multiple components detected - ensure proper component communication")

        # Check signal to port ratio
        if self.summary_counts['signals_count'] > 0 and self.summary_counts['ports_count'] > 0:
            ratio = self.summary_counts['signals_count'] / self.summary_counts['ports_count']
            if ratio > 5:
                recommendations.append("High signals-to-ports ratio - consider optimizing port usage")

        if not recommendations:
            recommendations.append("Configuration appears well-structured")

        return recommendations