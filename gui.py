"""
Refactored GUI for EVE Production Calculator
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

from module_registry import ModuleRegistry, ShipModule, CapitalShipModule, ComponentModule
from calculator import RequirementsCalculator
from gui_utils import (
    create_labeled_dropdown,
    create_labeled_entry,
    create_button,
    create_scrolled_text,
    create_label_frame,
    set_text_content,
    create_grid_view
)

class EveProductionCalculator(tk.Tk):
    """Main GUI application for EVE Production Calculator"""
    def __init__(self, ore_data, registry, calculator):
        super().__init__()
        
        # Set application title and geometry
        self.title("EVE Online Production Calculator")
        self.geometry("900x800")
        self.minsize(800, 700)
        
        # Configure main application window
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Store registry and calculator references
        self.registry = registry
        self.calculator = calculator
        self.ore_data = ore_data
        
        # UI variables
        self.selected_faction = tk.StringVar(value="All")
        self.selected_ship_type = tk.StringVar(value="All")
        self.selected_ship = tk.StringVar()
        self.selected_capital_ship = tk.StringVar()
        self.selected_component = tk.StringVar()
        self.selected_pi_level = tk.StringVar(value="P1")
        self.material_efficiency = tk.StringVar(value="0")
        
        # Create UI
        self.create_ui()
        
    def create_ui(self):
        """Create the main UI components"""
        # Create notebook (tab container)
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Create tabs
        self.ship_tab = ttk.Frame(self.notebook)
        self.capital_ship_tab = ttk.Frame(self.notebook)
        self.component_tab = ttk.Frame(self.notebook)
        self.pi_tab = ttk.Frame(self.notebook)
        self.ore_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.ship_tab, text="Ships")
        self.notebook.add(self.capital_ship_tab, text="Capital Ships")
        self.notebook.add(self.component_tab, text="Components")
        self.notebook.add(self.pi_tab, text="PI Materials")
        self.notebook.add(self.ore_tab, text="Ore Refining")
        self.notebook.add(self.settings_tab, text="Settings")
        
        # Create shared frame for output
        self.output_frame = create_label_frame(
            self, 
            "Ship Information and Requirements", 
            use_grid=True,
            grid_row=1,
            grid_column=0,
            grid_sticky="nsew", 
            grid_padx=10, 
            grid_pady=5
        )
        self.output_frame.columnconfigure(0, weight=1)
        self.output_frame.rowconfigure(0, weight=1)
        
        # Text widget for all output
        self.output_text = create_scrolled_text(self.output_frame, height=20)
        
        # Configure the row weights
        self.rowconfigure(0, weight=2)  # Notebook gets more space
        self.rowconfigure(1, weight=3)  # Output frame gets more space
        
        # Create content for each tab
        self.create_ship_tab()
        self.create_capital_ship_tab()
        self.create_component_tab()
        self.create_pi_tab()
        self.create_ore_tab()
        self.create_settings_tab()
        
        # Bind tab change event to update the details
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
    
    def on_tab_change(self, event):
        """Handle tab changes to update the shared output areas"""
        tab_index = self.notebook.index(self.notebook.select())
        
        # Clear output areas
        set_text_content(self.output_text, "")
        
        # Update the displayed information based on the selected tab
        if tab_index == 0:  # Ships tab
            self.update_ship_details()
        elif tab_index == 1:  # Capital Ships tab
            self.update_capital_ship_details()
        elif tab_index == 2:  # Components tab
            self.update_component_details()
    
    def create_ship_tab(self):
        """Create the Ships tab content"""
        # Frame for ship selection
        selection_frame = create_label_frame(self.ship_tab, "Ship Selection")
        
        # Create faction filter
        factions = self.registry.get_factions()
        self.faction_dropdown = create_labeled_dropdown(
            selection_frame,
            "Faction:",
            self.selected_faction,
            factions,
            command=self.update_ship_dropdown
        )
        
        # Create ship type filter
        ship_types = self.registry.get_ship_types()
        self.ship_type_dropdown = create_labeled_dropdown(
            selection_frame,
            "Ship Type:",
            self.selected_ship_type,
            ship_types,
            command=self.update_ship_dropdown
        )
        
        # Create ship dropdown (will be populated by update_ship_dropdown)
        self.ship_dropdown = create_labeled_dropdown(
            selection_frame,
            "Ship:",
            self.selected_ship,
            [],
            command=self.update_ship_details
        )
        
        # Material efficiency input
        self.me_entry = create_labeled_entry(
            selection_frame,
            "Material Efficiency:",
            self.material_efficiency
        )
        
        # Calculate button
        self.calculate_button = create_button(
            selection_frame,
            "Calculate Requirements",
            self.calculate_ship_requirements
        )
        
        # Initialize the ship dropdown
        self.update_ship_dropdown()
    
    def create_capital_ship_tab(self):
        """Create the Capital Ships tab content"""
        # Frame for capital ship selection
        selection_frame = create_label_frame(self.capital_ship_tab, "Capital Ship Selection")
        
        # Create faction filter for capital ships
        factions = ["All", "Amarr", "Caldari", "Gallente", "Minmatar", "ORE"]
        self.capital_faction_dropdown = create_labeled_dropdown(
            selection_frame,
            "Faction:",
            tk.StringVar(value="All"),
            factions,
            command=self.update_capital_ship_dropdown
        )
        
        # Create ship type filter for capital ships
        capital_ship_types = ["All", "Freighter", "Dreadnought", "Carrier", "Capital Industrial"]
        self.capital_ship_type_dropdown = create_labeled_dropdown(
            selection_frame,
            "Ship Type:",
            tk.StringVar(value="All"),
            capital_ship_types,
            command=self.update_capital_ship_dropdown
        )
        
        # Create capital ship dropdown
        self.capital_ship_dropdown = create_labeled_dropdown(
            selection_frame,
            "Capital Ship:",
            self.selected_capital_ship,
            [],
            command=self.update_capital_ship_details
        )
        
        # Material efficiency input (we'll reuse the same variable)
        self.capital_me_entry = create_labeled_entry(
            selection_frame,
            "Material Efficiency:",
            self.material_efficiency
        )
        
        # Calculate button
        self.calculate_capital_button = create_button(
            selection_frame,
            "Calculate Requirements",
            self.calculate_capital_ship_requirements
        )
        
        # Initialize the capital ship dropdown
        self.update_capital_ship_dropdown()
    
    def update_capital_ship_dropdown(self, event=None):
        """Update the capital ship dropdown based on selected filters"""
        # Get the filters
        faction = self.capital_faction_dropdown.get()
        ship_type = self.capital_ship_type_dropdown.get()
        
        # Get filtered capital ships - only show owned capital ships
        capital_ships = self.registry.get_capital_ships_by_filter(
            None if faction == "All" else faction,
            None if ship_type == "All" else ship_type,
            owned_only=True  # Only show owned capital ships
        )
        
        # Get display names
        capital_ship_names = [ship.display_name for ship in capital_ships]
        
        # Sort the names
        capital_ship_names.sort()
        
        # Update the dropdown
        self.capital_ship_dropdown.configure(values=capital_ship_names)
        
        # If there are ships, select the first one
        if capital_ship_names:
            self.selected_capital_ship.set(capital_ship_names[0])
            self.update_capital_ship_details()
        else:
            self.selected_capital_ship.set("")
            set_text_content(self.output_text, "No owned capital ships found matching the filters.")
    
    def create_component_tab(self):
        """Create the Components tab content"""
        # Frame for component selection
        selection_frame = create_label_frame(self.component_tab, "Component Selection")
        
        # Get all components
        components = self.registry.get_all_components()
        component_names = [component.display_name for comp_name, component in components.items()]
        
        # Create component dropdown
        self.component_dropdown = create_labeled_dropdown(
            selection_frame,
            "Component:",
            self.selected_component,
            component_names,
            command=self.update_component_details
        )
        
        # Material efficiency input
        self.component_me_entry = create_labeled_entry(
            selection_frame,
            "Material Efficiency:",
            self.material_efficiency
        )
        
        # Calculate button
        self.calculate_component_button = create_button(
            selection_frame,
            "Calculate Requirements",
            self.calculate_component_requirements
        )
    
    def create_pi_tab(self):
        """Create the PI Materials tab content"""
        # To be implemented based on PI material requirements
        label = ttk.Label(self.pi_tab, text="Planetary Interaction material calculator coming soon!")
        label.pack(padx=20, pady=20)
    
    def create_ore_tab(self):
        """Create the Ore Refining tab content"""
        # To be implemented based on ore refining calculations
        label = ttk.Label(self.ore_tab, text="Ore refining calculator coming soon!")
        label.pack(padx=20, pady=20)
    
    def create_settings_tab(self):
        """Create the Settings tab content"""
        # Frame for blueprint ownership settings
        blueprint_frame = create_label_frame(self.settings_tab, "Blueprint Ownership")
        
        # Button to edit blueprint ownership
        edit_blueprints_button = create_button(
            blueprint_frame,
            "Edit Blueprint Ownership",
            self.edit_blueprint_ownership
        )
        
        # Frame for import/export settings
        import_export_frame = create_label_frame(self.settings_tab, "Import/Export")
        
        # Buttons for import/export
        export_button = create_button(
            import_export_frame,
            "Export Settings",
            self.export_settings
        )
        
        import_button = create_button(
            import_export_frame,
            "Import Settings",
            self.import_settings
        )
    
    def update_ship_dropdown(self, event=None):
        """
        Update the ship dropdown based on selected faction and ship type
        
        Args:
            event: Tkinter event (optional)
        """
        # Get filter values
        faction = self.selected_faction.get()
        ship_type = self.selected_ship_type.get()
        
        # Get filtered ships - only show owned ships
        ships = self.registry.get_ships_by_filter(
            None if faction == "All" else faction,
            None if ship_type == "All" else ship_type,
            owned_only=True  # Only show owned ships
        )
        
        # Update dropdown values
        ship_names = [ship.display_name for ship in ships]
        self.ship_dropdown['values'] = ship_names
        
        # Clear selection if no ships available
        if not ship_names:
            self.selected_ship.set("")
            set_text_content(self.output_text, "No owned ships available with the selected filters.")
        elif self.selected_ship.get() not in ship_names:
            self.selected_ship.set(ship_names[0])
            self.update_ship_details()
    
    def update_ship_details(self, event=None):
        """
        Update the ship details text based on selected ship
        
        Args:
            event: Tkinter event (optional)
        """
        ship_name = self.selected_ship.get()
        
        if not ship_name:
            set_text_content(self.output_text, "No ship selected.")
            return
            
        # Find ship in registry
        ship = self.registry.get_ship_by_display_name(ship_name)
        
        if not ship:
            set_text_content(self.output_text, f"Ship '{ship_name}' not found in registry.")
            return
            
        # Update details text
        set_text_content(self.output_text, ship.details)
    
    def update_capital_ship_details(self, event=None):
        """
        Update the capital ship details text based on selected capital ship
        
        Args:
            event: Tkinter event (optional)
        """
        capital_ship_name = self.selected_capital_ship.get()
        
        if not capital_ship_name:
            set_text_content(self.output_text, "No capital ship selected.")
            return
            
        # Find capital ship in registry
        capital_ship = self.registry.get_capital_ship_by_display_name(capital_ship_name)
        
        if not capital_ship:
            set_text_content(self.output_text, f"Capital ship '{capital_ship_name}' not found in registry.")
            return
            
        # Update details text
        set_text_content(self.output_text, capital_ship.details)
    
    def update_component_details(self, event=None):
        """
        Update the component details text based on selected component
        
        Args:
            event: Tkinter event (optional)
        """
        component_name = self.selected_component.get()
        
        if not component_name:
            set_text_content(self.output_text, "No component selected.")
            return
            
        # Find component in registry
        component = self.registry.get_component_by_display_name(component_name)
        
        if not component:
            set_text_content(self.output_text, f"Component '{component_name}' not found in registry.")
            return
            
        # Update details text
        set_text_content(self.output_text, component.details)
    
    def calculate_ship_requirements(self):
        """Calculate and display ship material requirements"""
        # Get selected ship and ME
        ship_name = self.selected_ship.get()
        
        if not ship_name:
            messagebox.showwarning("Warning", "No ship selected.")
            return
        
        # Find ship in registry
        ship = self.registry.get_ship_by_display_name(ship_name)
        
        if not ship:
            messagebox.showerror("Error", f"Ship '{ship_name}' not found in registry.")
            return
        
        # Get material efficiency
        try:
            me = int(self.me_entry.get())
        except ValueError:
            messagebox.showwarning("Warning", "Invalid material efficiency value. Using 0.")
            me = 0
        
        # Calculate requirements
        requirements = self.calculator.calculate_ship_requirements(ship.name, me)
        
        # Format requirements for display
        requirements_text = f"Material Requirements for {ship_name} (ME: {me}%):\n\n"
        
        # Sort materials alphabetically
        sorted_materials = sorted(requirements.items())
        
        for material, amount in sorted_materials:
            requirements_text += f"{material}: {amount:,}\n"
            
        # Update materials text
        output_text = f"{ship.details}\n\n{requirements_text}"
        set_text_content(self.output_text, output_text)
    
    def calculate_capital_ship_requirements(self):
        """Calculate and display capital ship material requirements"""
        # Get selected capital ship and ME
        capital_ship_name = self.selected_capital_ship.get()
        
        if not capital_ship_name:
            messagebox.showwarning("Warning", "No capital ship selected.")
            return
        
        # Find capital ship in registry
        capital_ship = self.registry.get_capital_ship_by_display_name(capital_ship_name)
        
        if not capital_ship:
            messagebox.showerror("Error", f"Capital ship '{capital_ship_name}' not found in registry.")
            return
        
        # Get material efficiency
        try:
            me = int(self.capital_me_entry.get())
        except ValueError:
            messagebox.showwarning("Warning", "Invalid material efficiency value. Using 0.")
            me = 0
        
        # Calculate requirements
        requirements = self.calculator.calculate_capital_ship_requirements(capital_ship.name, me)
        
        # Format requirements for display
        requirements_text = f"Material Requirements for {capital_ship_name} (ME: {me}%):\n\n"
        
        # Sort materials alphabetically
        sorted_materials = sorted(requirements.items())
        
        for material, amount in sorted_materials:
            requirements_text += f"{material}: {amount:,}\n"
            
        # Update materials text
        output_text = f"{capital_ship.details}\n\n{requirements_text}"
        set_text_content(self.output_text, output_text)
    
    def calculate_component_requirements(self):
        """Calculate and display component material requirements"""
        # Get selected component and ME
        component_name = self.selected_component.get()
        
        if not component_name:
            messagebox.showwarning("Warning", "No component selected.")
            return
        
        # Find component in registry
        component = self.registry.get_component_by_display_name(component_name)
        
        if not component:
            messagebox.showerror("Error", f"Component '{component_name}' not found in registry.")
            return
        
        # Get material efficiency
        try:
            me = int(self.component_me_entry.get())
        except ValueError:
            messagebox.showwarning("Warning", "Invalid material efficiency value. Using 0.")
            me = 0
        
        # Calculate requirements
        requirements = self.calculator.calculate_component_requirements(component.name, me)
        
        # Format requirements for display
        requirements_text = f"Material Requirements for {component_name} (ME: {me}%):\n\n"
        
        # Sort materials alphabetically
        sorted_materials = sorted(requirements.items())
        
        for material, amount in sorted_materials:
            requirements_text += f"{material}: {amount:,}\n"
            
        # Update materials text
        output_text = f"{component.details}\n\n{requirements_text}"
        set_text_content(self.output_text, output_text)
    
    def edit_blueprint_ownership(self):
        """Open the blueprint ownership editor"""
        # To be implemented
        messagebox.showinfo("Info", "Blueprint ownership editor coming soon!")
    
    def export_settings(self):
        """Export settings to a JSON file"""
        # Ask for file location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export Settings"
        )
        
        if not file_path:
            return
            
        # Create settings dictionary
        settings = {
            "blueprint_ownership": {}
        }
        
        # Write to file
        try:
            with open(file_path, 'w') as f:
                json.dump(settings, f, indent=2)
            messagebox.showinfo("Success", f"Settings exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export settings: {str(e)}")
    
    def import_settings(self):
        """Import settings from a JSON file"""
        # Ask for file location
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Import Settings"
        )
        
        if not file_path:
            return
            
        # Read from file
        try:
            with open(file_path, 'r') as f:
                settings = json.load(f)
                
            # Update blueprint config
            if "blueprint_ownership" in settings:
                messagebox.showinfo("Success", "Settings imported successfully.")
            else:
                messagebox.showwarning("Warning", "No blueprint ownership settings found in file.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import settings: {str(e)}")
