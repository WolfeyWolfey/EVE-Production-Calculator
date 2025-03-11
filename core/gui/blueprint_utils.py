"""
Blueprint utility functions for EVE Production Calculator
Provides functions for blueprint ownership management and integration with the main application
"""

import tkinter as tk
from tkinter import messagebox
from core.gui.blueprints_gui import BlueprintManager

def open_blueprint_editor(app, registry, blueprint_config, callback=None):
    """
    Open the Blueprint Ownership Editor
    
    Args:
        app: The main application window
        registry: The module registry
        blueprint_config: The blueprint configuration
        callback: Optional callback function to call when the editor is closed
    
    Returns:
        bool: True if the editor was opened successfully
    """
    # Check if the ownership editor is already shown
    if getattr(app, 'ownership_editor_shown', False):
        messagebox.showinfo("Info", "Blueprint Ownership Editor is already open.")
        return False
        
    try:
        # Set the flag to prevent multiple windows
        app.ownership_editor_shown = True
        
        # Create a new top-level window
        blueprint_window = tk.Toplevel(app)
        blueprint_window.title("Blueprint Ownership Manager")
        
        # Prepare the modules dictionary for the blueprint manager
        discovered_modules = {
            'ships': registry.ships,
            'capital_ships': registry.capital_ships,
            'components': registry.components,
            'capital_components': registry.capital_components
        }
        
        # Create the blueprint manager
        blueprint_manager = BlueprintManager(
            blueprint_window, 
            discovered_modules,
            blueprint_config,
            registry
        )
        
        # Create the blueprint window UI
        blueprint_manager.create_blueprint_window(blueprint_window)
        
        # Configure window position
        window_width = 800
        window_height = 600
        
        # Center the window
        position_right = int(app.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(app.winfo_screenheight() / 2 - window_height / 2)
        
        # Set the window size and position
        blueprint_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
        
        # Make the editor modal
        blueprint_window.transient(app)
        blueprint_window.grab_set()
        blueprint_window.focus_set()
        
        # Configure the callback
        if callback:
            # Store the callback in the blueprint manager
            blueprint_manager.on_close_callback = callback
            
            # Configure the window to call the callback when closed
            def on_window_close():
                app.ownership_editor_shown = False
                if callback:
                    callback()
                blueprint_window.destroy()
                
            blueprint_window.protocol("WM_DELETE_WINDOW", on_window_close)
            
        # Wait for the window to be closed
        app.wait_window(blueprint_window)
        
        return True
        
    except Exception as e:
        app.ownership_editor_shown = False
        messagebox.showerror("Error", f"Failed to open Blueprint Ownership Editor: {str(e)}")
        return False

def reset_ship_ownership(registry, blueprint_config, refresh_callback=None):
    """
    Reset ownership status for all ships
    
    Args:
        registry: The module registry
        blueprint_config: The blueprint configuration
        refresh_callback: Optional callback to refresh the UI after reset
    
    Returns:
        bool: True if the reset was successful
    """
    # Confirm with the user
    if not messagebox.askyesno("Confirm Reset", 
                              "Are you sure you want to reset ownership status for ALL ships?\n\n"
                               "This action cannot be undone."):
        return False
    
    # Reset ownership for all ships
    for ship_name, ship in registry.ships.items():
        ship.owned_status = False
        
        # Update the blueprint config
        if ship_name in blueprint_config.get('ship_blueprints', {}):
            blueprint_config['ship_blueprints'][ship_name]['owned'] = False
        elif hasattr(ship, 'display_name') and ship.display_name in blueprint_config.get('ship_blueprints', {}):
            blueprint_config['ship_blueprints'][ship.display_name]['owned'] = False
    
    # Reset ownership for all capital ships
    for ship_name, ship in registry.capital_ships.items():
        ship.owned_status = False
        
        # Update the blueprint config
        if ship_name in blueprint_config.get('capital_ship_blueprints', {}):
            blueprint_config['capital_ship_blueprints'][ship_name]['owned'] = False
        elif hasattr(ship, 'display_name') and ship.display_name in blueprint_config.get('capital_ship_blueprints', {}):
            blueprint_config['capital_ship_blueprints'][ship.display_name]['owned'] = False
    
    # Save the changes
    try:
        from core.config.blueprint_config import save_blueprint_ownership
        
        # Run the save function
        success = save_blueprint_ownership(blueprint_config)
        
        if success:
            messagebox.showinfo("Success", "All ship ownership status has been reset.")
            
            # Call the refresh callback if provided
            if refresh_callback:
                refresh_callback()
                
            return True
        else:
            messagebox.showerror("Error", "Failed to save ownership changes.")
            return False
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save ownership changes: {str(e)}")
        return False

def apply_blueprint_changes(blueprint_config, registry):
    """
    Apply blueprint configuration changes to the registry
    
    Args:
        blueprint_config: The blueprint configuration
        registry: The module registry
    """
    try:
        from core.config.blueprint_config import save_blueprint_ownership, apply_blueprint_ownership
        
        # Save the ownership
        save_blueprint_ownership(blueprint_config)
        
        # Apply the updated ownership to the registry
        apply_blueprint_ownership(blueprint_config, registry)
        
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to apply blueprint changes: {str(e)}")
        return False
