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
    Load ore data from ore_data.py
    
    Returns:
        dict: Dictionary of ore data
    """
    import importlib.util
    
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
    
    # Create and run GUI
    app = EveProductionCalculator(
        ore_data=ore_data,
        registry=module_registry,
        calculator=calculator
    )
    
    # Start the main event loop
    app.mainloop()

if __name__ == "__main__":
    main()
