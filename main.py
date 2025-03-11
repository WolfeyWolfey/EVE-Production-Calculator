#!/usr/bin/env python3
"""
EVE Online Production Calculator - Refactored Version
A tool for calculating resource requirements for manufacturing in EVE Online
"""

import os
import sys
import argparse
import tkinter as tk
from tkinter import ttk, messagebox

from core.module_registry import ModuleRegistry
from core.data_loaders import load_ships, load_components, load_pi_data, load_ore_data
from core.calculator import RequirementsCalculator
from core.config.blueprint_config import load_blueprint_ownership, apply_blueprint_ownership
from core.gui.gui import EveProductionCalculator
from core.utils.debug import set_debug_mode, debug_print

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="EVE Online Production Calculator")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    return parser.parse_args()

def main():
    """
    Main function to run the application
    """
    # Parse command line arguments
    args = parse_arguments()
    
    # Set debug mode if --debug flag is present
    set_debug_mode(args.debug)
    
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
    load_ore_data(module_registry, base_path)
    
    # Load blueprint ownership data
    blueprint_config = load_blueprint_ownership()
    debug_print(f"Blueprint configuration loaded. Categories: {', '.join(blueprint_config.keys())}")
    
    # Apply blueprint ownership configuration
    debug_print("Applying blueprint ownership to registry...")
    apply_blueprint_ownership(blueprint_config, module_registry)
    
    # Check if any ships are owned
    owned_ships = [ship.name for ship in module_registry.get_all_ships() if ship.owned_status]
    if owned_ships:
        debug_print(f"After applying ownership, found {len(owned_ships)} owned ships: {', '.join(owned_ships)}")
    else:
        debug_print("WARNING: No owned ships found after applying ownership")
    
    # Set blueprint config in calculator
    calculator.set_blueprint_config(blueprint_config)
    
    # Create and run GUI
    app = EveProductionCalculator(
        registry=module_registry,
        calculator=calculator,
        blueprint_config=blueprint_config
    )
    
    # Start the main event loop
    app.mainloop()

if __name__ == "__main__":
    main()
