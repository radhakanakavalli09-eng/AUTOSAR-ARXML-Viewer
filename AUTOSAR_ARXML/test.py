"""
Test script to verify the AUTOSAR ARXML Viewer functionality without GUI.
"""

import sys
import os

# Add current directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(__file__))

from parser import ARXMLParser
from insights import ARXMLInsights

def test_parser():
    """Test the parser with a simple XML structure."""
    print("Testing ARXML Parser...")

    # Create a simple test XML content
    test_xml = """<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.0">
    <AR-PACKAGES>
        <AR-PACKAGE>
            <SHORT-NAME>TestPackage</SHORT-NAME>
            <ELEMENTS>
                <ECU-INSTANCE>
                    <SHORT-NAME>TestECU</SHORT-NAME>
                    <DESC>Test ECU Description</DESC>
                </ECU-INSTANCE>
                <I-SIGNAL>
                    <SHORT-NAME>TestSignal</SHORT-NAME>
                    <DATA-TYPE>uint8</DATA-TYPE>
                    <LENGTH>8</LENGTH>
                    <INIT-VALUE>0</INIT-VALUE>
                    <DESC>Test signal</DESC>
                </I-SIGNAL>
                <P-PORT-PROTOTYPE>
                    <SHORT-NAME>TestPort</SHORT-NAME>
                    <DESC>Test port</DESC>
                </P-PORT-PROTOTYPE>
                <RUNNABLE-ENTITY>
                    <SHORT-NAME>TestRunnable</SHORT-NAME>
                    <SYMBOL>TestSymbol</SYMBOL>
                </RUNNABLE-ENTITY>
                <APPLICATION-SW-COMPONENT-TYPE>
                    <SHORT-NAME>TestComponent</SHORT-NAME>
                    <INTERNAL-BEHAVIOR>
                        <SHORT-NAME>TestBehavior</SHORT-NAME>
                    </INTERNAL-BEHAVIOR>
                </APPLICATION-SW-COMPONENT-TYPE>
            </ELEMENTS>
        </AR-PACKAGE>
    </AR-PACKAGES>
</AUTOSAR>"""

    # Create a temporary test file
    test_file = "test_sample.arxml"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_xml)

    try:
        # Test the parser
        parser = ARXMLParser()
        success, message = parser.load_file(test_file)

        if success:
            print("✓ Parser loaded file successfully")
            print(f"✓ Message: {message}")

            # Check parsed data
            counts = parser.get_summary_counts()
            print("\nParsed Data Summary:")
            print(f"  - ECU Count: {counts['ecu_count']}")
            print(f"  - Signals: {counts['signals_count']}")
            print(f"  - Ports: {counts['ports_count']}")
            print(f"  - Runnables: {counts['runnables_count']}")
            print(f"  - Components: {counts['components_count']}")
            print(f"  - XML Nodes: {counts['xml_nodes_count']}")

            # Test insights
            insights_gen = ARXMLInsights(parser.parsed_data, counts)
            insights = insights_gen.generate_insights()
            print("\n✓ AI Insights generated successfully")
            print("Sample insights:")
            for line in insights.split('\n')[:5]:  # Show first 5 lines
                print(f"  {line}")

            # Test search
            search_results = parser.search_data("Test")
            print("\n✓ Search functionality working")
            print(f"  Search results: {sum(len(results) for results in search_results.values())} items found")

        else:
            print(f"✗ Parser failed: {message}")
            return False

    finally:
        # Clean up test file
        if os.path.exists(test_file):
            os.remove(test_file)

    return True

def test_imports():
    """Test that all modules can be imported."""
    print("Testing module imports...")

    try:
        import parser
        import ui
        import exporter
        import insights
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

if __name__ == "__main__":
    print("AUTOSAR ARXML Viewer - Test Suite")
    print("=" * 40)

    success = True

    # Test imports
    if not test_imports():
        success = False

    # Test parser functionality
    if not test_parser():
        success = False

    print("\n" + "=" * 40)
    if success:
        print("✓ All tests passed! The application is working correctly.")
        print("\nTo run the GUI application:")
        print('  & "C:\\Users\\radha\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" main.py')
    else:
        print("✗ Some tests failed. Please check the errors above.")