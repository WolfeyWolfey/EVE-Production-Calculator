"""
Refactored GUI for EVE Production Calculator
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import shutil

from core.utils.debug import debug_print

from core.module_registry import ModuleRegistry, ShipModule, CapitalShipModule, ComponentModule
from core.calculator import RequirementsCalculator
from core.gui.gui_utils import (
    create_labeled_dropdown,
    create_labeled_entry,
    create_button,
    create_scrolled_text,
    create_label_frame,
    set_text_content,
    create_grid_view
)
from core.gui.blueprints_gui import BlueprintManager
from core.gui.settings_gui import SettingsWindow
from core.gui.blueprint_utils import open_blueprint_editor, reset_ship_ownership, apply_blueprint_changes
from core.config.settings import load_settings, save_settings

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
        
        # Load settings
        self.settings = load_settings()
        
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
        self.selected_component = tk.StringVar()
        self.selected_pi_level = tk.StringVar(value="P1")
        
        # Quantity variables for calculation
        self.ship_quantity = tk.StringVar(value="1")
        self.component_quantity = tk.StringVar(value="1")
        self.pi_quantity = tk.StringVar(value="1")
        
        # Ownership editor shown flag
        self.ownership_editor_shown = False
        
        # Create UI
        self.create_ui()
        
        # Apply theme based on settings
        self.apply_theme(self.settings.get('theme', 'light'))
        
        # Register save function on window close
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def create_ui(self):
        """Create the main UI components"""
        # Create notebook (tab container)
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Create tabs
        self.ship_tab = ttk.Frame(self.notebook)
        self.component_tab = ttk.Frame(self.notebook)
        self.pi_tab = ttk.Frame(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.ship_tab, text="Ships")
        self.notebook.add(self.component_tab, text="Components")
        self.notebook.add(self.pi_tab, text="PI Materials")
        
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
        self.create_component_tab()
        self.create_pi_tab()
        
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
        elif tab_index == 1:  # Components tab
            self.update_component_details()
        elif tab_index == 2:  # PI Materials tab
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
        
        # Create ship type dropdown - include capital ship types
        all_ship_types = ["All"] + sorted(list(set(self.registry.get_ship_types())))
        self.ship_type_dropdown = create_labeled_dropdown(
            selection_frame,
            "Ship Type:",
            self.selected_ship_type,
            all_ship_types,
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
        
        # Create quantity input and calculate button
        self._create_quantity_frame(
            selection_frame,
            self.ship_quantity,
            self.calculate_ship_requirements,
            quantity_attr_name="ship_quantity_entry",
            button_attr_name="calculate_button"
        )
        
        # Initialize the ship dropdown
        self.update_ship_dropdown()
    
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
        
        # Create quantity input and calculate button
        self._create_quantity_frame(
            selection_frame,
            self.component_quantity,
            self.calculate_component_requirements,
            quantity_attr_name="component_quantity_entry",
            button_attr_name="calculate_component_button"
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
        
        # Create quantity input and calculate button
        self._create_quantity_frame(
            selection_frame,
            self.pi_quantity,
            self.calculate_pi_requirements,
            quantity_attr_name="pi_quantity_entry",
            button_attr_name="calculate_pi_button"
        )
        
        # Initialize the PI material dropdown
        self.update_pi_material_dropdown()
    
    def _create_quantity_frame(self, parent, quantity_var, calculate_command, quantity_attr_name=None, button_attr_name=None):
        """
        Create a standard quantity input frame with calculate button
        
        Args:
            parent: Parent frame to add this frame to
            quantity_var: StringVar for the quantity input
            calculate_command: Command to execute when calculate button is pressed
            quantity_attr_name: Attribute name to store the quantity entry widget
            button_attr_name: Attribute name to store the calculate button widget
        """
        # Create quantity input frame
        quantity_frame = ttk.Frame(parent)
        quantity_frame.pack(fill="x", padx=5, pady=5)
        
        # Add quantity input field
        quantity_entry = create_labeled_entry(
            quantity_frame,
            "Quantity:",
            quantity_var,
            width=5,
            label_width=10
        )
        
        # Store reference if attribute name is provided
        if quantity_attr_name:
            setattr(self, quantity_attr_name, quantity_entry)
        
        # Calculate button
        calculate_button = create_button(
            quantity_frame,
            "Calculate Requirements",
            calculate_command
        )
        
        # Store reference if attribute name is provided
        if button_attr_name:
            setattr(self, button_attr_name, calculate_button)
        
        return quantity_frame
    
    def update_ship_details(self, event=None):
        """
        Update the ship details text based on selected ship
        
        Args:
            event: Tkinter event (optional)
        """
        self._update_details('ship', self.selected_ship.get(), self.registry.get_ship_by_display_name_combined)
    
    def update_component_details(self, event=None):
        """
        Update the component details text based on selected component
        
        Args:
            event: Tkinter event (optional)
        """
        self._update_details('component', self.selected_component.get(), self.registry.get_component_by_display_name)
    
    def update_pi_details(self, event=None):
        """
        Update the PI details text based on selected PI material
        
        Args:
            event: Tkinter event (optional)
        """
        self._update_details('PI material', self.pi_material_dropdown.get(), self.registry.get_pi_material_by_display_name)
    
    def _update_details(self, item_type, item_name, getter_func):
        """
        Generic method to update details text for an item
        
        Args:
            item_type: Type of item ('ship', 'component', or 'PI material')
            item_name: Name of the item to display details for
            getter_func: Function to retrieve the item from registry
        """
        if not item_name:
            set_text_content(self.output_text, f"No {item_type} selected.")
            return
            
        # Find item in registry
        item = getter_func(item_name)
        
        if not item:
            set_text_content(self.output_text, f"{item_type.capitalize()} '{item_name}' not found in registry.")
            return
            
        # Update details text
        set_text_content(self.output_text, item.details)
        
        # Enable calculate button for ships
        if item_type == 'ship' and hasattr(self, 'calculate_button'):
            self.calculate_button.configure(state="normal")
    
    def update_ship_dropdown(self, event=None):
        """Update the ship dropdown based on selected faction and type"""
        # Get the selected faction and type
        faction = self.selected_faction.get()
        ship_type = self.selected_ship_type.get()
        
        # Filter ships (passing True for owned_only to show only owned ships)
        # Now using the combined method that includes both regular and capital ships
        filtered_ships = self.registry.get_ships_combined_by_filter(
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
    
    def calculate_ship_requirements(self):
        """Calculate and display ship material requirements"""
        selected_item = self.selected_ship.get()
        quantity_var = self.ship_quantity
        
        if not self._validate_calculation_input(selected_item, 'ship', quantity_var):
            return
            
        # Find ship in registry
        item = self.registry.get_ship_by_display_name_combined(selected_item)
        
        # Calculate requirements based on item type
        is_capital_ship = isinstance(item, CapitalShipModule)
        config_category = 'capital_ship_blueprints' if is_capital_ship else 'ship_blueprints'
        
        if is_capital_ship:
            requirements = self.calculator.calculate_capital_ship_requirements(item.name)
        else:
            requirements = self.calculator.calculate_ship_requirements(item.name)
            
        # Format and display requirements with proper quantity
        self._display_requirements(item, requirements, config_category, int(quantity_var.get()))
    
    def calculate_component_requirements(self):
        """Calculate and display component material requirements"""
        selected_item = self.selected_component.get()
        quantity_var = self.component_quantity
        
        if not self._validate_calculation_input(selected_item, 'component', quantity_var):
            return
            
        # Find component in registry
        item = self.registry.get_component_by_display_name(selected_item)
        
        # Calculate requirements
        requirements = self.calculator.calculate_component_requirements(item.name)
        
        # Format and display requirements with proper quantity
        self._display_requirements(item, requirements, 'components', int(quantity_var.get()))
    
    def calculate_pi_requirements(self):
        """Calculate and display PI material requirements"""
        selected_item = self.pi_material_dropdown.get()
        quantity_var = self.pi_quantity
        
        if not self._validate_calculation_input(selected_item, 'PI material', quantity_var):
            return
            
        # Find PI material in registry
        item = self.registry.get_pi_material_by_display_name(selected_item)
        
        # Calculate requirements
        requirements = self.calculator.calculate_pi_requirements(item.name)
        
        # Format and display requirements with proper quantity
        self._display_requirements(item, requirements, 'pi_materials', int(quantity_var.get()))
    
    def _validate_calculation_input(self, selected_item, item_type, quantity_var):
        """
        Validate calculation inputs
        
        Args:
            selected_item: The selected item name
            item_type: Type of item (ship, component, PI material)
            quantity_var: The quantity StringVar
            
        Returns:
            bool: True if inputs are valid, False otherwise
        """
        if not selected_item:
            messagebox.showwarning("Warning", f"No {item_type} selected.")
            return False
        
        # Validate quantity
        try:
            quantity = int(quantity_var.get())
            if quantity < 1:
                quantity = 1
                quantity_var.set("1")
        except ValueError:
            quantity = 1
            quantity_var.set("1")
            
        return True
    
    def _display_requirements(self, item, requirements, config_category, quantity):
        """
        Format and display calculation requirements
        
        Args:
            item: The item module
            requirements: The calculated requirements dictionary
            config_category: The configuration category for ME/TE retrieval
            quantity: The number of items to produce
        """
        # Get ME and TE levels
        me_level = self.calculator.get_me_level(config_category, item.name)
        te_level = self.calculator.get_te_level(config_category, item.name)
        
        # Calculate production time
        base_time = getattr(item, 'production_time', 3600)  # Default to 1 hour if not specified
        production_time = self.calculator.calculate_production_time(base_time, te_level)
        
        # Format time for display
        hours, remainder = divmod(production_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        
        # Format requirements for display
        requirements_text = f"Material Requirements for {quantity}x {item.display_name} (ME: {me_level}%, TE: {te_level}%):\n\n"
        requirements_text += f"Production Time per Unit: {time_str}\n\n"
        
        # Sort materials alphabetically
        sorted_materials = sorted(requirements.items())
        
        for material, material_quantity in sorted_materials:
            # Multiply by quantity
            total_quantity = material_quantity * quantity
            requirements_text += f"{material}: {total_quantity:,.2f}\n"
            
        set_text_content(self.output_text, requirements_text)
    
    def edit_blueprint_ownership(self):
        """Open the Blueprint Ownership Editor"""
        open_blueprint_editor(
            self, 
            self.registry, 
            self.blueprint_config, 
            callback=self._on_editor_closed
        )
    
    def reset_ship_ownership(self):
        """Reset ownership status for all ships"""
        # Define refresh function
        def refresh_ui():
            current_tab = self.notebook.index(self.notebook.select())
            if current_tab == 0:  # Ships tab
                self.update_ship_dropdown()
        
        # Call the reset function
        reset_ship_ownership(
            self.registry,
            self.blueprint_config,
            refresh_callback=refresh_ui
        )
    
    def _on_editor_closed(self):
        """Callback to handle the blueprint editor being closed"""
        # Reset the ownership editor shown flag
        self.ownership_editor_shown = False
        
        # Apply the changes
        apply_blueprint_changes(self.blueprint_config, self.registry)
        
        # Refresh the UI based on the current tab
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:  # Ships tab
            self.update_ship_dropdown()
    
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

    def _create_menus(self):
        """Create menu bar items"""
        # Create menu bar
        menubar = tk.Menu(self)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Export Settings", command=self.export_settings)
        file_menu.add_command(label="Import Settings", command=self.import_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_close)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Settings", command=self.open_settings)
        settings_menu.add_separator()
        settings_menu.add_command(label="Edit Blueprint Ownership", command=self.edit_blueprint_ownership)
        settings_menu.add_command(label="Reset Ship Ownership", command=self.reset_ship_ownership)
        menubar.add_cascade(label="Options", menu=settings_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        # Set the menu bar
        self.config(menu=menubar)
    
    def open_settings(self):
        """Open the settings window"""
        settings_window = SettingsWindow(self, self.registry, self.calculator, self.blueprint_config)
    
    def apply_theme(self, theme):
        """Apply the selected theme to the application"""
        if theme == "dark":
            self.configure(bg="#2e2e2e")
            style = ttk.Style(self)
            style.theme_use('clam')  # Use clam as base
            
            # Configure the dark theme
            style.configure("TFrame", background="#2e2e2e")
            style.configure("TLabel", background="#2e2e2e", foreground="#ffffff")
            style.configure("TButton", background="#3c3c3c", foreground="#ffffff")
            style.configure("TNotebook", background="#2e2e2e", foreground="#ffffff")
            style.configure("TNotebook.Tab", background="#3c3c3c", foreground="#ffffff")
            style.map("TNotebook.Tab",
                background=[("selected", "#4c4c4c"), ("active", "#3c3c3c")],
                foreground=[("selected", "#ffffff"), ("active", "#ffffff")])
            
            # Configure the Labelframe
            style.configure("TLabelframe", background="#2e2e2e", foreground="#ffffff")
            style.configure("TLabelframe.Label", background="#2e2e2e", foreground="#ffffff")
            
            # Configure the Combobox
            style.configure("TCombobox", fieldbackground="#3c3c3c", background="#3c3c3c", foreground="#ffffff")
            
            # Configure Text widgets
            self.output_text.config(bg="#3c3c3c", fg="#ffffff", insertbackground="#ffffff")
        else:
            # Reset to default theme
            style = ttk.Style(self)
            style.theme_use('default')
            
            # Reset Text widget colors
            self.output_text.config(bg="white", fg="black", insertbackground="black")
        
        # Update settings
        self.settings['theme'] = theme
    
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
        
        try:
            # Create export data combining blueprint config and other settings
            export_data = {
                "blueprint_config": self.blueprint_config,
                "app_settings": self.settings
            }
            
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=4)
            messagebox.showinfo("Success", "Settings exported successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export settings: {str(e)}")
    
    def import_settings(self):
        """Import settings from a JSON file"""
        # Ask for file location
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Import Settings"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r') as f:
                imported_data = json.load(f)
            
            # Import blueprint config if available
            if "blueprint_config" in imported_data:
                self.blueprint_config.update(imported_data["blueprint_config"])
                
                # Apply blueprint ownership
                from core.config.blueprint_config import apply_blueprint_ownership
                apply_blueprint_ownership(self.blueprint_config, self.registry)
                
                # Update UI
                self.update_ship_dropdown()
            
            # Import app settings if available
            if "app_settings" in imported_data:
                self.settings.update(imported_data["app_settings"])
                
                # Apply theme
                if "theme" in imported_data["app_settings"]:
                    self.apply_theme(imported_data["app_settings"]["theme"])
            
            messagebox.showinfo("Success", "Settings imported successfully.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import settings: {str(e)}")
        
    def show_help(self):
        """Display help information"""
        help_text = """
