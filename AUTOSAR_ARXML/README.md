# AUTOSAR ARXML Viewer

A professional Python Tkinter desktop application for **validating, analyzing, and engineering** AUTOSAR ARXML files with advanced automotive tooling features.

## Features

- **File Loading**: Load and validate AUTOSAR ARXML files with error handling
- **Dashboard**: Summary overview with key metrics and network complexity scoring
- **XML Structure Viewer**: Interactive tree view with detailed tag inspector panel
- **AUTOSAR Validation**: Comprehensive validation checks with color-coded results
- **Signal Mapping**: Relationship mapping between signals, ports, and components
- **Global Search**: Advanced search with result counts and filtering
- **Data Extraction Tabs**:
  - ECU Information
  - Signals (name, data type, length, initial value, description)
  - Ports (provided/required, interface references)
  - Runnables (symbol, event references)
  - Software Components (type, internal behaviors)
- **AI Insights**: Smart analysis with warnings, recommendations, and configuration type detection
- **Export Functionality**: CSV exports and comprehensive validation reports
- **Professional UI**: Clean, modern interface with validation indicators and status updates

## Installation

1. Ensure Python 3.6+ is installed (Tkinter is included in standard Python)
2. Clone or download this repository
3. No additional dependencies required - uses only Python standard library

## How to Run

```bash
python main.py
```

## Usage

1. Launch the application
2. Click "Load ARXML File" to select an AUTOSAR ARXML file
3. Navigate through the tabs to view different aspects of the data
4. Use the search bar to find specific items
5. Export data using the export buttons in each tab

## Example Use Case

This tool is designed for automotive engineers working with AUTOSAR configurations. Load an ARXML file exported from tools like Vector DaVinci or EB tresos to:

- Quickly assess the complexity of an AUTOSAR system
- Extract signal definitions for documentation
- Analyze port configurations for integration testing
- Review runnable configurations for software architecture
- Generate reports from the dashboard and exports

## Screenshots

*[Add screenshots here after implementation]*

## Project Structure

```
AUTOSAR_ARXML/
├── main.py          # Main application entry point
├── parser.py        # ARXML parsing functions
├── ui.py            # GUI components and layout
├── exporter.py      # Data export functionality
├── insights.py      # AI insights generation
├── README.md        # This file
└── requirements.txt # Dependencies
```

## Future Improvements

- Support for additional AUTOSAR versions
- Advanced filtering and sorting options
- Integration with AUTOSAR databases
- Batch processing of multiple ARXML files
- Custom report generation
- Dark mode theme option

## License

[Add license information]

## Contributing

[Add contribution guidelines]