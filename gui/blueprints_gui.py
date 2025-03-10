"""
Blueprint management GUI components for EVE Production Calculator
This file contains the UI components and logic for blueprint management
"""

import tkinter as tk
from tkinter import ttk
import json
import os
from collections import defaultdict

# Import blueprint configuration utilities
from config.blueprint_config import (
    get_blueprint_ownership, update_blueprint_ownership, get_blueprint_me, get_blueprint_te, 
    update_blueprint_me, update_blueprint_te, 
    update_blueprint_invention, save_blueprint_ownership,
    load_blueprint_ownership
)

from tkinter import messagebox

class BlueprintManager:
    """
    Blueprint management class for handling blueprint ownership and invention status
    for EVE Online ships, capital ships, components, and capital components.
    """
    
    def __init__(self, parent, discovered_modules, blueprint_config, module_registry):
        """
        Initialize the blueprint manager
        
        Args:
            parent: The parent tkinter application
            discovered_modules: Dictionary of discovered modules
            blueprint_config: Blueprint configuration
            module_registry: Module registry
        """
        self.parent = parent
        self.discovered_modules = discovered_modules
        self.blueprint_config = blueprint_config
        self.module_registry = module_registry
        
        # Initialize status variable
        if hasattr(parent, 'status_var'):
            self.status_var = parent.status_var
        else:
            self.status_var = tk.StringVar()
            self.status_var.set("Ready")
        
        # Initialize capital component variables
        self.initialize_capital_component_vars()
    
    def create_blueprint_management_tab(self, parent_tab):
        """Create the main blueprint management tab"""
        # Create notebook for different blueprint types
        notebook = ttk.Notebook(parent_tab)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create main tabs
        ships_tab = ttk.Frame(notebook)
        capital_ships_tab = ttk.Frame(notebook)
        components_tab = ttk.Frame(notebook)
        
        # Add tabs to notebook
        notebook.add(ships_tab, text="Ships")
        notebook.add(capital_ships_tab, text="Capital Ships")
        notebook.add(components_tab, text="Components")
        
        # Create ship blueprint management tab
        self.create_ships_blueprint_tab(ships_tab)
        
        # Create capital ship blueprint management tab
        self.create_capital_ships_blueprint_tab(capital_ships_tab)
        
        # Create components blueprint tab (includes both regular and capital components)
        self.create_components_blueprint_tab(components_tab)
        
        # Create save frame at the bottom
        save_frame = ttk.Frame(parent_tab)
        save_frame.pack(fill="x", padx=10, pady=10)
        
        # Add save button
        save_button = ttk.Button(save_frame, text="Save Configuration", 
                                command=self.save_blueprint_config)
        save_button.pack(side="right", padx=5)
    
    def create_ships_blueprint_tab(self, parent_tab):
        """Create the ships blueprint tab"""
        if 'ships' in self.discovered_modules:
            # Frame for ship blueprint management
            ship_frame = ttk.LabelFrame(parent_tab, text="Ship Blueprints")
            ship_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create grid view for ships
            self.create_ship_blueprint_grid(ship_frame)
        else:
            ttk.Label(parent_tab, text="No ship modules discovered").pack(padx=10, pady=10)
    
    def create_capital_ships_blueprint_tab(self, parent_tab):
        """Create the capital ships blueprint tab"""
        if 'capital_ships' in self.discovered_modules:
            # Frame for capital ship blueprint management
            cap_ship_frame = ttk.LabelFrame(parent_tab, text="Capital Ship Blueprints")
            cap_ship_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create grid view for capital ships
            self.create_capital_ship_blueprint_grid(cap_ship_frame)
        else:
            ttk.Label(parent_tab, text="No capital ship modules discovered").pack(padx=10, pady=10)
    
    def create_components_blueprint_tab(self, parent_tab):
        """Create the components blueprint tab for both regular and capital components"""
        # Container for all components
        components_container = ttk.Frame(parent_tab)
        components_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create frame for regular components if they exist
        if 'components' in self.discovered_modules and self.discovered_modules['components']:
            component_frame = ttk.LabelFrame(components_container, text="Component Blueprints")
            component_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create grid view for components
            self.create_component_blueprint_grid(component_frame)
        
        # Create frame for capital components if they exist
        if hasattr(self.module_registry, 'capital_components') and self.module_registry.capital_components:
            cap_component_frame = ttk.LabelFrame(components_container, text="Capital Component Blueprints")
            cap_component_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Store capital components in discovered_modules for consistency
            self.discovered_modules['capital_components'] = self.module_registry.capital_components
            
            # Create grid for capital component blueprints
            self.create_capital_component_blueprint_grid(cap_component_frame)
        
        # Display message if no components found
        if (not 'components' in self.discovered_modules or not self.discovered_modules['components']) and (not hasattr(self.module_registry, 'capital_components') or not self.module_registry.capital_components):
            ttk.Label(components_container, text="No component modules discovered").pack(padx=10, pady=5)
    
    def create_capital_components_blueprint_tab(self, parent_tab):
        """Create the capital components blueprint tab"""
        if 'capital_components' in self.discovered_modules:
            # Frame for capital component blueprint management
            cap_component_frame = ttk.LabelFrame(parent_tab, text="Capital Component Blueprints")
            cap_component_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create grid view for capital components
            self.create_capital_component_blueprint_grid(cap_component_frame)
        else:
            ttk.Label(parent_tab, text="No capital component modules discovered").pack(padx=10, pady=10)
    
    def create_ship_blueprint_grid(self, parent):
        """Create a grid for ship blueprints"""
        if 'ships' in self.discovered_modules:
            self.create_blueprint_grid(parent, "Ships", self.discovered_modules['ships'])
        else:
            ttk.Label(parent, text="No ship modules discovered.").pack(padx=10, pady=10)
    
    def create_capital_ship_blueprint_grid(self, parent):
        """Create a grid for capital ship blueprints"""
        if 'capital_ships' in self.discovered_modules:
            self.create_blueprint_grid(parent, "Capital Ships", self.discovered_modules['capital_ships'])
        else:
            ttk.Label(parent, text="No capital ship modules discovered.").pack(padx=10, pady=10)
    
    def create_component_blueprint_grid(self, parent):
        """Create a grid for component blueprints"""
        if 'components' in self.discovered_modules:
            self.create_component_blueprint_grid_without_filters(parent, "Components", self.discovered_modules['components'])
        else:
            ttk.Label(parent, text="No component modules discovered.").pack(padx=10, pady=10)
    
    def create_capital_component_blueprint_grid(self, parent_tab):
        """Create a grid for capital component blueprints"""
        # Create a frame with scrollbar
        frame = ttk.Frame(parent_tab)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create scrollable canvas
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create a frame for grid contents
        grid_frame = ttk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=grid_frame, anchor="nw")
        
        # Add headers
        ttk.Label(grid_frame, text="Capital Component Blueprint", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(grid_frame, text="Unowned", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(grid_frame, text="Owned", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(grid_frame, text="ME%", font=("Arial", 10, "bold")).grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(grid_frame, text="TE%", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5, pady=5)
        
        # Add separator
        separator = ttk.Separator(grid_frame, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=5, sticky="ew", pady=5)
        
        # Populate grid with capital component blueprints
        row = 2
        if 'capital_components' in self.discovered_modules:
            for comp_name, comp_data in sorted(self.discovered_modules['capital_components'].items()):
                # Display name
                ttk.Label(grid_frame, text=comp_data.display_name).grid(row=row, column=0, padx=5, pady=2, sticky="w")
                
                # Create ownership variable if it doesn't exist
                if not hasattr(comp_data, 'ownership_var'):
                    comp_data.ownership_var = tk.StringVar()
                
                # Get current ownership status and set the radio button variable
                ownership = get_blueprint_ownership(self.blueprint_config, 'component_blueprints', comp_name)
                # Convert to lowercase to match radio button values
                if ownership == "Owned":
                    comp_data.ownership_var.set("owned")
                elif ownership == "Unowned":
                    comp_data.ownership_var.set("unowned")
                else:
                    comp_data.ownership_var.set("unowned")  # Default to unowned
                
                # Unowned radiobutton
                ttk.Radiobutton(
                    grid_frame, 
                    value="unowned", 
                    variable=comp_data.ownership_var,
                    command=lambda n=comp_name, d=comp_data, v="unowned": self.update_cap_component_ownership(n, d, v)
                ).grid(row=row, column=1, padx=5, pady=2)
                
                # Owned radiobutton
                ttk.Radiobutton(
                    grid_frame, 
                    value="owned", 
                    variable=comp_data.ownership_var,
                    command=lambda n=comp_name, d=comp_data, v="owned": self.update_cap_component_ownership(n, d, v)
                ).grid(row=row, column=2, padx=5, pady=2)
                
                # ME% input field
                if not hasattr(comp_data, 'me_var'):
                    comp_data.me_var = tk.StringVar()
                me_value = get_blueprint_me(self.blueprint_config, 'component_blueprints', comp_name)
                comp_data.me_var.set(str(me_value))
                me_entry = ttk.Entry(grid_frame, width=4, textvariable=comp_data.me_var)
                me_entry.grid(row=row, column=3, padx=5, pady=2)
                me_entry.bind("<FocusOut>", lambda event, n=comp_name: self.validate_capital_component_me(event, n))
                
                # TE% input field
                if not hasattr(comp_data, 'te_var'):
                    comp_data.te_var = tk.StringVar()
                te_value = get_blueprint_te(self.blueprint_config, 'component_blueprints', comp_name)
                comp_data.te_var.set(str(te_value))
                te_entry = ttk.Entry(grid_frame, width=4, textvariable=comp_data.te_var)
                te_entry.grid(row=row, column=4, padx=5, pady=2)
                te_entry.bind("<FocusOut>", lambda event, n=comp_name: self.validate_capital_component_te(event, n))
                
                row += 1
        
        # Configure the canvas to adjust scrolling based on the grid size
        grid_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        # Make sure the canvas size changes with window size
        def _configure_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=event.width)
            
        frame.bind("<Configure>", _configure_canvas)
    
    def create_blueprint_grid(self, parent, modules_type, modules_dict):
        """Create a grid view for blueprint management"""
        # Container with scrollbar
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Add filter frame at the top
        filter_frame = ttk.Frame(container)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create filter options - Ship Type and Faction
        ttk.Label(filter_frame, text="Ship Type:").grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")
        ship_type_var = tk.StringVar(value="All")
        ship_types = ["All"]
        
        # Faction filter
        ttk.Label(filter_frame, text="Faction:").grid(row=0, column=2, padx=(15, 5), pady=5, sticky="w")
        faction_var = tk.StringVar(value="All")
        factions = ["All"]
        
        # Extract available ship types and factions
        for module_name, module in modules_dict.items():
            # Extract ship type
            if hasattr(module, 'ship_type') and module.ship_type not in ship_types:
                ship_types.append(module.ship_type)
            
            # Extract faction
            if hasattr(module, 'faction') and module.faction not in factions:
                factions.append(module.faction)
        
        # Create dropdown menus
        ship_type_dropdown = ttk.Combobox(filter_frame, textvariable=ship_type_var, values=ship_types, state="readonly", width=20)
        ship_type_dropdown.grid(row=0, column=1, padx=0, pady=5, sticky="w")
        
        faction_dropdown = ttk.Combobox(filter_frame, textvariable=faction_var, values=factions, state="readonly", width=20)
        faction_dropdown.grid(row=0, column=3, padx=0, pady=5, sticky="w")
        
        # Create a search button
        apply_filter_btn = ttk.Button(filter_frame, text="Apply Filter", 
                                     command=lambda: self.populate_grid(grid_frame, modules_type, modules_dict, ship_type_var.get(), faction_var.get()))
        apply_filter_btn.grid(row=0, column=4, padx=15, pady=5)
        
        # Reset button
        reset_filter_btn = ttk.Button(filter_frame, text="Reset", 
                                    command=lambda: self.reset_filter(ship_type_dropdown, faction_dropdown, grid_frame, modules_type, modules_dict))
        reset_filter_btn.grid(row=0, column=5, padx=5, pady=5)
        
        # Add canvas and scrollbar
        canvas_frame = ttk.Frame(container)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        canvas = tk.Canvas(canvas_frame)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
        
        # Configure scrollbars
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.configure(yscrollcommand=scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Create frame for grid
        grid_frame = ttk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=grid_frame, anchor="nw")
        
        # Add headers
        ttk.Label(grid_frame, text=f"{modules_type} Blueprint", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(grid_frame, text="Ship Type", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(grid_frame, text="Faction", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(grid_frame, text="Unowned", font=("Arial", 10, "bold")).grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(grid_frame, text="Owned", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5, pady=5)
        ttk.Label(grid_frame, text="ME%", font=("Arial", 10, "bold")).grid(row=0, column=5, padx=5, pady=5)
        ttk.Label(grid_frame, text="TE%", font=("Arial", 10, "bold")).grid(row=0, column=6, padx=5, pady=5)
        
        # Separator
        separator = ttk.Separator(grid_frame, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=7, sticky="ew", padx=5, pady=2)
        
        # Populate the grid
        self.populate_grid(grid_frame, modules_type, modules_dict)
        
        # Configure the canvas
        def _configure_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Set min width to avoid shrinking
            canvas.itemconfig(canvas_window, width=max(event.width, grid_frame.winfo_reqwidth()))
        
        grid_frame.bind("<Configure>", _configure_canvas)
        canvas.bind("<Configure>", _configure_canvas)
        
    def create_component_blueprint_grid_without_filters(self, parent, modules_type, modules_dict):
        """Create a grid view for blueprint management without ship filters"""
        # Container with scrollbar
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create a canvas with scrollbar
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create frame for grid
        grid_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=grid_frame, anchor="nw")
        
        # Add headers
        ttk.Label(grid_frame, text="Component Blueprint", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(grid_frame, text="Unowned", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(grid_frame, text="Owned", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(grid_frame, text="ME%", font=("Arial", 10, "bold")).grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(grid_frame, text="TE%", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5, pady=5)
        
        # Add separator
        separator = ttk.Separator(grid_frame, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=5, sticky="ew", pady=5)
        
        # Populate grid with components
        row = 2
        for comp_name, comp_data in sorted(modules_dict.items()):
            # Component name
            ttk.Label(grid_frame, text=comp_data.display_name).grid(row=row, column=0, padx=5, pady=2, sticky="w")
            
            # Ownership RadioButtons
            # Check if the comp_data already has an ownership_var attribute, if not create one
            if not hasattr(comp_data, 'ownership_var'):
                comp_data.ownership_var = tk.StringVar(value=get_blueprint_ownership(self.blueprint_config, 'components', comp_name))
            
            # Unowned radiobutton
            ttk.Radiobutton(
                grid_frame, 
                value="unowned", 
                variable=comp_data.ownership_var,
                command=lambda n=comp_name, v="unowned": update_blueprint_ownership(self.blueprint_config, 'components', n, v)
            ).grid(row=row, column=1, padx=5, pady=2)
            
            # Owned radiobutton
            ttk.Radiobutton(
                grid_frame, 
                value="owned", 
                variable=comp_data.ownership_var,
                command=lambda n=comp_name, v="owned": update_blueprint_ownership(self.blueprint_config, 'components', n, v)
            ).grid(row=row, column=2, padx=5, pady=2)
            
            # ME% input field
            if not hasattr(comp_data, 'me_var'):
                comp_data.me_var = tk.StringVar()
            me_value = get_blueprint_me(self.blueprint_config, 'components', comp_name)
            comp_data.me_var.set(str(me_value))
            me_entry = ttk.Entry(grid_frame, width=4, textvariable=comp_data.me_var)
            me_entry.grid(row=row, column=3, padx=5, pady=2)
            me_entry.bind("<FocusOut>", lambda event, n=comp_name: self.validate_me(event, 'components', n))
            
            # TE% input field
            if not hasattr(comp_data, 'te_var'):
                comp_data.te_var = tk.StringVar()
            te_value = get_blueprint_te(self.blueprint_config, 'components', comp_name)
            comp_data.te_var.set(str(te_value))
            te_entry = ttk.Entry(grid_frame, width=4, textvariable=comp_data.te_var)
            te_entry.grid(row=row, column=4, padx=5, pady=2)
            te_entry.bind("<FocusOut>", lambda event, n=comp_name: self.validate_te(event, 'components', n))
            
            row += 1
        
        # Configure the canvas to adjust scrolling based on the grid size
        grid_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    
    def populate_grid(self, grid_frame, modules_type, modules_dict, ship_type_filter="All", faction_filter="All"):
        """Populate the grid with modules that match the filter criteria"""
        # Clear existing grid content (except headers and separator)
        for widget in grid_frame.winfo_children():
            grid_info = widget.grid_info()
            if grid_info and int(grid_info['row']) > 1:  # Skip headers and separator
                widget.destroy()
        
        row = 2
        for module_name, module in modules_dict.items():
            display_name = getattr(module, 'display_name', module_name)
            ship_type = getattr(module, 'ship_type', '')
            faction = getattr(module, 'faction', '')
            
            # Apply filters
            if (ship_type_filter != "All" and ship_type != ship_type_filter) or \
               (faction_filter != "All" and faction != faction_filter):
                continue
            
            # Get current ownership status, properly handling boolean values
            if hasattr(module, 'ownership_var'):
                current_status = module.ownership_var.get() if hasattr(module.ownership_var, 'get') else module.ownership_var
            else:
                # Get current ownership status from module attributes
                if hasattr(module, 'owned_status'):
                    # Convert boolean to string representation if needed
                    if isinstance(module.owned_status, bool):
                        current_status = "Owned" if module.owned_status else "Unowned"
                    else:
                        current_status = module.owned_status
                elif hasattr(module, 'blueprint_owned'):
                    # Convert boolean to string representation if needed
                    if isinstance(module.blueprint_owned, bool):
                        current_status = "Owned" if module.blueprint_owned else "Unowned" 
                    else:
                        current_status = module.blueprint_owned
                else:
                    current_status = "Unowned"
            
            # Create variable to track ownership status
            ownership_var = tk.StringVar()
            ownership_var.set(current_status)
            
            # Create variable to track ME%
            me_var = tk.StringVar()
            
            # Get ME% from config
            category = self.get_category_from_module_type(modules_type)
            me_value = get_blueprint_me(self.blueprint_config, category, module_name)
            me_var.set(str(me_value))
            
            # Create variable to track TE%
            te_var = tk.StringVar()
            
            # Get TE% from config
            te_value = get_blueprint_te(self.blueprint_config, category, module_name)
            te_var.set(str(te_value))
            
            # Store these variables in the module for later reference
            module.ownership_var = ownership_var
            module.me_var = me_var  # Store ME% variable
            module.te_var = te_var  # Store TE% variable
            
            # Add blueprint name
            ttk.Label(grid_frame, text=display_name).grid(row=row, column=0, padx=5, pady=2, sticky="w")
            
            # Add ship type and faction if available
            ttk.Label(grid_frame, text=ship_type).grid(row=row, column=1, padx=5, pady=2)
            ttk.Label(grid_frame, text=faction).grid(row=row, column=2, padx=5, pady=2)
            
            # Radio buttons for Unowned/Owned
            ttk.Radiobutton(grid_frame, variable=ownership_var, value="Unowned",
                           command=lambda m=module: self.update_module_ownership(m, "Unowned")).grid(row=row, column=3, padx=5, pady=2)
            ttk.Radiobutton(grid_frame, variable=ownership_var, value="Owned",
                           command=lambda m=module: self.update_module_ownership(m, "Owned")).grid(row=row, column=4, padx=5, pady=2)
            
            # Entry for ME%
            me_entry = ttk.Entry(grid_frame, width=4, textvariable=me_var)
            me_entry.grid(row=row, column=5, padx=5, pady=2)
            me_entry.bind("<FocusOut>", lambda event, m=module: self.validate_me_entry(m))
            
            # Entry for TE%
            te_entry = ttk.Entry(grid_frame, width=4, textvariable=te_var)
            te_entry.grid(row=row, column=6, padx=5, pady=2)
            te_entry.bind("<FocusOut>", lambda event, m=module: self.validate_te_entry(m))
            
            row += 1
            
    def apply_filter(self, grid_frame, modules_dict, ship_type_filter, faction_filter):
        """Apply filter to the blueprint grid"""
        # Get the modules_type from grid_frame's master window title
        parent = grid_frame.master.master.master  # Canvas > Frame > Container
        modules_type = None
        for item in parent.winfo_children():
            if isinstance(item, ttk.LabelFrame):
                modules_type = item.cget("text").replace(" Blueprints", "")
                break
        
        if modules_type:
            self.populate_grid(grid_frame, modules_type, modules_dict, ship_type_filter, faction_filter)
        
    def reset_filter(self, ship_type_dropdown, faction_dropdown, grid_frame, modules_type, modules_dict):
        """Reset filters to show all modules"""
        ship_type_dropdown.set("All")
        faction_dropdown.set("All")
        self.populate_grid(grid_frame, modules_type, modules_dict)
            
    def get_category_from_module_type(self, module_type):
        """
        Convert module type string to config category key
        
        Args:
            module_type: String name of module type (e.g., 'Ships', 'Capital Ships')
            
        Returns:
            Category key for the blueprint config (e.g., 'ships', 'capital_ships')
        """
        module_map = {
            'Ships': 'ships',
            'Capital Ships': 'capital_ships',
            'Components': 'components',
            'Capital Components': 'component_blueprints'
        }
        return module_map.get(module_type, module_type.lower())
        
    def validate_me_entry(self, module):
        """
        Validate ME% entry to ensure it's a valid number
        
        Args:
            module: Module with ME% entry to validate
        """
        try:
            # Get ME% value
            me_value = int(module.me_var.get())
            
            # Validate ME% (0-10 is typical range in EVE)
            if me_value < 0:
                me_value = 0
            elif me_value > 10:
                me_value = 10
                
            # Set validated value
            module.me_var.set(str(me_value))
            
            # Get the category for this module
            for category_type, modules in self.discovered_modules.items():
                if module in modules.values():
                    category = self.get_category_from_module_type(category_type)
                    module_name = next(name for name, mod in modules.items() if mod == module)
                    update_blueprint_me(self.blueprint_config, category, module_name, me_value)
                    break
            
        except ValueError:
            # Reset to 0 if invalid
            module.me_var.set("0")
    
    def validate_te_entry(self, module):
        """
        Validate TE% entry to ensure it's a valid number
        
        Args:
            module: Module with TE% entry to validate
        """
        try:
            # Get TE% value
            te_value = int(module.te_var.get())
            
            # Validate TE% (0-20 is typical range in EVE)
            if te_value < 0:
                te_value = 0
            elif te_value > 20:
                te_value = 20
                
            # Set validated value
            module.te_var.set(str(te_value))
            
            # Get the category for this module
            for category_type, modules in self.discovered_modules.items():
                if module in modules.values():
                    category = self.get_category_from_module_type(category_type)
                    module_name = next(name for name, mod in modules.items() if mod == module)
                    update_blueprint_te(self.blueprint_config, category, module_name, te_value)
                    break
            
        except ValueError:
            # Reset to 0 if invalid
            module.te_var.set("0")
    
    def validate_capital_component_me(self, event, comp_name):
        """
        Validate ME% entry for capital components
        
        Args:
            event: FocusOut event
            comp_name: Name of the capital component
        """
        try:
            # Get ME% value from the entry widget
            me_entry = event.widget
            me_value = int(me_entry.get())
            
            # Validate ME% (0-10 is typical range in EVE)
            if me_value < 0:
                me_value = 0
            elif me_value > 10:
                me_value = 10
                
            # Set validated value
            me_entry.delete(0, tk.END)
            me_entry.insert(0, str(me_value))
            
            # Update blueprint config
            update_blueprint_me(self.blueprint_config, 'component_blueprints', comp_name, me_value)
            
        except ValueError:
            # Reset to 0 if invalid
            me_entry.delete(0, tk.END)
            me_entry.insert(0, "0")
    
    def validate_capital_component_te(self, event, comp_name):
        """
        Validate TE% entry for capital components
        
        Args:
            event: FocusOut event
            comp_name: Name of the capital component
        """
        try:
            # Get TE% value from the entry widget
            te_entry = event.widget
            te_value = int(te_entry.get())
            
            # Validate TE% (0-20 is typical range in EVE)
            if te_value < 0:
                te_value = 0
            elif te_value > 20:
                te_value = 20
                
            # Set validated value
            te_entry.delete(0, tk.END)
            te_entry.insert(0, str(te_value))
            
            # Update blueprint config
            update_blueprint_te(self.blueprint_config, 'component_blueprints', comp_name, te_value)
            
        except ValueError:
            # Reset to 0 if invalid
            te_entry.delete(0, tk.END)
            te_entry.insert(0, "0")
    
    def create_blueprint_window(self, blueprint_window):
        """Create the blueprint management window interface"""
        # Configure the window to use the full screen (maximize)
        width = self.parent.winfo_screenwidth() - 100
        height = self.parent.winfo_screenheight() - 100
        blueprint_window.geometry(f"{width}x{height}+50+50")
        
        # Create notebook for tabs
        blueprint_notebook = ttk.Notebook(blueprint_window)
        blueprint_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs for each type of blueprint
        ships_tab = ttk.Frame(blueprint_notebook)
        capital_ships_tab = ttk.Frame(blueprint_notebook)
        components_tab = ttk.Frame(blueprint_notebook)
        
        # Add tabs to notebook
        blueprint_notebook.add(ships_tab, text="Ships")
        blueprint_notebook.add(capital_ships_tab, text="Capital Ships")
        blueprint_notebook.add(components_tab, text="Components")
        
        # Create content for each tab
        self.create_ship_blueprint_grid(ships_tab)
        self.create_capital_ship_blueprint_grid(capital_ships_tab)
        self.create_component_blueprint_grid(components_tab)
        
        # Add Save All button at the bottom
        button_frame = ttk.Frame(blueprint_window)
        button_frame.pack(fill="x", pady=10)
        
        save_button = ttk.Button(button_frame, text="Save All", command=self.save_all_blueprint_ownership)
        save_button.pack(side="right", padx=20)
        
    def show_blueprint_grid(self):
        """Show blueprint management in a popup window"""
        blueprint_window = tk.Toplevel(self.parent)
        blueprint_window.title("Blueprint Management")
        blueprint_window.geometry("800x600")
        
        # Create the blueprint window interface
        self.create_blueprint_window(blueprint_window)
    
    def save_all_blueprint_ownership(self):
        """Save all blueprint ownership data to configuration"""
        try:
            # Save ships
            if 'ships' in self.discovered_modules:
                for ship_name, ship_module in self.discovered_modules['ships'].items():
                    if hasattr(ship_module, 'ownership_var'):
                        if isinstance(ship_module.ownership_var, tk.StringVar):
                            ownership_status = ship_module.ownership_var.get()
                        else:
                            ownership_status = ship_module.ownership_var
                            
                        # Update the module's ownership status
                        if hasattr(ship_module, 'blueprint_owned'):
                            ship_module.blueprint_owned = ownership_status
                        elif hasattr(ship_module, 'owned_status'):
                            ship_module.owned_status = ownership_status
                            
                        # Save to config
                        update_blueprint_ownership(self.blueprint_config, 'ships', ship_name, ownership_status)
            
            # Save capital ships
            if 'capital_ships' in self.discovered_modules:
                for ship_name, ship_module in self.discovered_modules['capital_ships'].items():
                    if hasattr(ship_module, 'ownership_var'):
                        if isinstance(ship_module.ownership_var, tk.StringVar):
                            ownership_status = ship_module.ownership_var.get()
                        else:
                            ownership_status = ship_module.ownership_var
                            
                        # Update the module's ownership status
                        if hasattr(ship_module, 'blueprint_owned'):
                            ship_module.blueprint_owned = ownership_status
                        elif hasattr(ship_module, 'owned_status'):
                            ship_module.owned_status = ownership_status
                            
                        # Save to config
                        update_blueprint_ownership(self.blueprint_config, 'capital_ships', ship_name, ownership_status)
            
            # Save components
            if 'components' in self.discovered_modules:
                for comp_name, comp_module in self.discovered_modules['components'].items():
                    if hasattr(comp_module, 'ownership_var'):
                        if isinstance(comp_module.ownership_var, tk.StringVar):
                            ownership_status = comp_module.ownership_var.get()
                        else:
                            ownership_status = comp_module.ownership_var
                            
                        # Update the module's ownership status
                        if hasattr(comp_module, 'blueprint_owned'):
                            comp_module.blueprint_owned = ownership_status
                        elif hasattr(comp_module, 'owned_status'):
                            comp_module.owned_status = ownership_status
                            
                        # Save to config
                        update_blueprint_ownership(self.blueprint_config, 'components', comp_name, ownership_status)
            
            # Save capital components
            if 'capital_components' in self.discovered_modules:
                for comp_name, comp_data in self.discovered_modules['capital_components'].items():
                    if 'ownership_var' in comp_data:
                        if isinstance(comp_data['ownership_var'], tk.StringVar):
                            ownership_status = comp_data['ownership_var'].get()
                        else:
                            ownership_status = comp_data['ownership_var']
                            
                        # Update the data
                        comp_data['blueprint_owned'] = ownership_status
                        
                        # Save to config using correct category
                        update_blueprint_ownership(self.blueprint_config, 'component_blueprints', comp_name, ownership_status)
            
            # Save ME%
            for category, modules in self.discovered_modules.items():
                for module_name, module in modules.items():
                    if hasattr(module, 'me_var'):
                        try:
                            me_value = int(module.me_var.get())
                            # Ensure ME is not negative
                            if me_value < 0:
                                me_value = 0
                                module.me_var.set("0")
                            # Update the ME in config
                            update_blueprint_me(self.blueprint_config, category, module_name, me_value)
                        except ValueError:
                            # Invalid ME value, set to 0
                            module.me_var.set("0")
                            update_blueprint_me(self.blueprint_config, category, module_name, 0)
            
            # Save TE%
            for category, modules in self.discovered_modules.items():
                for module_name, module in modules.items():
                    if hasattr(module, 'te_var'):
                        try:
                            te_value = int(module.te_var.get())
                            # Ensure TE is not negative
                            if te_value < 0:
                                te_value = 0
                                module.te_var.set("0")
                            # Update the TE in config
                            update_blueprint_te(self.blueprint_config, category, module_name, te_value)
                        except ValueError:
                            # Invalid TE value, set to 0
                            module.te_var.set("0")
                            update_blueprint_te(self.blueprint_config, category, module_name, 0)
        
            self.status_var.set("All blueprint ownership settings saved successfully")
        except Exception as e:
            self.status_var.set(f"Error saving blueprint ownership: {str(e)}")
    
    def update_invented_status(self, module):
        """Update the 'Invented' status for a module (separate from owned status)"""
        # Get the invented checkbox status - handle both boolean and BooleanVar
        if hasattr(module, 'invented_var'):
            if isinstance(module.invented_var, bool):
                is_invented = module.invented_var
            else:
                # It's a tkinter BooleanVar
                is_invented = module.invented_var.get()
        else:
            # Default to False if not found
            is_invented = False
        
        # Determine module type from where it's found in discovered_modules
        module_type = None
        module_name = None
        
        for category, modules in self.discovered_modules.items():
            if category in ['ships', 'capital_ships', 'components']:
                for name, mod in modules.items():
                    if mod == module:
                        module_type = category
                        module_name = name
                        break
                if module_type:
                    break
        
        if module_type and module_name:
            # Save to config
            update_blueprint_invention(self.blueprint_config, module_type, module_name, is_invented)
            self.status_var.set(f"Updated invention status for {getattr(module, 'display_name', 'unknown module')} to {is_invented}")
        else:
            self.status_var.set(f"Could not determine module type for {getattr(module, 'display_name', 'unknown module')}")
    
    def update_module_ownership(self, module, ownership_status):
        """
        Update the ownership status for a module
        
        Args:
            module: The module to update
            ownership_status: The new ownership status (Owned or Unowned)
        """
        # Update the module's ownership variable if it exists
        if hasattr(module, 'ownership_var'):
            if hasattr(module.ownership_var, 'set'):
                module.ownership_var.set(ownership_status)
            else:
                module.ownership_var = ownership_status
            
        # Set the ownership status on the module itself for future reference
        if hasattr(module, 'owned_status'):
            # Convert string value to boolean for storage in the module
            is_owned = (ownership_status == "Owned")
            module.owned_status = is_owned
        elif hasattr(module, 'blueprint_owned'):
            # Convert string value to boolean for storage in the module
            is_owned = (ownership_status == "Owned")
            module.blueprint_owned = is_owned
        
        # Determine which category this module belongs to
        module_type = None
        module_name = None
        
        for category, modules in self.discovered_modules.items():
            for name, mod in modules.items():
                if mod == module:
                    module_type = category
                    module_name = name
                    break
            if module_type:
                break
                
        if module_type and module_name:
            # Convert from discovered module category to config category
            category = self.get_category_from_module_type(module_type)
            
            # Directly update the blueprint config
            if category not in self.blueprint_config:
                self.blueprint_config[category] = {}
            
            # Convert the ownership status to boolean for consistent storage
            is_owned = (ownership_status == "Owned")
            
            if module_name not in self.blueprint_config[category]:
                # Create a new entry if it doesn't exist
                self.blueprint_config[category][module_name] = {
                    'owned': is_owned,
                    'invented': False,
                    'me': 0,
                    'te': 0
                }
            else:
                # Update existing entry
                self.blueprint_config[category][module_name]['owned'] = is_owned
            
            # Save the configuration immediately
            from config.blueprint_config import save_blueprint_ownership
            save_blueprint_ownership(self.blueprint_config)
            
            self.status_var.set(f"Updated ownership for {getattr(module, 'display_name', 'unknown module')} to {ownership_status}")
        else:
            self.status_var.set(f"Could not determine module type for {getattr(module, 'display_name', 'unknown module')}")
    
    def update_cap_component_ownership(self, component_name, component_data, ownership_status):
        """Update ownership status for a capital component"""
        if 'capital_components' in self.discovered_modules and component_name in self.discovered_modules['capital_components']:
            # Update the ownership var
            component_data.ownership_var.set(ownership_status)
            
            # Convert to boolean for blueprint_owned attribute
            is_owned = (ownership_status == "owned")
            
            # Update the module attribute
            self.discovered_modules['capital_components'][component_name].blueprint_owned = is_owned
            
            # Ensure component_blueprints section exists
            if 'component_blueprints' not in self.blueprint_config:
                self.blueprint_config['component_blueprints'] = {}
            
            # Ensure component exists in config
            if component_name not in self.blueprint_config['component_blueprints']:
                self.blueprint_config['component_blueprints'][component_name] = {
                    'owned': is_owned,
                    'invented': False,  # Components cannot be invented
                    'me': 0,
                    'te': 0
                }
            else:
                # Update existing entry
                self.blueprint_config['component_blueprints'][component_name]['owned'] = is_owned
            
            # Save the configuration immediately to ensure it persists
            from config.blueprint_config import save_blueprint_ownership
            save_blueprint_ownership(self.blueprint_config)
            
            self.status_var.set(f"Updated ownership for {component_name} to {ownership_status}")
        else:
            self.status_var.set(f"Component {component_name} not found")
    
    def update_cap_component_invention(self, component_name, component_data):
        """Update invention status for a capital component"""
        if 'capital_components' in self.discovered_modules and component_name in self.discovered_modules['capital_components']:
            # Get the invented status - handle both boolean and BooleanVar
            if 'invented_var' in component_data:
                if isinstance(component_data['invented_var'], bool):
                    is_invented = component_data['invented_var']
                else:
                    # It's a tkinter BooleanVar
                    is_invented = component_data['invented_var'].get()
            else:
                # Default to False if not found
                is_invented = False
                
            # Update the invention status in the component data
            self.discovered_modules['capital_components'][component_name].is_invented = is_invented
            # Save to config
            update_blueprint_invention(self.blueprint_config, 'component_blueprints', component_name, is_invented)
            self.status_var.set(f"Updated invention status for {component_name} to {is_invented}")
        else:
            self.status_var.set(f"Component {component_name} not found")
    
    def initialize_capital_component_vars(self):
        """Initialize capital component variables"""
        if 'capital_components' in self.discovered_modules:
            for comp_name, comp_data in self.discovered_modules['capital_components'].items():
                # Get the blueprint ownership from config
                ownership = get_blueprint_ownership(self.blueprint_config, 'component_blueprints', comp_name)
                
                # Create ownership variable
                comp_data.ownership_var = tk.StringVar()
                
                # Convert to lowercase to match radio button values
                if ownership == "Owned":
                    comp_data.ownership_var.set("owned")
                    comp_data.blueprint_owned = True
                else:
                    comp_data.ownership_var.set("unowned")
                    comp_data.blueprint_owned = False
                
                # Create ME% variable
                comp_data.me_var = tk.StringVar()
                me_value = get_blueprint_me(self.blueprint_config, 'component_blueprints', comp_name)
                comp_data.me_var.set(str(me_value))
                
                # Create TE% variable
                comp_data.te_var = tk.StringVar()
                te_value = get_blueprint_te(self.blueprint_config, 'component_blueprints', comp_name)
                comp_data.te_var.set(str(te_value))
    
    def save_blueprint_config(self):
        """Save the blueprint configuration"""
        try:
            from config.blueprint_config import update_blueprint_ownership, update_blueprint_me, update_blueprint_te, save_blueprint_ownership, update_blueprint_invention
            
            # Save ownership status for all modules
            for category_name, modules in self.discovered_modules.items():
                category = self.get_category_from_module_type(category_name)
                
                # Skip empty categories
                if not category or not modules:
                    continue
                
                for module_name, module in modules.items():
                    # Special handling for capital components
                    if category_name == 'capital_components':
                        if hasattr(module, 'ownership_var'):
                            try:
                                ownership_status = module.ownership_var.get()
                                is_owned = (ownership_status == "owned")
                                
                                # Make sure the category exists
                                if 'component_blueprints' not in self.blueprint_config:
                                    self.blueprint_config['component_blueprints'] = {}
                                
                                # Create or update entry
                                if module_name not in self.blueprint_config['component_blueprints']:
                                    self.blueprint_config['component_blueprints'][module_name] = {
                                        'owned': is_owned,
                                        'invented': False,  # Components cannot be invented
                                        'me': 0,
                                        'te': 0
                                    }
                                else:
                                    # Update existing entry
                                    self.blueprint_config['component_blueprints'][module_name]['owned'] = is_owned
                                
                                # Update the module objects
                                module.blueprint_owned = is_owned
                                
                                # Save the configuration immediately
                                from config.blueprint_config import save_blueprint_ownership
                                save_blueprint_ownership(self.blueprint_config)
                            except Exception as e:
                                print(f"Error saving capital component {module_name}: {e}")
                    # Regular modules (ships, components, etc.)
                    elif hasattr(module, 'ownership_var'):
                        try:
                            # Get the ownership status as a string (Owned/Unowned)
                            ownership_status = "Owned" if module.ownership_var.get() == "owned" else "Unowned"
                            
                            # Convert to boolean for config
                            is_owned = (ownership_status == "Owned")
                            
                            # Make sure the category exists in config
                            if category not in self.blueprint_config:
                                self.blueprint_config[category] = {}
                            
                            # If the module doesn't exist in config, create it
                            if module_name not in self.blueprint_config[category]:
                                self.blueprint_config[category][module_name] = {
                                    'owned': is_owned,
                                    'invented': False,
                                    'me': 0,
                                    'te': 0
                                }
                            else:
                                self.blueprint_config[category][module_name]['owned'] = is_owned
                            
                            # Also update the module's owned_status/blueprint_owned attribute
                            if hasattr(module, 'owned_status'):
                                module.owned_status = is_owned
                            elif hasattr(module, 'blueprint_owned'):
                                module.blueprint_owned = is_owned
                        except Exception as e:
                            pass
            
            # Save ME% values for all modules including capital components
            for category_name, modules in self.discovered_modules.items():
                category = self.get_category_from_module_type(category_name)
                for module_name, module in modules.items():
                    if hasattr(module, 'me_var'):
                        try:
                            me_value = int(module.me_var.get())
                            # Ensure ME is not negative
                            if me_value < 0:
                                me_value = 0
                                module.me_var.set("0")
                            
                            # Special handling for capital components
                            if category_name == 'capital_components':
                                if 'component_blueprints' not in self.blueprint_config:
                                    self.blueprint_config['component_blueprints'] = {}
                                if module_name not in self.blueprint_config['component_blueprints']:
                                    self.blueprint_config['component_blueprints'][module_name] = {
                                        'owned': False,
                                        'invented': False,
                                        'me': me_value,
                                        'te': 0
                                    }
                                else:
                                    self.blueprint_config['component_blueprints'][module_name]['me'] = me_value
                            else:
                                # Update the ME in config
                                update_blueprint_me(self.blueprint_config, category, module_name, me_value)
                        except ValueError:
                            # Invalid ME value, set to 0
                            module.me_var.set("0")
                            if category_name == 'capital_components':
                                if 'component_blueprints' in self.blueprint_config and module_name in self.blueprint_config['component_blueprints']:
                                    self.blueprint_config['component_blueprints'][module_name]['me'] = 0
                            else:
                                update_blueprint_me(self.blueprint_config, category, module_name, 0)
            
            # Save TE% values for all modules including capital components
            for category_name, modules in self.discovered_modules.items():
                category = self.get_category_from_module_type(category_name)
                for module_name, module in modules.items():
                    if hasattr(module, 'te_var'):
                        try:
                            te_value = int(module.te_var.get())
                            # Ensure TE is not negative
                            if te_value < 0:
                                te_value = 0
                                module.te_var.set("0")
                            
                            # Special handling for capital components
                            if category_name == 'capital_components':
                                if 'component_blueprints' not in self.blueprint_config:
                                    self.blueprint_config['component_blueprints'] = {}
                                if module_name not in self.blueprint_config['component_blueprints']:
                                    self.blueprint_config['component_blueprints'][module_name] = {
                                        'owned': False,
                                        'invented': False,
                                        'me': 0,
                                        'te': te_value
                                    }
                                else:
                                    self.blueprint_config['component_blueprints'][module_name]['te'] = te_value
                            else:
                                # Update the TE in config
                                update_blueprint_te(self.blueprint_config, category, module_name, te_value)
                        except ValueError:
                            # Invalid TE value, set to 0
                            module.te_var.set("0")
                            if category_name == 'capital_components':
                                if 'component_blueprints' in self.blueprint_config and module_name in self.blueprint_config['component_blueprints']:
                                    self.blueprint_config['component_blueprints'][module_name]['te'] = 0
                            else:
                                update_blueprint_te(self.blueprint_config, category, module_name, 0)
            
            # Save the configuration
            success = save_blueprint_ownership(self.blueprint_config)
            
            if success:
                self.status_var.set("Blueprint configuration saved successfully")
                return True
            else:
                self.status_var.set("Error saving blueprint configuration")
                return False
                
        except Exception as e:
            self.status_var.set(f"Error saving blueprint configuration: {e}")
            return False