EVE Production Calculator Help

Ship Tab:
- Select a faction and ship type to filter the ship list
- Choose a ship from the dropdown to view its details
- Enter the quantity and click Calculate to see the resource requirements

Components Tab:
- Select a component to view its details
- Enter the quantity and click Calculate to see the resource requirements

PI Materials Tab:
- Select a PI level to filter the materials
- Choose a material to view its details
- Enter the quantity and click Calculate to see the resource requirements

Blueprint Ownership:
- Access the Blueprint Ownership Editor from the Blueprints menu
- Set which blueprints you own by using the radio buttons
- Ownership status affects which ships appear in the "Only Owned" filter

Settings:
- Change theme between light and dark mode
- Export or import your settings to backup your configuration
"""
        help_window = tk.Toplevel(self)
        help_window.title("Help")
        help_window.geometry("600x500")
        help_window.minsize(500, 400)
        
        # Help text widget
        help_text_widget = tk.Text(help_window, wrap="word", padx=10, pady=10)
        help_text_widget.pack(fill="both", expand=True)
        help_text_widget.insert("1.0", help_text)
        help_text_widget.config(state="disabled")
        
        # Apply current theme to help window
        if self.settings.get('theme') == 'dark':
            help_window.config(bg="#2e2e2e")
            help_text_widget.config(bg="#3c3c3c", fg="#ffffff")
    
    def show_about(self):
        """Display about information"""
        about_text = """
EVE Production Calculator

Version: 1.0.0

A tool for calculating resource requirements for manufacturing ships, 
components, and managing Planetary Interaction (PI) materials in EVE Online.

Features:
- Ship production calculation
- Component production calculation
- PI material processing
- Blueprint ownership management
- Dark mode support
- Settings import/export

 2025 EVE Production Calculator
"""
        messagebox.showinfo("About", about_text)
        
    def on_close(self):
        """Handle window close event"""
        # Save blueprint configuration
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'blueprint_ownership.json'), 'w') as f:
            json.dump(self.blueprint_config, f, indent=4)
        
        # Save settings
        save_settings(self.settings)
        
        # Destroy the window
        self.destroy()
