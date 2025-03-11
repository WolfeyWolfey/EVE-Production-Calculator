"""
Settings configuration for EVE Production Calculator
"""
import os
import json
from core.utils.debug import debug_print

def get_default_settings():
    """
    Get default settings
    
    Returns:
        dict: Default settings dictionary
    """
    return {
        "theme": "light",  # Default theme is light mode
        "window_size": {
            "width": 900, 
            "height": 800
        }
    }

def load_settings(base_path=None):
    """
    Load settings from settings.json
    
    Args:
        base_path: Base path of the application (optional)
        
    Returns:
        dict: Settings dictionary
    """
    # Get the base path if not provided
    if base_path is None:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Path to settings file
    settings_path = os.path.join(base_path, 'core', 'config', 'settings.json')
    
    # Get default settings
    settings = get_default_settings()
    
    # If settings file exists, load and update defaults
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r') as f:
                user_settings = json.load(f)
            
            # Update default settings with user settings
            settings.update(user_settings)
            debug_print("Settings loaded from settings.json")
        except Exception as e:
            debug_print(f"Error loading settings: {e}")
    else:
        debug_print("No settings.json found, using defaults")
        # Save default settings
        save_settings(settings, base_path)
    
    return settings

def save_settings(settings, base_path=None):
    """
    Save settings to settings.json
    
    Args:
        settings: Settings dictionary to save
        base_path: Base path of the application (optional)
    """
    # Get the base path if not provided
    if base_path is None:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Path to settings file
    settings_path = os.path.join(base_path, 'core', 'config', 'settings.json')
    
    # Create config directory if it doesn't exist
    os.makedirs(os.path.dirname(settings_path), exist_ok=True)
    
    try:
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=4)
        debug_print("Settings saved to settings.json")
    except Exception as e:
        debug_print(f"Error saving settings: {e}")

def update_setting(key, value, base_path=None):
    """
    Update a single setting
    
    Args:
        key: Setting key to update
        value: New value for the setting
        base_path: Base path of the application (optional)
    """
    # Load current settings
    settings = load_settings(base_path)
    
    # Update the setting
    settings[key] = value
    
    # Save updated settings
    save_settings(settings, base_path)
    
    return settings
