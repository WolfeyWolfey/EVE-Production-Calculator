"""
Refactored GUI for EVE Production Calculator
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

from core.module_registry import ModuleRegistry, ShipModule, CapitalShipModule, ComponentModule
from core.calculator import RequirementsCalculator
from gui.gui_utils import (
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
    def __init__(self, ore_data, registry, calculator, blueprint_config):
        """
        Initialize the main application
        
        Args:
            ore_data (dict): Ore data dictionary
            registry (ModuleRegistry): Module registry
            calculator (RequirementsCalculator): Requirements calculator
            blueprint_config (dict): Blueprint configuration
        """
        super().__init__()
        
        # Store references to external data
        self.ore_data = ore_data
        self.registry = registry
        self.calculator = calculator
        self.blueprint_config = blueprint_config
        
        # Set application title and geometry
        self.title("EVE Online Production Calculator")
        self.geometry("900x800")
        self.minsize(800, 700)
        
        # Configure main application window
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Set up state variables for various dropdowns
        self.selected_faction = tk.StringVar(value="All")
        self.selected_ship_type = tk.StringVar(value="All")
        self.selected_ship = tk.StringVar()
        self.selected_capital_ship = tk.StringVar()
        self.selected_component = tk.StringVar()
        self.selected_pi_level = tk.StringVar(value="P1")
        
        # Quantity variables for calculation
        self.ship_quantity = tk.StringVar(value="1")
        self.capital_ship_quantity = tk.StringVar(value="1")
        self.component_quantity = tk.StringVar(value="1")
        self.pi_quantity = tk.StringVar(value="1")
        
        # Ownership editor shown flag
        self.ownership_editor_shown = False
        
        # Create UI
        self.create_ui()
        
        # Register save function on window close
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
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
        # self.ore_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.ship_tab, text="Ships")
        self.notebook.add(self.capital_ship_tab, text="Capital Ships")
        self.notebook.add(self.component_tab, text="Components")
        self.notebook.add(self.pi_tab, text="PI Materials")
        # self.notebook.add(self.ore_tab, text="Ore Refining")
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
        # self.create_ore_tab()
        self.create_settings_tab()
        
        # Bind tab change event to update the details
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        
        # Create menus
        self._create_menus()
    
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
        elif tab_index == 3:  # PI Materials tab
            self.update_pi_details()
    
    def create_ship_tab(self):
        """Create the Ships tab content"""
        # Frame for ship selection
        selection_frame = create_label_frame(self.ship_tab, "Ship Selection")
        
        # Create faction dropdown
        self.faction_dropdown = create_labeled_dropdown(
            selection_frame,
            "Faction:",
            self.selected_faction,
            self.registry.get_factions(),
            command=self.update_ship_dropdown
        )
        
        # Create ship type dropdown
        self.ship_type_dropdown = create_labeled_dropdown(
            selection_frame,
            "Ship Type:",
            self.selected_ship_type,
            self.registry.get_ship_types(),
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
        
        # Create quantity input frame
        quantity_frame = ttk.Frame(selection_frame)
        quantity_frame.pack(fill="x", padx=5, pady=5)
        
        # Add quantity input field
        self.ship_quantity_entry = create_labeled_entry(
            quantity_frame,
            "Quantity:",
            self.ship_quantity,
            width=5,
            label_width=10
        )
        
        # Calculate button
        self.calculate_button = create_button(
            quantity_frame,
            "Calculate Requirements",
            self.calculate_ship_requirements
        )
        
        # Initialize the ship dropdown
        self.update_ship_dropdown()
    
    def create_capital_ship_tab(self):
        """Create the Capital Ships tab content"""
        # Frame for capital ship selection
        selection_frame = create_label_frame(self.capital_ship_tab, "Capital Ship Selection")
        
        # Create capital ship type dropdown
        self.capital_ship_type_dropdown = create_labeled_dropdown(
            selection_frame,
            "Ship Type:",
            tk.StringVar(value="All"),
            ["All", "Freighter", "Dreadnought", "Carrier", "Capital Industrial"],
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
        
        # Create quantity input frame
        quantity_frame = ttk.Frame(selection_frame)
        quantity_frame.pack(fill="x", padx=5, pady=5)
        
        # Add quantity input field
        self.capital_ship_quantity_entry = create_labeled_entry(
            quantity_frame,
            "Quantity:",
            self.capital_ship_quantity,
            width=5,
            label_width=10
        )
        
        # Calculate button
        self.calculate_capital_button = create_button(
            quantity_frame,
            "Calculate Requirements",
            self.calculate_capital_ship_requirements
        )
        
        # Initialize the capital ship dropdown
        self.update_capital_ship_dropdown()
    
    def create_component_tab(self):
        """Create the Components tab content"""
        # Frame for component selection
        selection_frame = create_label_frame(self.component_tab, "Component Selection")
        
        # Get all components that are owned
        components = self.registry.get_components_by_filter(owned_only=True)
        component_names = [component.display_name for component in components]
        
        # Create component dropdown
        self.component_dropdown = create_labeled_dropdown(
            selection_frame,
            "Component:",
            self.selected_component,
            component_names,
            command=self.update_component_details
        )
        
        # Create quantity input frame
        quantity_frame = ttk.Frame(selection_frame)
        quantity_frame.pack(fill="x", padx=5, pady=5)
        
        # Add quantity input field
        self.component_quantity_entry = create_labeled_entry(
            quantity_frame,
            "Quantity:",
            self.component_quantity,
            width=5,
            label_width=10
        )
        
        # Calculate button
        self.calculate_component_button = create_button(
            quantity_frame,
            "Calculate Requirements",
            self.calculate_component_requirements
        )
    
    def create_pi_tab(self):
        """Create the PI Materials tab content"""
        # Frame for PI selection
        selection_frame = create_label_frame(self.pi_tab, "PI Selection")
        
        # Create PI level filter
        pi_levels = ["P1", "P2", "P3", "P4"]
        self.pi_level_dropdown = create_labeled_dropdown(
            selection_frame,
            "PI Level:",
            self.selected_pi_level,
            pi_levels,
            command=self.update_pi_material_dropdown
        )
        
        # Create PI material dropdown
        self.pi_material_dropdown = create_labeled_dropdown(
            selection_frame,
            "PI Material:",
            tk.StringVar(),
            [],
            command=self.update_pi_details
        )
        
        # Create quantity input frame
        quantity_frame = ttk.Frame(selection_frame)
        quantity_frame.pack(fill="x", padx=5, pady=5)
        
        # Add quantity input field
        self.pi_quantity_entry = create_labeled_entry(
            quantity_frame,
            "Quantity:",
            self.pi_quantity,
            width=5,
            label_width=10
        )
        
        # Calculate button
        self.calculate_pi_button = create_button(
            quantity_frame,
            "Calculate Requirements",
            self.calculate_pi_requirements
        )
        
        # Initialize the PI material dropdown
        self.update_pi_material_dropdown()
    
    # def create_ore_tab(self):
    #     """Create the Ore Refining tab content"""
    #     # Frame for ore selection
    #     selection_frame = create_label_frame(self.ore_tab, "Ore Selection")
        
    #     # Create ore dropdown
    #     self.ore_dropdown = create_labeled_dropdown(
    #         selection_frame,
    #         "Ore:",
    #         tk.StringVar(),
    #         [],
    #         command=self.update_ore_details
    #     )
        
    #     # Calculate button
    #     self.calculate_ore_button = create_button(
    #         selection_frame,
    #         "Calculate Requirements",
    #         self.calculate_ore_requirements
    #     )
        
    #     # Initialize the ore dropdown
    #     self.update_ore_dropdown()
    
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
        """Update the ship dropdown based on selected faction and type"""
        # Get the selected faction and type
        faction = self.selected_faction.get()
        ship_type = self.selected_ship_type.get()
        
        # Filter ships (passing True for owned_only to show only owned ships)
        filtered_ships = self.registry.get_ships_by_filter(
            faction if faction != "All" else None,
            ship_type if ship_type != "All" else None,
            True  # Set to True to show only owned ships
        )
        
        # Get display names
        ship_display_names = [ship.display_name for ship in filtered_ships]
        
        # Sort the names
        ship_display_names.sort()
        
        # Update the dropdown with the filtered ships
        self.ship_dropdown.configure(values=ship_display_names)
        
        # Clear the ship text and disable manufacturing button
        self.output_text.delete(1.0, tk.END)
        self.calculate_button.configure(state="disabled")
        
        # If there are ships, select the first one
        if ship_display_names:
            self.ship_dropdown.set(ship_display_names[0])
            self.update_ship_details()  # Trigger the selection event
        else:
            self.ship_dropdown.set("")
            # Show a message if no ships are found with the current filter
            self.output_text.insert(tk.END, "No ships found with the current filter.\n\n"
                                          "Try selecting different filters or use the Blueprint Ownership Editor.")
    
    def update_capital_ship_dropdown(self, event=None):
        """Update the capital ship dropdown based on selected type"""
        # Get the selected ship type
        ship_type = self.capital_ship_type_dropdown.get()
        
        # Filter capital ships (passing True for owned_only to show only owned ships)
        filtered_ships = self.registry.get_capital_ships_by_filter(
            None,  # No faction filter for capital ships
            ship_type if ship_type != "All" else None,
            True  # Set to True to show only owned ships
        )
        
        # Get display names
        ship_display_names = [ship.display_name for ship in filtered_ships]
        
        # Sort the names
        ship_display_names.sort()
        
        # Update the dropdown with the filtered ships
        self.capital_ship_dropdown.configure(values=ship_display_names)
        
        # Clear the capital ship text and disable manufacturing button
        self.output_text.delete(1.0, tk.END)
        self.calculate_capital_button.configure(state="disabled")
        
        # If there are ships, select the first one
        if ship_display_names:
            self.capital_ship_dropdown.set(ship_display_names[0])
            self.update_capital_ship_details()  # Trigger the selection event
        else:
            self.capital_ship_dropdown.set("")
            # Show a message if no ships are found with the current filter
            self.output_text.insert(tk.END, "No capital ships found with the current filter.\n\n"
                                          "Try selecting different filters or use the Blueprint Ownership Editor.")
    
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
    
    def update_pi_details(self, event=None):
        """
        Update the PI details text based on selected PI material
        
        Args:
            event: Tkinter event (optional)
        """
        pi_material_name = self.pi_material_dropdown.get()
        
        if not pi_material_name:
            set_text_content(self.output_text, "No PI material selected.")
            return
            
        # Find PI material in registry
        pi_material = self.registry.get_pi_material_by_display_name(pi_material_name)
        
        if not pi_material:
            set_text_content(self.output_text, f"PI material '{pi_material_name}' not found in registry.")
            return
            
        # Update details text
        set_text_content(self.output_text, pi_material.details)
    
    # def update_ore_details(self, event=None):
    #     """
    #     Update the ore details text based on selected ore
        
    #     Args:
    #         event: Tkinter event (optional)
    #     """
    #     ore_name = self.ore_dropdown.get()
        
    #     if not ore_name:
    #         set_text_content(self.output_text, "No ore selected.")
    #         return
            
    #     # Find ore in registry
    #     ore = self.registry.get_ore_by_display_name(ore_name)
        
    #     if not ore:
    #         set_text_content(self.output_text, f"Ore '{ore_name}' not found in registry.")
    #         return
            
    #     # Update details text
    #     set_text_content(self.output_text, ore.details)
    
    def calculate_ship_requirements(self):
        """Calculate and display ship material requirements"""
        # Get selected ship
        ship_name = self.selected_ship.get()
        
        if not ship_name:
            messagebox.showwarning("Warning", "No ship selected.")
            return
        
        # Get quantity (default to 1 if invalid)
        try:
            quantity = int(self.ship_quantity.get())
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1
            self.ship_quantity.set("1")
        
        # Find ship in registry
        ship = self.registry.get_ship_by_display_name(ship_name)
        
        if not ship:
            messagebox.showerror("Error", f"Ship '{ship_name}' not found in registry.")
            return
        
        # Calculate requirements
        requirements = self.calculator.calculate_ship_requirements(ship.name)
        
        # Get ME level from calculator for this specific ship
        me_level = self.calculator.get_me_level('ships', ship.name)
        
        # Get TE level from calculator for this specific ship
        te_level = self.calculator.get_te_level('ships', ship.name)
        
        # Calculate production time (use default base time if not available)
        base_time = getattr(ship, 'production_time', 3600)  # Default to 1 hour if not specified
        production_time = self.calculator.calculate_production_time(base_time, te_level)
        
        # Format time for display
        hours, remainder = divmod(production_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        
        # Format requirements for display
        requirements_text = f"Material Requirements for {quantity}x {ship_name} (ME: {me_level}%, TE: {te_level}%):\n\n"
        requirements_text += f"Production Time per Unit: {time_str}\n\n"
        
        # Sort materials alphabetically
        sorted_materials = sorted(requirements.items())
        
        for material, material_quantity in sorted_materials:
            # Multiply by quantity
            total_quantity = material_quantity * quantity
            requirements_text += f"{material}: {total_quantity:,.2f}\n"
            
        set_text_content(self.output_text, requirements_text)
    
    def calculate_capital_ship_requirements(self):
        """Calculate and display capital ship material requirements"""
        # Get selected capital ship
        capital_ship_name = self.selected_capital_ship.get()
        
        if not capital_ship_name:
            messagebox.showwarning("Warning", "No capital ship selected.")
            return
        
        # Get quantity (default to 1 if invalid)
        try:
            quantity = int(self.capital_ship_quantity.get())
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1
            self.capital_ship_quantity.set("1")
        
        # Find capital ship in registry
        capital_ship = self.registry.get_capital_ship_by_display_name(capital_ship_name)
        
        if not capital_ship:
            messagebox.showerror("Error", f"Capital ship '{capital_ship_name}' not found in registry.")
            return
        
        # Calculate requirements
        requirements = self.calculator.calculate_capital_ship_requirements(capital_ship.name)
        
        # Get ME level for capital ship
        me_level = self.calculator.get_me_level('capital_ships', capital_ship.name)
        
        # Get TE level for capital ship
        te_level = self.calculator.get_te_level('capital_ships', capital_ship.name)
        
        # Calculate production time (use default base time if not available)
        base_time = getattr(capital_ship, 'production_time', 7200)  # Default to 2 hours if not specified
        production_time = self.calculator.calculate_production_time(base_time, te_level)
        
        # Format time for display
        hours, remainder = divmod(production_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        
        # Format requirements for display
        requirements_text = f"Material Requirements for {quantity}x {capital_ship_name} (ME: {me_level}%, TE: {te_level}%):\n\n"
        requirements_text += f"Production Time per Unit: {time_str}\n\n"
        
        # Sort materials alphabetically
        sorted_materials = sorted(requirements.items())
        
        for material, material_quantity in sorted_materials:
            # Multiply by quantity
            total_quantity = material_quantity * quantity
            requirements_text += f"{material}: {total_quantity:,.2f}\n"
            
        set_text_content(self.output_text, requirements_text)
    
    def calculate_component_requirements(self):
        """Calculate and display component material requirements"""
        # Get selected component
        component_name = self.selected_component.get()
        
        if not component_name:
            messagebox.showwarning("Warning", "No component selected.")
            return
        
        # Get quantity (default to 1 if invalid)
        try:
            quantity = int(self.component_quantity.get())
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1
            self.component_quantity.set("1")
        
        # Find component in registry
        component = self.registry.get_component_by_display_name(component_name)
        
        if not component:
            messagebox.showerror("Error", f"Component '{component_name}' not found in registry.")
            return
        
        # Calculate requirements
        requirements = self.calculator.calculate_component_requirements(component.name)
        
        # Get ME level for component
        me_level = self.calculator.get_me_level('components', component.name)
        
        # Get TE level for component
        te_level = self.calculator.get_te_level('components', component.name)
        
        # Calculate production time (use default base time if not available)
        base_time = getattr(component, 'production_time', 1800)  # Default to 30 minutes if not specified
        production_time = self.calculator.calculate_production_time(base_time, te_level)
        
        # Format time for display
        hours, remainder = divmod(production_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        
        # Format requirements for display
        requirements_text = f"Material Requirements for {quantity}x {component_name} (ME: {me_level}%, TE: {te_level}%):\n\n"
        requirements_text += f"Production Time per Unit: {time_str}\n\n"
        
        # Sort materials alphabetically
        sorted_materials = sorted(requirements.items())
        
        for material, material_quantity in sorted_materials:
            # Multiply by quantity
            total_quantity = material_quantity * quantity
            requirements_text += f"{material}: {total_quantity:,.2f}\n"
            
        set_text_content(self.output_text, requirements_text)
    
    def calculate_pi_requirements(self):
        """Calculate and display PI material requirements"""
        # Get selected PI material
        pi_material_name = self.pi_material_dropdown.get()
        
        if not pi_material_name:
            messagebox.showwarning("Warning", "No PI material selected.")
            return
        
        # Get quantity (default to 1 if invalid)
        try:
            quantity = int(self.pi_quantity.get())
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1
            self.pi_quantity.set("1")
        
        # Find PI material in registry
        pi_material = self.registry.get_pi_material_by_display_name(pi_material_name)
        
        if not pi_material:
            messagebox.showerror("Error", f"PI material '{pi_material_name}' not found in registry.")
            return
        
        # Calculate requirements
        requirements = self.calculator.calculate_pi_requirements(pi_material.name)
        
        # Get ME level from calculator for this specific PI material
        me_level = self.calculator.get_me_level('pi', pi_material.name)
        
        # Format requirements for display
        requirements_text = f"Material Requirements for {quantity}x {pi_material_name} (ME: {me_level}%):\n\n"
        
        # Sort materials alphabetically
        sorted_materials = sorted(requirements.items())
        
        for material, material_quantity in sorted_materials:
            # Multiply by quantity
            total_quantity = material_quantity * quantity
            requirements_text += f"{material}: {total_quantity:,.2f}\n"
            
        set_text_content(self.output_text, requirements_text)
    
    # def calculate_ore_requirements(self):
    #     """Calculate and display ore material requirements"""
    #     # Get selected ore
    #     ore_name = self.ore_dropdown.get()
        
    #     if not ore_name:
    #         messagebox.showwarning("Warning", "No ore selected.")
    #         return
        
    #     # Find ore in registry
    #     ore = self.registry.get_ore_by_display_name(ore_name)
        
    #     if not ore:
    #         messagebox.showerror("Error", f"Ore '{ore_name}' not found in registry.")
    #         return
        
    #     # Calculate requirements
    #     requirements = self.calculator.calculate_ore_requirements(ore.name)
        
    #     # Format requirements for display
    #     requirements_text = f"Material Requirements for {ore_name}:\n\n"
        
    #     # Sort materials alphabetically
    #     sorted_materials = sorted(requirements.items())
        
    #     for material, amount in sorted_materials:
    #         requirements_text += f"{material}: {amount:,}\n"
            
    #     # Update materials text
    #     output_text = f"{ore.details}\n\n{requirements_text}"
    #     set_text_content(self.output_text, output_text)
    
    def edit_blueprint_ownership(self):
        """Open the blueprint ownership editor"""
        from gui.blueprints_gui import BlueprintManager
        from config.blueprint_config import load_blueprint_ownership, save_blueprint_ownership
        
        try:
            # Load the current blueprint configuration
            self.blueprint_config = load_blueprint_ownership()
            
            # Create a new toplevel window
            blueprint_window = tk.Toplevel(self)
            blueprint_window.title("Blueprint Ownership Manager")
            
            # Prepare the modules dictionary for the blueprint manager
            discovered_modules = {
                'ships': self.registry.ships,
                'capital_ships': self.registry.capital_ships,
                'components': self.registry.components
            }
            
            # Create the blueprint manager
            blueprint_manager = BlueprintManager(
                blueprint_window, 
                discovered_modules,
                self.blueprint_config,
                self.registry
            )
            
            # Create the blueprint window UI
            blueprint_manager.create_blueprint_window(blueprint_window)
            
            # Make the window modal
            blueprint_window.transient(self)
            blueprint_window.grab_set()
            
            # Wait for the window to be closed
            self.wait_window(blueprint_window)
            
            # Make sure to save changes after the window is closed
            save_blueprint_ownership(self.blueprint_config)
            
            # Apply the updated ownership to the registry
            from config.blueprint_config import apply_blueprint_ownership
            apply_blueprint_ownership(self.blueprint_config, self.registry)
            
            # Refresh the UI to reflect any changes
            current_tab = self.notebook.index(self.notebook.select())
            if current_tab == 0:  # Ships tab
                self.update_ship_dropdown()
            elif current_tab == 1:  # Capital Ships tab
                self.update_capital_ship_dropdown()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Blueprint Ownership Editor: {str(e)}")
    
    # def load_capital_components(self):
    #     """Load capital components from the JSON file for the blueprint editor"""
    #     import os
    #     import json
        
    #     capital_components = {}
    #     components_path = os.path.join(os.path.dirname(__file__), "data", "capitalcomponents.json")
        
    #     try:
    #         with open(components_path, 'r') as f:
    #             data = json.load(f)
                
    #         if 'capital_components' in data:
    #             for key, component in data['capital_components'].items():
    #                 capital_components[key] = {
    #                     'display_name': component.get('display_name', key),
    #                     'blueprint_owned': component.get('owned_status', 'Unowned'),
    #                     'details': component.get('details', '')
    #                 }
    #     except Exception as e:
    #         print(f"Error loading capital components: {e}")
            
    #     return capital_components
    
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
    
    def _create_menus(self):
        """Create application menus"""
        # Create main menu
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        
        # Create File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.destroy)
        
        # Create Settings menu
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Blueprint Ownership Editor", command=self.edit_blueprint_ownership)
        settings_menu.add_command(label="Reset All Ship Ownership", command=self.reset_ship_ownership)
        settings_menu.add_command(label="Export Settings", command=self.export_settings)
        settings_menu.add_command(label="Import Settings", command=self.import_settings)
    
    def reset_ship_ownership(self):
        """Reset ownership status for all ships and capital ships"""
        # Confirm with the user
        if not messagebox.askyesno("Confirm Reset", 
                                  "Are you sure you want to reset ownership status for ALL ships and capital ships?\n\n"
                                  "This action cannot be undone."):
            return
        
        # Reset ownership for all ships
        for ship_name, ship in self.registry.ships.items():
            ship.owned_status = False
            
            # Update the blueprint config
            if ship_name in self.blueprint_config.get('ships', {}):
                self.blueprint_config['ships'][ship_name]['owned'] = False
            elif hasattr(ship, 'display_name') and ship.display_name in self.blueprint_config.get('ships', {}):
                self.blueprint_config['ships'][ship.display_name]['owned'] = False
        
        # Reset ownership for all capital ships
        for ship_name, ship in self.registry.capital_ships.items():
            ship.owned_status = False
            
            # Update the blueprint config
            if ship_name in self.blueprint_config.get('capital_ships', {}):
                self.blueprint_config['capital_ships'][ship_name]['owned'] = False
            elif hasattr(ship, 'display_name') and ship.display_name in self.blueprint_config.get('capital_ships', {}):
                self.blueprint_config['capital_ships'][ship.display_name]['owned'] = False
        
        # Save the changes
        try:
            from config.blueprint_config import save_blueprint_ownership
            # Save the configuration
            success = save_blueprint_ownership(self.blueprint_config)
            if success:
                messagebox.showinfo("Success", "All ship ownership has been reset. The changes have been saved.")
                
                # Reset the editor shown flag so it can appear again
                self.ownership_editor_shown = False
                
                # Refresh dropdown displays if needed
                current_tab = self.notebook.index(self.notebook.select())
                if current_tab == 0:  # Ships tab
                    self.update_ship_dropdown()
                elif current_tab == 1:  # Capital Ships tab
                    self.update_capital_ship_dropdown()
            else:
                messagebox.showerror("Error", "Failed to save ownership changes.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def test_set_atron_owned(self):
        """Test function to set Atron as owned for testing the ownership functionality"""
        try:
            # Create BlueprintManager instance
            from gui.blueprints_gui import BlueprintManager
            manager = BlueprintManager(
                self,
                self.discovered_modules,
                self.blueprint_config,
                self.registry
            )
            
            # Call the test function
            success = manager.set_atron_as_owned_test()
            
            if success:
                # Force a refresh of the ship dropdowns to show the changes
                self.update_ship_dropdown()
                messagebox.showinfo("Test Successful", "Atron has been set as owned. Check blueprint_ownership.json to verify the changes were saved.")
            else:
                messagebox.showerror("Test Failed", "Failed to set Atron as owned. Check console for details.")
                
        except Exception as e:
            error_msg = f"Error in test_set_atron_owned: {str(e)}"
            messagebox.showerror("Error", error_msg)
    
    def update_pi_material_dropdown(self, event=None):
        """Update the PI material dropdown based on selected PI level"""
        # Get the PI level
        pi_level = self.selected_pi_level.get()
        
        # Get filtered PI materials
        pi_materials = self.registry.get_pi_materials_by_level(pi_level)
        
        # Get display names
        pi_material_names = [material.display_name for material in pi_materials]
        
        # Sort the names
        pi_material_names.sort()
        
        # Update the dropdown
        self.pi_material_dropdown.configure(values=pi_material_names)
        
        # If there are materials, select the first one
        if pi_material_names:
            self.pi_material_dropdown.set(pi_material_names[0])
            self.update_pi_details()
        else:
            self.pi_material_dropdown.set("")
            set_text_content(self.output_text, "No PI materials found matching the filters.")

    def on_close(self):
        """Save blueprint configuration before closing the application"""
        try:
            from config.blueprint_config import save_blueprint_ownership
            # Save the configuration
            success = save_blueprint_ownership(self.blueprint_config)
            if success:
                print("Blueprint configuration saved successfully.")
            else:
                print("Failed to save blueprint configuration.")
        except Exception as e:
            print(f"Error saving blueprint configuration: {e}")
        
        # Destroy the application
        self.destroy()
