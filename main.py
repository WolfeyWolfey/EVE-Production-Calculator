#!/usr/bin/env python3
"""
EVE Online Production Calculator
A tool for calculating resource requirements for manufacturing in EVE Online
"""

import os
import importlib
import importlib.util
import tkinter as tk
from tkinter import ttk, messagebox
from gui import EveProductionCalculator
from blueprint_config import load_blueprint_ownership, apply_blueprint_ownership

class ShipModule:
    def __init__(self, name, display_name, requirements, details, faction=None, ship_type=None, owned_status=None):
        self.name = name
        self.display_name = display_name
        self.requirements = requirements
        self.details = details
        self.faction = faction
        self.ship_type = ship_type
        self.owned_status = owned_status

def discover_modules(base_path):
    """Discover all available modules in the codebase"""
    discovered_modules = {
        'ships': {},
        'capital_ships': {},
        'components': {},
        'pi_data': {}
    }
    
    # Recursively find all ship data files
    ship_data_files = []
    for root, dirs, files in os.walk(os.path.join(base_path, "Ships")):
        # Skip the Capital Ships folder since we handle it separately
        if "Capital Ships" in root:
            continue
        for file in files:
            if file.endswith("_data.py"):
                ship_data_files.append(os.path.join(root, file))
    
    # Process ship data files
    for ship_file in ship_data_files:
        try:
            # Convert path to module name
            rel_path = os.path.relpath(ship_file, base_path)
            module_name = os.path.splitext(rel_path)[0].replace(os.path.sep, ".")
            
            # Import module
            ship_module = importlib.import_module(module_name)
            
            # Get module name
            module_var_name = os.path.basename(ship_file).replace("_data.py", "")
            
            # Get requirements
            requirements_var = f"{module_var_name}_requirements"
            if hasattr(ship_module, requirements_var):
                requirements = getattr(ship_module, requirements_var)
            else:
                requirements = {}
                
            # Create ShipModule
            if hasattr(ship_module, "details"):
                ship = ShipModule(
                    name=module_var_name,
                    display_name=getattr(ship_module, "display_name", module_var_name),
                    requirements=requirements,
                    details=getattr(ship_module, "details", ""),
                )
                
                # Add faction and ship_type if they exist
                if hasattr(ship_module, "faction"):
                    ship.faction = ship_module.faction
                if hasattr(ship_module, "ship_type"):
                    ship.ship_type = ship_module.ship_type
                    
                # Add ownership status if it exists
                if hasattr(ship_module, "owned_status"):
                    ship.owned_status = ship_module.owned_status
                
                discovered_modules['ships'][module_var_name] = ship
        except Exception as e:
            print(f"Error loading ship module {ship_file}: {e}")
    
    # Discover capital ships
    capital_ships = {}
    for filename in os.listdir(os.path.join(base_path, "Capital Ships")):
        if filename.endswith('.py'):
            # Module name is the filename without extension
            module_name = filename[:-3]
            
            # Construct absolute path to the module
            module_path = os.path.join(base_path, "Capital Ships", filename)
            
            # Create a module spec
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            
            # Create a module from the spec
            module = importlib.util.module_from_spec(spec)
            
            # Execute the module
            spec.loader.exec_module(module)
            
            # Check if module has a display_name attribute
            if hasattr(module, 'display_name'):
                # Add module to the dictionary
                capital_ships[module_name] = module
                
                # Add the module type attribute
                module.module_type = 'capital_ship'
                
                # Add owned_status attribute if it doesn't exist
                if not hasattr(module, 'owned_status'):
                    module.owned_status = "Unowned"
                    
                # Initialize blueprint_owned fields for capital components
                if hasattr(module, 'capital_component_data'):
                    for component_name, component_data in module.capital_component_data.items():
                        if 'blueprint_owned' not in component_data:
                            component_data['blueprint_owned'] = "Unowned"
            else:
                print(f"Module {module_name} doesn't have display_name")
    
    discovered_modules['capital_ships'] = capital_ships
    
    # Discover components
    components = {}
    for filename in os.listdir(os.path.join(base_path, "Components")):
        if filename.endswith('.py'):
            # Module name is the filename without extension
            module_name = filename[:-3]
            
            # Construct absolute path to the module
            module_path = os.path.join(base_path, "Components", filename)
            
            # Create a module spec
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            
            # Create a module from the spec
            module = importlib.util.module_from_spec(spec)
            
            # Execute the module
            spec.loader.exec_module(module)
            
            # Check if module has a display_name attribute
            if hasattr(module, 'display_name'):
                # Add module to the dictionary
                components[module_name] = module
                
                # Add the module type attribute
                module.module_type = 'component'
                
                # Add owned_status attribute if it doesn't exist
                if not hasattr(module, 'owned_status'):
                    module.owned_status = "Unowned"
            else:
                print(f"Module {module_name} doesn't have display_name")
    
    discovered_modules['components'] = components
    
    # PI components are handled separately
    # Import PI data directly
    pi_data_path = os.path.join(base_path, 'planetary_data.py')
    if os.path.exists(pi_data_path):
        pi_spec = importlib.util.spec_from_file_location('planetary_data', pi_data_path)
        pi_module = importlib.util.module_from_spec(pi_spec)
        pi_spec.loader.exec_module(pi_module)
        
        # Add PI data to discovered modules
        discovered_modules['pi_data'] = {
            'p0_materials': getattr(pi_module, 'p0_materials', {}),
            'p1_materials': getattr(pi_module, 'p1_materials', {}),
            'p2_materials': getattr(pi_module, 'p2_materials', {}),
            'p3_materials': getattr(pi_module, 'p3_materials', {}),
            'p4_materials': getattr(pi_module, 'p4_materials', {})
        }
    
    return discovered_modules

def load_ore_data():
    """
    Load ore data from ore_data.py
    
    Returns:
        dict: Dictionary of ore data
    """
    ore_data_path = os.path.join(os.path.dirname(__file__), 'ore_data.py')
    
    # Create a module spec
    spec = importlib.util.spec_from_file_location('ore_data', ore_data_path)
    
    # Create a module from the spec
    module = importlib.util.module_from_spec(spec)
    
    # Execute the module
    spec.loader.exec_module(module)
    
    # Return the ore_data dictionary
    return module.ore_data

def main():
    """
    Main function to run the application
    """
    # Discover modules
    discovered_modules = discover_modules(os.path.dirname(__file__))
    
    # Load ore data
    ore_data = load_ore_data()
    
    # Load blueprint ownership configuration
    blueprint_config = load_blueprint_ownership()
    
    # Apply blueprint ownership settings to modules
    apply_blueprint_ownership(discovered_modules, blueprint_config)
    
    # Create the GUI
    root = EveProductionCalculator(ore_data, discovered_modules, blueprint_config)
    
    # Run the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
