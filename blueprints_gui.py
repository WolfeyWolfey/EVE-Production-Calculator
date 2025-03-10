"""
Blueprint management GUI components for EVE Production Calculator
This file contains the UI components and logic for blueprint management
"""

import tkinter as tk
from tkinter import ttk
from blueprint_config import (
    update_blueprint_ownership, get_blueprint_ownership, 
    update_blueprint_invention, save_blueprint_ownership,
    update_blueprint_me, get_blueprint_me
)
from tkinter import messagebox

class BlueprintManager:
    """
    Blueprint management class for handling blueprint ownership and invention status
    for EVE Online ships, capital ships, components, and capital components.
    """
    
    def __init__(self, parent, discovered_modules, blueprint_config):
        """
        Initialize the blueprint manager
        
        Args:
            parent: The parent tkinter application
            discovered_modules: Dictionary of discovered modules
            blueprint_config: Blueprint configuration
        """
        self.parent = parent
        self.discovered_modules = discovered_modules
        self.blueprint_config = blueprint_config
        
        # Initialize status variable
        if hasattr(parent, 'status_var'):
            self.status_var = parent.status_var
        else:
            self.status_var = tk.StringVar()
            self.status_var.set("Ready")
        
        # Initialize capital component variables
        self.initialize_capital_component_vars()
    
    def create_blueprint_management_tab(self, tab_frame):
        """Create the blueprint management tab"""
        # Create a notebook for blueprint management
        blueprint_notebook = ttk.Notebook(tab_frame)
        blueprint_notebook.pack(fill="both", expand=True)
        
        # Create tabs for each type of blueprint
        ships_tab = ttk.Frame(blueprint_notebook)
        capital_ships_tab = ttk.Frame(blueprint_notebook)
        components_tab = ttk.Frame(blueprint_notebook)
        capital_components_tab = ttk.Frame(blueprint_notebook)
        
        # Add tabs to notebook
        blueprint_notebook.add(ships_tab, text="Ships")
        blueprint_notebook.add(capital_ships_tab, text="Capital Ships")
        blueprint_notebook.add(components_tab, text="Components")
        blueprint_notebook.add(capital_components_tab, text="Capital Components")
        
        # Create content for each tab
        self.create_ships_blueprint_tab(ships_tab)
        self.create_capital_ships_blueprint_tab(capital_ships_tab)
        self.create_components_blueprint_tab(components_tab)
        self.create_capital_components_blueprint_tab(capital_components_tab)
        
        # Create save frame at the bottom
        save_frame = ttk.Frame(tab_frame)
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
        """Create the components blueprint tab"""
        if 'components' in self.discovered_modules:
            # Frame for component blueprint management
            component_frame = ttk.LabelFrame(parent_tab, text="Component Blueprints")
            component_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create grid view for components
            self.create_component_blueprint_grid(component_frame)
        else:
            ttk.Label(parent_tab, text="No component modules discovered").pack(padx=10, pady=10)
    
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
            self.create_blueprint_grid(parent, "Components", self.discovered_modules['components'])
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
        ttk.Label(grid_frame, text="Invented", font=("Arial", 10, "bold")).grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(grid_frame, text="ME%", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5, pady=5)
        
        # Add separator
        separator = ttk.Separator(grid_frame, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=5, sticky="ew", pady=5)
        
        # Populate grid with capital component blueprints
        row = 2
        if 'capital_components' in self.discovered_modules:
            for comp_name, comp_data in self.discovered_modules['capital_components'].items():
                # Initialize ownership_var if it doesn't exist
                if 'ownership_var' not in comp_data:
                    # Check if blueprint_owned exists
                    blueprint_status = comp_data.get('blueprint_owned', 'Unowned')
                    comp_data['ownership_var'] = tk.StringVar(value=blueprint_status)
                
                # Initialize invented_var if it doesn't exist
                if 'invented_var' not in comp_data:
                    comp_data['invented_var'] = tk.BooleanVar()
                    # Default to False (not invented)
                    comp_data['invented_var'].set(False)
                
                # Add component name and radio buttons
                ttk.Label(grid_frame, text=comp_data.get('display_name', comp_name)).grid(row=row, column=0, padx=5, pady=2, sticky="w")
                ttk.Radiobutton(grid_frame, variable=comp_data['ownership_var'], value="Unowned", 
                               command=lambda n=comp_name, d=comp_data: self.update_cap_component_ownership(n, d, "Unowned")).grid(row=row, column=1, padx=5, pady=2)
                ttk.Radiobutton(grid_frame, variable=comp_data['ownership_var'], value="Owned", 
                               command=lambda n=comp_name, d=comp_data: self.update_cap_component_ownership(n, d, "Owned")).grid(row=row, column=2, padx=5, pady=2)
                ttk.Checkbutton(grid_frame, variable=comp_data['invented_var'], 
                               command=lambda n=comp_name, d=comp_data: self.update_cap_component_invention(n, d)).grid(row=row, column=3, padx=5, pady=2)
                
                # ME% input field
                me_var = tk.StringVar()
                me_value = get_blueprint_me(self.blueprint_config, 'capital_components', comp_name)
                me_var.set(str(me_value))
                me_entry = ttk.Entry(grid_frame, width=4, textvariable=me_var)
                me_entry.grid(row=row, column=4, padx=5, pady=2)
                me_entry.bind("<FocusOut>", lambda event, n=comp_name, d=comp_data: self.validate_capital_component_me(n, d))
                
                row += 1
        
        # Configure the canvas to adjust scrolling based on the grid size
        grid_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    
    def create_blueprint_grid(self, parent, modules_type, modules_dict):
        """Create a grid view for blueprint management"""
        # Container with scrollbar
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, padx=10, pady=5)
        
        # Add canvas and scrollbar
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create frame for grid
        grid_frame = ttk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=grid_frame, anchor="nw")
        
        # Add headers
        ttk.Label(grid_frame, text=f"{modules_type} Blueprint", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(grid_frame, text="Unowned", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(grid_frame, text="Owned", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(grid_frame, text="Invented", font=("Arial", 10, "bold")).grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(grid_frame, text="ME%", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5, pady=5)
        
        # Separator
        separator = ttk.Separator(grid_frame, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=5, sticky="ew", padx=5, pady=2)
        
        row = 2
        for module_name, module in modules_dict.items():
            display_name = getattr(module, 'display_name', module_name)
            
            # Skip if the module has already been processed
            if hasattr(module, 'ownership_var'):
                current_status = module.ownership_var.get() if hasattr(module.ownership_var, 'get') else module.ownership_var
            else:
                # Get current ownership status
                if hasattr(module, 'owned_status'):
                    current_status = module.owned_status
                elif hasattr(module, 'blueprint_owned'):
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
            
            # Store these variables in the module for later reference
            module.ownership_var = ownership_var
            module.invented_var = tk.BooleanVar()
            module.invented_var.set(current_status == "Invented")
            module.me_var = me_var  # Store ME% variable
            
            # Radio buttons for Unowned/Owned
            ttk.Radiobutton(grid_frame, variable=ownership_var, value="Unowned",
                           command=lambda m=module: self.update_module_ownership(m, "Unowned")).grid(row=row, column=1, padx=5, pady=2)
            ttk.Radiobutton(grid_frame, variable=ownership_var, value="Owned", 
                           command=lambda m=module: self.update_module_ownership(m, "Owned")).grid(row=row, column=2, padx=5, pady=2)
            
            # Checkbox for Invented status
            ttk.Checkbutton(grid_frame, variable=module.invented_var, 
                           command=lambda m=module: self.update_invented_status(m)).grid(row=row, column=3, padx=5, pady=2)
            
            # ME% input field
            me_entry = ttk.Entry(grid_frame, width=4, textvariable=module.me_var)
            me_entry.grid(row=row, column=4, padx=5, pady=2)
            me_entry.bind("<FocusOut>", lambda event, m=module: self.validate_me_entry(m))
            
            # Module name
            ttk.Label(grid_frame, text=display_name).grid(row=row, column=0, padx=5, pady=2, sticky="w")
            
            row += 1
        
        # Update scrollregion to accommodate all widgets
        grid_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        # Add canvas resize binding
        def _configure_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.bind('<Configure>', _configure_canvas)
    
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
            'Capital Components': 'capital_components'
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
            
        except ValueError:
            # Reset to 0 if invalid
            module.me_var.set("0")
    
    def validate_capital_component_me(self, comp_name, comp_data):
        """
        Validate ME% entry for capital components
        
        Args:
            comp_name: Name of the capital component
            comp_data: Component data dictionary
        """
        try:
            # Get ME% value
            me_value = int(comp_data['me_var'].get())
            
            # Validate ME% (0-10 is typical range in EVE)
            if me_value < 0:
                me_value = 0
            elif me_value > 10:
                me_value = 10
                
            # Set validated value
            comp_data['me_var'].set(str(me_value))
            
            # Update blueprint config
            update_blueprint_me(self.blueprint_config, 'capital_components', comp_name, me_value)
            
        except ValueError:
            # Reset to 0 if invalid
            comp_data['me_var'].set("0")
    
    def create_blueprint_window(self, blueprint_window):
        """Create the blueprint management window interface"""
        # Create notebook for tabs
        blueprint_notebook = ttk.Notebook(blueprint_window)
        blueprint_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs for each type of blueprint
        ships_tab = ttk.Frame(blueprint_notebook)
        capital_ships_tab = ttk.Frame(blueprint_notebook)
        components_tab = ttk.Frame(blueprint_notebook)
        capital_components_tab = ttk.Frame(blueprint_notebook)
        
        # Add tabs to notebook
        blueprint_notebook.add(ships_tab, text="Ships")
        blueprint_notebook.add(capital_ships_tab, text="Capital Ships")
        blueprint_notebook.add(components_tab, text="Components")
        blueprint_notebook.add(capital_components_tab, text="Capital Components")
        
        # Create content for each tab
        self.create_ship_blueprint_grid(ships_tab)
        self.create_capital_ship_blueprint_grid(capital_ships_tab)
        self.create_component_blueprint_grid(components_tab)
        self.create_capital_component_blueprint_grid(capital_components_tab)
        
        # Add Save All button at the bottom
        save_button = ttk.Button(blueprint_window, text="Save All", command=self.save_all_blueprint_ownership)
        save_button.pack(pady=10)
        
        # Add Close button
        close_button = ttk.Button(blueprint_window, text="Close", command=blueprint_window.destroy)
        close_button.pack(pady=5)
        
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
                        
                        # Save to config
                        update_blueprint_ownership(self.blueprint_config, 'capital_components', comp_name, ownership_status)
            
            # Save ME%
            for category, modules in self.discovered_modules.items():
                for module_name, module in modules.items():
                    if hasattr(module, 'me_var'):
                        me_value = int(module.me_var.get())
                        update_blueprint_me(self.blueprint_config, category, module_name, me_value)
            
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
        """Update ownership status for a module and save it"""
        module_type = None
        module_name = None
        
        # Determine module type from where it's found in discovered_modules
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
            # Update ownership in the module based on which attribute it has
            if hasattr(module, 'blueprint_owned'):
                module.blueprint_owned = ownership_status
            elif hasattr(module, 'owned_status'):
                module.owned_status = ownership_status
            else:
                # Add the attribute if it doesn't exist
                module.owned_status = ownership_status
            
            # Set the ownership_var
            if hasattr(module, 'ownership_var'):
                if isinstance(module.ownership_var, tk.StringVar):
                    module.ownership_var.set(ownership_status)
                else:
                    module.ownership_var = ownership_status
                
            # Save to config
            update_blueprint_ownership(self.blueprint_config, module_type, module_name, ownership_status)
            self.status_var.set(f"Updated ownership for {getattr(module, 'display_name', 'unknown module')} to {ownership_status}")
        else:
            self.status_var.set(f"Could not determine module type for {getattr(module, 'display_name', 'unknown module')}")
    
    def update_cap_component_ownership(self, component_name, component_data, ownership_status):
        """Update ownership status for a capital component"""
        if 'capital_components' in self.discovered_modules and component_name in self.discovered_modules['capital_components']:
            # Update the ownership var and the module attribute
            component_data['ownership_var'].set(ownership_status)
            self.discovered_modules['capital_components'][component_name]['blueprint_owned'] = ownership_status
            # Save to config
            update_blueprint_ownership(self.blueprint_config, 'capital_components', component_name, ownership_status)
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
            self.discovered_modules['capital_components'][component_name]['is_invented'] = is_invented
            # Save to config
            update_blueprint_invention(self.blueprint_config, 'capital_components', component_name, is_invented)
            self.status_var.set(f"Updated invention status for {component_name} to {is_invented}")
        else:
            self.status_var.set(f"Component {component_name} not found")
    
    def initialize_capital_component_vars(self):
        """Initialize capital component variables"""
        if 'capital_components' in self.discovered_modules:
            for comp_name, comp_data in self.discovered_modules['capital_components'].items():
                # Create ownership variable
                comp_data['ownership_var'] = tk.StringVar()
                if 'blueprint_owned' in comp_data:
                    comp_data['ownership_var'].set(comp_data['blueprint_owned'])
                else:
                    comp_data['ownership_var'].set("Unowned")
                    comp_data['blueprint_owned'] = "Unowned"
                
                # Create invented variable
                comp_data['invented_var'] = tk.BooleanVar()
                if 'is_invented' in comp_data:
                    comp_data['invented_var'].set(comp_data['is_invented'])
                else:
                    comp_data['invented_var'].set(False)
                    comp_data['is_invented'] = False
                
                # Create ME% variable
                comp_data['me_var'] = tk.StringVar()
                me_value = get_blueprint_me(self.blueprint_config, 'capital_components', comp_name)
                comp_data['me_var'].set(str(me_value))
    
    def save_blueprint_config(self):
        """Save the blueprint configuration"""
        from blueprint_config import save_blueprint_ownership
        
        # Save ME% values for all modules
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
                        # Update the ME in config
                        update_blueprint_me(self.blueprint_config, category, module_name, me_value)
                    except ValueError:
                        # Invalid ME value, set to 0
                        module.me_var.set("0")
                        update_blueprint_me(self.blueprint_config, category, module_name, 0)
        
        # Save the configuration
        success = save_blueprint_ownership(self.blueprint_config)
        
        if success:
            self.status_var.set("Blueprint configuration saved successfully")
        else:
            self.status_var.set("Error saving blueprint configuration")
            
        return success
