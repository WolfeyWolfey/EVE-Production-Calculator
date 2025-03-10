#!/usr/bin/env python3
"""
EVE Online Production Calculator
A tool for calculating resource requirements for manufacturing in EVE Online
"""

import os
import importlib.util
import tkinter as tk
from tkinter import ttk, messagebox
from gui import EveProductionCalculator
from blueprint_config import load_blueprint_ownership, apply_blueprint_ownership

def discover_modules(directory, module_type):
    """
    Discover and load modules from a directory
    
    Args:
        directory (str): Directory to search for modules
        module_type (str): Type of modules to load
        
    Returns:
        dict: Dictionary of loaded modules
    """
    modules = {}
    
    # Check if directory exists
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return modules
        
    # Get all Python files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            # Module name is the filename without extension
            module_name = filename[:-3]
            
            # Construct absolute path to the module
            module_path = os.path.join(directory, filename)
            
            # Create a module spec
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            
            # Create a module from the spec
            module = importlib.util.module_from_spec(spec)
            
            # Execute the module
            spec.loader.exec_module(module)
            
            # Check if module has a display_name attribute
            if hasattr(module, 'display_name'):
                # Add module to the dictionary
                modules[module_name] = module
                
                # Add the module type attribute
                module.module_type = module_type
                
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
    
    return modules

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
    discovered_modules = {
        'ships': discover_modules('Ships', 'ship'),
        'capital_ships': discover_modules('Capital Ships', 'capital_ship'),
        'components': discover_modules('Components', 'component')
    }
    
    # PI components are handled separately
    # Import PI data directly
    pi_data_path = os.path.join(os.path.dirname(__file__), 'planetary_data.py')
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
