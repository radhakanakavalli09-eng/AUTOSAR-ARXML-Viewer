"""
AUTOSAR ARXML Viewer UI Module

This module contains the GUI components and layout for the ARXML Viewer application.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from parser import ARXMLParser
from exporter import ARXMLExporter
from insights import ARXMLInsights


class ARXMLViewerUI:
    """Main UI class for the ARXML Viewer application."""

    def __init__(self, root):
        self.root = root
        self.root.title("AUTOSAR ARXML Viewer")
        self.root.geometry("1200x800")

        # Initialize parser and data
        self.parser = ARXMLParser()
        self.current_file = None
        self.search_results = None

        # Create main UI components
        self._create_header()
        self._create_search_bar()
        self._create_notebook()
        self._create_status_bar()

        # Initialize tabs
        self._setup_dashboard_tab()
        self._setup_xml_structure_tab()
        self._setup_validation_tab()
        self._setup_signal_mapping_tab()
        self._setup_ecu_tab()
        self._setup_signals_tab()
        self._setup_ports_tab()
        self._setup_runnables_tab()
        self._setup_components_tab()
        self._setup_insights_tab()

    def _create_header(self):
        """Create the application header."""
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.pack(fill=tk.X, side=tk.TOP)

        # Title
        title_label = ttk.Label(header_frame, text="AUTOSAR ARXML Viewer",
                               font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT)

        # File info
        self.file_info_frame = ttk.Frame(header_frame)
        self.file_info_frame.pack(side=tk.RIGHT)

        ttk.Label(self.file_info_frame, text="File:").grid(row=0, column=0, sticky=tk.W)
        self.file_name_label = ttk.Label(self.file_info_frame, text="No file loaded",
                                        font=("Arial", 10, "italic"))
        self.file_name_label.grid(row=0, column=1, padx=(5,0), sticky=tk.W)

        ttk.Label(self.file_info_frame, text="Status:").grid(row=1, column=0, sticky=tk.W)
        self.file_status_label = ttk.Label(self.file_info_frame, text="Not Loaded",
                                          foreground="red")
        self.file_status_label.grid(row=1, column=1, padx=(5,0), sticky=tk.W)

        # Load button
        self.load_button = ttk.Button(header_frame, text="Load ARXML File",
                                     command=self._load_file)
        self.load_button.pack(side=tk.RIGHT, padx=(10,0))

    def _create_search_bar(self):
        """Create the global search bar."""
        search_frame = ttk.Frame(self.root, padding="5")
        search_frame.pack(fill=tk.X, side=tk.TOP)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=(5,10))

        self.search_button = ttk.Button(search_frame, text="Search",
                                       command=self._perform_search)
        self.search_button.pack(side=tk.LEFT, padx=(0,5))

        self.reset_button = ttk.Button(search_frame, text="Reset",
                                      command=self._reset_search)
        self.reset_button.pack(side=tk.LEFT)

    def _create_notebook(self):
        """Create the main notebook with tabs."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tab frames
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.xml_frame = ttk.Frame(self.notebook)
        self.validation_frame = ttk.Frame(self.notebook)
        self.signal_mapping_frame = ttk.Frame(self.notebook)
        self.ecu_frame = ttk.Frame(self.notebook)
        self.signals_frame = ttk.Frame(self.notebook)
        self.ports_frame = ttk.Frame(self.notebook)
        self.runnables_frame = ttk.Frame(self.notebook)
        self.components_frame = ttk.Frame(self.notebook)
        self.insights_frame = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        self.notebook.add(self.xml_frame, text="XML Structure")
        self.notebook.add(self.validation_frame, text="Validation")
        self.notebook.add(self.signal_mapping_frame, text="Signal Mapping")
        self.notebook.add(self.ecu_frame, text="ECU Info")
        self.notebook.add(self.signals_frame, text="Signals")
        self.notebook.add(self.ports_frame, text="Ports")
        self.notebook.add(self.runnables_frame, text="Runnables")
        self.notebook.add(self.components_frame, text="Software Components")
        self.notebook.add(self.insights_frame, text="AI Insights")

    def _create_status_bar(self):
        """Create the status bar at the bottom."""
        self.status_frame = ttk.Frame(self.root, relief=tk.SUNKEN, padding="2")
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = ttk.Label(self.status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)

        self.items_label = ttk.Label(self.status_frame, text="Items: 0")
        self.items_label.pack(side=tk.RIGHT)

    def _setup_dashboard_tab(self):
        """Setup the dashboard tab with summary cards."""
        # Create a canvas with scrollbar for the dashboard
        canvas = tk.Canvas(self.dashboard_frame)
        scrollbar = ttk.Scrollbar(self.dashboard_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create summary cards
        self.summary_cards = {}
        card_titles = [
            ("ECU Count", "ecu_count"),
            ("Signals", "signals_count"),
            ("Ports", "ports_count"),
            ("Runnables", "runnables_count"),
            ("Software Components", "components_count"),
            ("XML Nodes", "xml_nodes_count"),
            ("Network Complexity", "complexity_score")
        ]

        for i, (title, key) in enumerate(card_titles):
            card_frame = ttk.LabelFrame(scrollable_frame, text=title, padding="10")
            card_frame.grid(row=i//3, column=i%3, padx=10, pady=10, sticky=tk.NSEW)

            if key == "complexity_score":
                self.summary_cards[key] = ttk.Label(card_frame, text="Not Calculated",
                                                  font=("Arial", 14, "bold"))
            else:
                self.summary_cards[key] = ttk.Label(card_frame, text="0",
                                                  font=("Arial", 24, "bold"))
            self.summary_cards[key].pack()

        # Export button
        export_frame = ttk.Frame(scrollable_frame)
        export_frame.grid(row=2, column=0, columnspan=3, pady=20)

        self.dashboard_export_button = ttk.Button(export_frame,
                                                 text="Export Dashboard Summary",
                                                 command=self._export_dashboard)
        self.dashboard_export_button.pack()

    def _setup_xml_structure_tab(self):
        """Setup the XML structure tab with tree view and details panel."""
        # Create paned window for tree and details
        paned = ttk.PanedWindow(self.xml_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel - Tree view
        tree_frame = ttk.Frame(paned)
        paned.add(tree_frame, weight=2)

        # Treeview
        self.xml_tree = ttk.Treeview(tree_frame)
        self.xml_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbars for tree
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.xml_tree.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.xml_tree.configure(yscrollcommand=v_scrollbar.set)

        # Right panel - Details
        details_frame = ttk.Frame(paned)
        paned.add(details_frame, weight=1)

        ttk.Label(details_frame, text="XML Tag Details", font=("Arial", 12, "bold")).pack(pady=(0,10))

        # Details text area
        self.details_text = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD, height=20)
        self.details_text.pack(fill=tk.BOTH, expand=True)

        # Configure treeview columns
        self.xml_tree.heading("#0", text="XML Structure")

        # Bind selection event for details panel
        self.xml_tree.bind('<<TreeviewSelect>>', self._on_xml_tree_select)

    def _setup_validation_tab(self):
        """Setup the validation tab."""
        validation_frame = ttk.Frame(self.validation_frame, padding="10")
        validation_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(validation_frame, text="AUTOSAR Validation Results",
                 font=("Arial", 14, "bold")).pack(pady=(0,10))

        # Create scrolled text for validation results
        self.validation_text = scrolledtext.ScrolledText(validation_frame, wrap=tk.WORD,
                                                        height=20, state=tk.DISABLED)
        self.validation_text.pack(fill=tk.BOTH, expand=True)

        # Export button
        self.validation_export_button = ttk.Button(validation_frame,
                                                  text="Export Validation Report",
                                                  command=self._export_validation_report)
        self.validation_export_button.pack(pady=10)

    def _setup_signal_mapping_tab(self):
        """Setup the signal mapping tab."""
        mapping_frame = ttk.Frame(self.signal_mapping_frame, padding="10")
        mapping_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(mapping_frame, text="Signal Relationship Mapping",
                 font=("Arial", 14, "bold")).pack(pady=(0,10))

        # Create treeview for signal mapping
        tree_frame = ttk.Frame(mapping_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.signal_mapping_tree = ttk.Treeview(tree_frame, columns=["Signal", "Port", "Component"],
                                               show="headings", height=15)

        # Configure columns
        for col in ["Signal", "Port", "Component"]:
            self.signal_mapping_tree.heading(col, text=col)
            self.signal_mapping_tree.column(col, width=200, minwidth=150)

        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.signal_mapping_tree.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        h_scrollbar = ttk.Scrollbar(mapping_frame, orient=tk.HORIZONTAL, command=self.signal_mapping_tree.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.signal_mapping_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.signal_mapping_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _setup_ecu_tab(self):
        """Setup the ECU information tab."""
        self._create_data_tab(self.ecu_frame, "ECU Information",
                             ["Name", "Reference", "Description"])

    def _setup_signals_tab(self):
        """Setup the signals tab."""
        frame = self._create_data_tab(self.signals_frame, "Signals",
                                     ["Name", "Data Type", "Length", "Initial Value", "Description"])
        # Add export button
        self.signals_export_button = ttk.Button(frame, text="Export to CSV",
                                               command=self._export_signals)
        self.signals_export_button.pack(pady=5)

    def _setup_ports_tab(self):
        """Setup the ports tab."""
        frame = self._create_data_tab(self.ports_frame, "Ports",
                                     ["Name", "Type", "Interface", "Description"])
        # Add export button
        self.ports_export_button = ttk.Button(frame, text="Export to CSV",
                                             command=self._export_ports)
        self.ports_export_button.pack(pady=5)

    def _setup_runnables_tab(self):
        """Setup the runnables tab."""
        frame = self._create_data_tab(self.runnables_frame, "Runnables",
                                     ["Name", "Symbol", "Event Reference"])
        # Add export button
        self.runnables_export_button = ttk.Button(frame, text="Export to CSV",
                                                 command=self._export_runnables)
        self.runnables_export_button.pack(pady=5)

    def _setup_components_tab(self):
        """Setup the software components tab."""
        frame = self._create_data_tab(self.components_frame, "Software Components",
                                     ["Name", "Type", "Internal Behaviors"])
        # Add export button
        self.components_export_button = ttk.Button(frame, text="Export to CSV",
                                                  command=self._export_components)
        self.components_export_button.pack(pady=5)

    def _setup_insights_tab(self):
        """Setup the AI insights tab."""
        insights_frame = ttk.Frame(self.insights_frame, padding="10")
        insights_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(insights_frame, text="AI Insights",
                 font=("Arial", 14, "bold")).pack(pady=(0,10))

        # Create scrolled text for insights
        self.insights_text = scrolledtext.ScrolledText(insights_frame, wrap=tk.WORD,
                                                      height=20, state=tk.DISABLED)
        self.insights_text.pack(fill=tk.BOTH, expand=True)

    def _create_data_tab(self, parent_frame, title, columns):
        """Create a standard data tab with treeview."""
        frame = ttk.Frame(parent_frame, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=title, font=("Arial", 14, "bold")).pack(pady=(0,10))

        # Create treeview with scrollbars
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        treeview = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        # Configure columns
        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=150, minwidth=100)

        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=treeview.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        h_scrollbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=treeview.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        treeview.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Store reference to treeview
        setattr(self, f"{title.lower().replace(' ', '_')}_tree", treeview)

        return frame

    def _load_file(self):
        """Load an ARXML file."""
        file_path = filedialog.askopenfilename(
            title="Select ARXML File",
            filetypes=[("ARXML files", "*.arxml"), ("XML files", "*.xml"), ("All files", "*.*")]
        )

        if not file_path:
            return

        # Update status
        self.status_label.config(text="Parsing file...")
        self.root.update()

        # Load and parse file
        success, message = self.parser.load_file(file_path)

        if success:
            self.current_file = file_path
            self._update_ui_after_load()
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
            self.status_label.config(text="Load failed")

    def _update_ui_after_load(self):
        """Update UI after successful file load."""
        # Update header
        file_name = os.path.basename(self.current_file)
        self.file_name_label.config(text=file_name)
        self.file_status_label.config(text="Loaded", foreground="green")

        # Update dashboard
        self._update_dashboard()

        # Update data tabs
        self._update_data_tabs()

        # Update XML tree
        self._update_xml_tree()

        # Update insights
        self._update_insights()

        # Update status
        total_items = sum(len(data) for data in self.parser.parsed_data.values()
                         if isinstance(data, list))
        self.items_label.config(text=f"Items: {total_items}")
        self.status_label.config(text="Ready")

    def _update_dashboard(self):
        """Update dashboard with current data."""
        counts = self.parser.get_summary_counts()
        for key, value in counts.items():
            if key in self.summary_cards:
                self.summary_cards[key].config(text=str(value))

    def _update_data_tabs(self):
        """Update all data tabs with parsed information."""
        # Clear existing data
        for tree_name in ['ecu_information_tree', 'signals_tree', 'ports_tree',
                         'runnables_tree', 'software_components_tree']:
            tree = getattr(self, tree_name, None)
            if tree:
                for item in tree.get_children():
                    tree.delete(item)

        # Update ECU tab
        for ecu in self.parser.parsed_data['ecu_info']:
            self.ecu_information_tree.insert("", tk.END, values=(
                ecu.get('name', ''),
                ecu.get('reference', ''),
                ecu.get('description', '')
            ))

        # Update signals tab
        for signal in self.parser.parsed_data['signals']:
            self.signals_tree.insert("", tk.END, values=(
                signal.get('name', ''),
                signal.get('data_type', ''),
                signal.get('length', ''),
                signal.get('initial_value', ''),
                signal.get('description', '')
            ))

        # Update ports tab
        for port in self.parser.parsed_data['ports']:
            self.ports_tree.insert("", tk.END, values=(
                port.get('name', ''),
                port.get('type', ''),
                port.get('interface', ''),
                port.get('description', '')
            ))

        # Update runnables tab
        for runnable in self.parser.parsed_data['runnables']:
            self.runnables_tree.insert("", tk.END, values=(
                runnable.get('name', ''),
                runnable.get('symbol', ''),
                runnable.get('event_ref', '')
            ))

        # Update components tab
        for component in self.parser.parsed_data['software_components']:
            self.software_components_tree.insert("", tk.END, values=(
                component.get('name', ''),
                component.get('type', ''),
                component.get('internal_behaviors', '')
            ))

    def _update_xml_tree(self):
        """Update the XML structure tree."""
        # Clear existing tree
        for item in self.xml_tree.get_children():
            self.xml_tree.delete(item)

        def add_tree_node(parent, node_data):
            """Recursively add nodes to tree."""
            text = f"{node_data['tag']}"
            if node_data['text']:
                text += f" ({node_data['text'][:50]}...)" if len(node_data['text']) > 50 else f" ({node_data['text']})"

            item_id = self.xml_tree.insert(parent, tk.END, text=text)

            for child in node_data['children']:
                add_tree_node(item_id, child)

        if self.parser.parsed_data['xml_tree']:
            add_tree_node("", self.parser.parsed_data['xml_tree'])

    def _update_insights(self):
        """Update the AI insights tab."""
        counts = self.parser.get_summary_counts()
        insights_generator = ARXMLInsights(self.parser.parsed_data, counts)
        insights_text = insights_generator.generate_insights()

        self.insights_text.config(state=tk.NORMAL)
        self.insights_text.delete(1.0, tk.END)
        self.insights_text.insert(tk.END, insights_text)
        self.insights_text.config(state=tk.DISABLED)

    def _perform_search(self):
        """Perform global search across all data."""
        keyword = self.search_var.get().strip()
        if not keyword:
            return

        # Search data
        self.search_results = self.parser.search_data(keyword)

        # Update status
        self.status_label.config(text=f"Search results for: {keyword}")

        # Update tabs with search results
        self._update_data_tabs_with_search()

    def _reset_search(self):
        """Reset search and show all data."""
        self.search_var.set("")
        self.search_results = None
        self.status_label.config(text="Ready")
        self._update_data_tabs()

    def _update_data_tabs_with_search(self):
        """Update data tabs with search results."""
        if not self.search_results:
            return

        # Update each tab with filtered results
        trees_and_data = [
            ('ecu_information_tree', 'ecu_info'),
            ('signals_tree', 'signals'),
            ('ports_tree', 'ports'),
            ('runnables_tree', 'runnables'),
            ('software_components_tree', 'software_components')
        ]

        for tree_name, data_key in trees_and_data:
            tree = getattr(self, tree_name)
            # Clear tree
            for item in tree.get_children():
                tree.delete(item)

            # Add search results
            data = self.search_results[data_key]
            for item in data:
                if data_key == 'ecu_info':
                    tree.insert("", tk.END, values=(
                        item.get('name', ''),
                        item.get('reference', ''),
                        item.get('description', '')
                    ))
                elif data_key == 'signals':
                    tree.insert("", tk.END, values=(
                        item.get('name', ''),
                        item.get('data_type', ''),
                        item.get('length', ''),
                        item.get('initial_value', ''),
                        item.get('description', '')
                    ))
                elif data_key == 'ports':
                    tree.insert("", tk.END, values=(
                        item.get('name', ''),
                        item.get('type', ''),
                        item.get('interface', ''),
                        item.get('description', '')
                    ))
                elif data_key == 'runnables':
                    tree.insert("", tk.END, values=(
                        item.get('name', ''),
                        item.get('symbol', ''),
                        item.get('event_ref', '')
                    ))
                elif data_key == 'software_components':
                    tree.insert("", tk.END, values=(
                        item.get('name', ''),
                        item.get('type', ''),
                        item.get('internal_behaviors', '')
                    ))

    def _export_dashboard(self):
        """Export dashboard summary."""
        if not self.current_file:
            messagebox.showwarning("Warning", "No file loaded")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="dashboard_summary.txt"
        )

        if not file_path:
            return

        exporter = ARXMLExporter(self.parser.parsed_data)
        counts = self.parser.get_summary_counts()
        success, message = exporter.export_dashboard_txt(file_path, counts)

        if success:
            exporter.show_export_success(message)
        else:
            exporter.show_export_error(message)

    def _export_signals(self):
        """Export signals to CSV."""
        self._export_data('signals', 'signals')

    def _export_ports(self):
        """Export ports to CSV."""
        self._export_data('ports', 'ports')

    def _export_runnables(self):
        """Export runnables to CSV."""
        self._export_data('runnables', 'runnables')

    def _export_components(self):
        """Export components to CSV."""
        self._export_data('software_components', 'components')

    def _export_data(self, data_key, export_type):
        """Generic export function."""
        if not self.current_file:
            messagebox.showwarning("Warning", "No file loaded")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"autosar_{export_type}.csv"
        )

        if not file_path:
            return

        exporter = ARXMLExporter(self.parser.parsed_data)

        if export_type == 'signals':
            success, message = exporter.export_signals_csv(file_path)
        elif export_type == 'ports':
            success, message = exporter.export_ports_csv(file_path)
        elif export_type == 'runnables':
            success, message = exporter.export_runnables_csv(file_path)
        elif export_type == 'components':
            success, message = exporter.export_components_csv(file_path)

        if success:
            exporter.show_export_success(message)
        else:
            exporter.show_export_error(message)

    def _on_xml_tree_select(self, event):
        """Handle XML tree selection to show details."""
        selected_items = self.xml_tree.selection()
        if not selected_items:
            return

        item = selected_items[0]
        item_text = self.xml_tree.item(item, 'text')

        # Get the full path and details
        details = f"Tag: {item_text}\n\n"

        # For now, show basic info. In a full implementation, you'd store
        # the actual XML element data when building the tree
        details += "Attributes: None\n"
        details += "Value: (click to see full content)\n\n"
        details += "Note: This is a basic XML inspector. Full attribute\n"
        details += "and namespace information would be available in a\n"
        details += "complete implementation."

        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, details)

    def _update_dashboard(self):
        """Update dashboard with current data."""
        counts = self.parser.get_summary_counts()

        # Calculate complexity score
        complexity = self._calculate_complexity_score(counts)
        counts['complexity_score'] = complexity

        for key, value in counts.items():
            if key in self.summary_cards:
                if key == 'complexity_score':
                    self.summary_cards[key].config(text=str(value))
                else:
                    self.summary_cards[key].config(text=str(value))

        # Update validation and signal mapping
        self._update_validation_tab()
        self._update_signal_mapping_tab()

    def _calculate_complexity_score(self, counts):
        """Calculate network complexity score."""
        signals = counts['signals_count']
        components = counts['components_count']
        ports = counts['ports_count']

        # Simple complexity calculation
        score = signals * 0.3 + components * 0.4 + ports * 0.3

        if score < 10:
            return "Low"
        elif score < 50:
            return "Medium"
        else:
            return "High"

    def _update_validation_tab(self):
        """Update the validation tab with current validation results."""
        validation_results = self._perform_validation()

        self.validation_text.config(state=tk.NORMAL)
        self.validation_text.delete(1.0, tk.END)

        for result in validation_results:
            self.validation_text.insert(tk.END, result + "\n")

        self.validation_text.config(state=tk.DISABLED)

    def _perform_validation(self):
        """Perform AUTOSAR validation checks."""
        results = []
        counts = self.parser.get_summary_counts()

        # ECU validation
        if counts['ecu_count'] == 0:
            results.append("⚠ Missing ECU name - No ECU information found")
        else:
            results.append("✔ ECU information present")

        # Signals validation
        if counts['signals_count'] == 0:
            results.append("⚠ No signals found - Empty signal configuration")
        else:
            results.append("✔ Signals configuration present")

        # Runnables validation
        if counts['runnables_count'] == 0:
            results.append("⚠ No runnables present - Static configuration only")
        else:
            results.append("✔ Runnables configuration present")

        # Duplicate names check
        duplicates = self._check_duplicates()
        if duplicates:
            results.append(f"⚠ Duplicate names found: {', '.join(duplicates)}")
        else:
            results.append("✔ No duplicate names detected")

        # Port connections (basic check)
        unconnected_ports = self._check_port_connections()
        if unconnected_ports > 0:
            results.append(f"⚠ {unconnected_ports} ports without interface references")
        else:
            results.append("✔ All ports have interface references")

        return results

    def _check_duplicates(self):
        """Check for duplicate names across all data types."""
        duplicates = []

        # Check signal names
        signal_names = [s.get('name', '') for s in self.parser.parsed_data['signals'] if s.get('name')]
        if len(signal_names) != len(set(signal_names)):
            duplicates.append("signals")

        # Check port names
        port_names = [p.get('name', '') for p in self.parser.parsed_data['ports'] if p.get('name')]
        if len(port_names) != len(set(port_names)):
            duplicates.append("ports")

        # Check runnable names
        runnable_names = [r.get('name', '') for r in self.parser.parsed_data['runnables'] if r.get('name')]
        if len(runnable_names) != len(set(runnable_names)):
            duplicates.append("runnables")

        # Check component names
        component_names = [c.get('name', '') for c in self.parser.parsed_data['software_components'] if c.get('name')]
        if len(component_names) != len(set(component_names)):
            duplicates.append("components")

        return duplicates

    def _check_port_connections(self):
        """Check for ports without interface connections."""
        unconnected = 0
        for port in self.parser.parsed_data['ports']:
            if not port.get('interface'):
                unconnected += 1
        return unconnected

    def _update_signal_mapping_tab(self):
        """Update the signal mapping tab with relationships."""
        # Clear existing data
        for item in self.signal_mapping_tree.get_children():
            self.signal_mapping_tree.delete(item)

        # Create signal to port/component mapping
        mappings = self._create_signal_mappings()

        for mapping in mappings:
            self.signal_mapping_tree.insert("", tk.END, values=mapping)

    def _create_signal_mappings(self):
        """Create signal to port/component relationship mappings."""
        mappings = []

        # This is a simplified mapping - in real AUTOSAR, the relationships
        # are more complex and defined through various reference elements
        signals = self.parser.parsed_data['signals']
        ports = self.parser.parsed_data['ports']
        components = self.parser.parsed_data['software_components']

        for signal in signals:
            signal_name = signal.get('name', 'Unknown')
            port_name = "Mapping not available"
            component_name = "Mapping not available"

            # Try to find related port (simplified logic)
            for port in ports:
                if port.get('interface') and signal_name.lower() in port.get('interface', '').lower():
                    port_name = port.get('name', 'Unknown')
                    break

            # Try to find related component (simplified logic)
            for component in components:
                if component.get('name') and signal_name.lower() in component.get('name', '').lower():
                    component_name = component.get('name', 'Unknown')
                    break

            mappings.append((signal_name, port_name, component_name))

        return mappings

    def _perform_search(self):
        """Perform global search across all data."""
        keyword = self.search_var.get().strip()
        if not keyword:
            return

        # Search data
        self.search_results = self.parser.search_data(keyword)

        # Update status with result count
        total_results = sum(len(results) for results in self.search_results.values())
        self.status_label.config(text=f"Search results: {total_results} matches for '{keyword}'")

        # Update tabs with search results and highlighting
        self._update_data_tabs_with_search()

    def _reset_search(self):
        """Reset search and show all data."""
        self.search_var.set("")
        self.search_results = None
        self.status_label.config(text="Ready")
        self._update_data_tabs()

    def _export_validation_report(self):
        """Export validation report."""
        if not self.current_file:
            messagebox.showwarning("Warning", "No file loaded")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="validation_report.txt"
        )

        if not file_path:
            return

        # Generate validation report data
        validation_results = []
        for result in self._perform_validation():
            if "✔" in result:
                validation_results.append({"type": "ok", "message": result[2:]})
            elif "⚠" in result:
                validation_results.append({"type": "warning", "message": result[2:]})
            else:
                validation_results.append({"type": "error", "message": result[2:]})

        counts = self.parser.get_summary_counts()
        insights_generator = ARXMLInsights(self.parser.parsed_data, counts)
        insights_text = insights_generator.generate_insights()
        file_name = os.path.basename(self.current_file)

        exporter = ARXMLExporter(self.parser.parsed_data)
        success, message = exporter.export_validation_report(file_path, validation_results, counts, insights_text, file_name)

        if success:
            exporter.show_export_success(message)
        else:
            exporter.show_export_error(message)