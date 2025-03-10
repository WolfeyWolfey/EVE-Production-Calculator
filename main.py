#!/usr/bin/env python3
"""
EVE Online Production Calculator - Refactored Version
A tool for calculating resource requirements for manufacturing in EVE Online
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox

from core.module_registry import ModuleRegistry
from core.data_loaders import load_ships, load_components, load_pi_data, load_ore_data
from core.calculator import RequirementsCalculator
from config.blueprint_config import load_blueprint_ownership, apply_blueprint_ownership
from gui.gui import EveProductionCalculator

def main():
    """
    Main function to run the application
    """
    # Get base path for application
    base_path = os.path.dirname(__file__)
    
    # Create module registry
    module_registry = ModuleRegistry()
    
    # Load data into registry
    load_ships(module_registry, base_path)
    load_components(module_registry, base_path)
    load_pi_data(module_registry, base_path)
    
    # Create calculator
    calculator = RequirementsCalculator(module_registry)
    
    # Load ore data
    ore_data = load_ore_data(base_path)
    
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
