"""
AUTOSAR ARXML Viewer - Main Application

This is the main entry point for the AUTOSAR ARXML Viewer desktop application.
"""

import tkinter as tk
from ui import ARXMLViewerUI


def main():
    """Main application entry point."""
    # Create root window
    root = tk.Tk()

    # Set application icon (optional)
    try:
        # You can add an icon file later if desired
        # root.iconbitmap('icon.ico')
        pass
    except:
        pass

    # Create the main UI
    app = ARXMLViewerUI(root)

    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    main()