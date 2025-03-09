#!/usr/bin/env python3
"""
EVE Online Production Calculator
A tool for calculating resource requirements for manufacturing in EVE Online
"""

import os
import importlib.util
import tkinter as tk
from tkinter import ttk, messagebox

# Import data from separate modules
from ore_data import ore_data, ore_security_levels
from planetary_data import p0_materials, p1_materials, p2_materials, p3_materials, p4_materials

# Import GUI
from gui import EveProductionCalculator

def discover_ships_and_components():
    """Dynamically discover ship and component data modules in the project folders"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Dictionary to store discovered modules
    discovered = {
        'ships': {},
        'capital_ships': {},
        'components': {}
    }
    
    # Check Ships directory
    ships_dir = os.path.join(base_dir, 'Ships')
    if os.path.exists(ships_dir) and os.path.isdir(ships_dir):
        for file in os.listdir(ships_dir):
            if file.endswith('_data.py'):
                module_name = file.replace('_data.py', '')
                module_path = os.path.join(ships_dir, file)
                module = import_module_from_file(module_path, module_name)
                discovered['ships'][module.display_name] = module
    
    # Check Capital Ships directory
    capital_ships_dir = os.path.join(base_dir, 'Capital Ships')
    if os.path.exists(capital_ships_dir) and os.path.isdir(capital_ships_dir):
        for file in os.listdir(capital_ships_dir):
            if file.endswith('_data.py'):
                module_name = file.replace('_data.py', '')
                module_path = os.path.join(capital_ships_dir, file)
                module = import_module_from_file(module_path, module_name)
                discovered['capital_ships'][module.display_name] = module
    
    # Check Components directory
    components_dir = os.path.join(base_dir, 'Components')
    if os.path.exists(components_dir) and os.path.isdir(components_dir):
        for file in os.listdir(components_dir):
            if file.endswith('_data.py'):
                module_name = file.replace('_data.py', '')
                module_path = os.path.join(components_dir, file)
                module = import_module_from_file(module_path, module_name)
                discovered['components'][module.display_name] = module
    
    return discovered

def import_module_from_file(file_path, module_name):
    """Import a module from file path"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    """Main entry point for the application"""
    try:
        # Discover ships and components data modules
        discovered_modules = discover_ships_and_components()
        
        # Create the application
        app = EveProductionCalculator(
            ore_data=ore_data,
            discovered_modules=discovered_modules
        )
        
        # Set icon and other properties if needed
        # app.iconbitmap('path/to/icon.ico')
        
        # Run the application
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        raise  # Re-raise for debugging

if __name__ == "__main__":
    main()
