#!/usr/bin/env python3
"""
EVE Online Production Calculator - Refactored Version
A tool for calculating resource requirements for manufacturing in EVE Online
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox

from module_registry import ModuleLoader
from calculator import RequirementsCalculator
from blueprint_config import load_blueprint_ownership, apply_blueprint_ownership
from gui import EveProductionCalculator

def load_ore_data():
    """
    Load ore data from ore.json
    
    Returns:
        dict: Dictionary of ore data
    """
    import json
    
    ore_data_path = os.path.join(os.path.dirname(__file__), 'data', 'ore.json')
    
    try:
        with open(ore_data_path, 'r') as f:
            ore_json = json.load(f)
            
        # Convert the structured JSON into a flat dictionary for compatibility with existing code
        flat_ore_data = {}
        for sec_level, ores in ore_json['ores'].items():
            for ore_key, ore_info in ores.items():
                flat_ore_data[ore_info['display_name']] = ore_info['yields']
                
        return flat_ore_data
        
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading ore data: {e}")
        # Fallback to the original ore_data if JSON loading fails
        try:
            import importlib.util
            old_ore_data_path = os.path.join(os.path.dirname(__file__), 'ore_data.py')
            spec = importlib.util.spec_from_file_location('ore_data', old_ore_data_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print("Falling back to original ore_data.py")
            return module.ore_data
        except Exception as e2:
            print(f"Fatal error, could not load ore data: {e2}")
            return {}

def main():
    """
    Main function to run the application
    """
    # Get base path for application
    base_path = os.path.dirname(__file__)
    
    # Load modules into registry
    module_loader = ModuleLoader(base_path)
    module_registry = module_loader.load_all()
    
    # Create calculator
    calculator = RequirementsCalculator(module_registry)
    
    # Load ore data
    ore_data = load_ore_data()
    
    # Load blueprint ownership data
    blueprint_config = load_blueprint_ownership()
    
    # Apply blueprint ownership to the appropriate modules
    apply_blueprint_ownership(blueprint_config, module_registry)
    
    # Set blueprint config in calculator
    calculator.set_blueprint_config(blueprint_config)
    
    # Create and run GUI
    app = EveProductionCalculator(
        ore_data=ore_data,
        registry=module_registry,
        calculator=calculator,
        blueprint_config=blueprint_config
    )
    
    # Start the main event loop
    app.mainloop()

if __name__ == "__main__":
    main()
