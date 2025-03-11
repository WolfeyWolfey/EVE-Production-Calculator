"""
Blueprint configuration manager for EVE Production Calculator
Handles saving and loading blueprint ownership status
"""

import os
import json
from collections import defaultdict
from core.utils.debug import debug_print

# Constants
CONFIG_FILENAME = "blueprint_ownership.json"
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'core', 'data', CONFIG_FILENAME)

def create_default_blueprint_config():
    """
    Create default blueprint configuration structure
    """
    return {
        'ship_blueprints': {},
        'capital_ship_blueprints': {},
        'components': {},
        'component_blueprints': {}  # For individual capital component blueprints
    }

def load_blueprint_ownership():
    """
    Load blueprint ownership configuration from file
    """
    try:
        # Check if file exists
        if os.path.exists(CONFIG_FILE):
            debug_print("Loading blueprint ownership from file...")
            # Read from existing file
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    debug_print(f"Loaded configuration from {CONFIG_FILE}")
                    
                    # Verify if any ships are set to owned
                    owned_ships = []
                    for ship_name, ship_data in config.get('ship_blueprints', {}).items():
                        if ship_data.get('owned', False):
                            owned_ships.append(ship_name)
                    
                    if owned_ships:
                        debug_print(f"Found {len(owned_ships)} owned ships in configuration: {', '.join(owned_ships)}")
                    else:
                        debug_print("No owned ships found in loaded configuration")
                    
                    return migrate_blueprint_config(config)
            except Exception as e:
                debug_print(f"Error loading blueprint configuration: {e}")
                return create_default_blueprint_config()
        else:
            debug_print(f"Configuration file not found at {CONFIG_FILE}, creating default config")
            config = create_default_blueprint_config()
            save_blueprint_ownership(config)
            return config
    except Exception as e:
        debug_print(f"Error in load_blueprint_ownership: {e}")
        return create_default_blueprint_config()

def save_blueprint_ownership(config):
    """
    Save blueprint ownership configuration to file
    
    Args:
        config: The blueprint configuration dictionary to save
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure the configuration directory exists
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        
        # First, try to read the existing config to merge with new changes
        existing_config = {}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as existing_file:
                    existing_config = json.load(existing_file)
            except Exception as e:
                debug_print(f"Could not read existing config file (will create new): {e}")
                
        # Carefully merge configs to preserve ownership settings
        # For each category in the new config
        for category, category_data in config.items():
            if category not in existing_config:
                existing_config[category] = {}
                
            # For each item in this category
            for item_name, item_data in category_data.items():
                # Only update this item if it doesn't exist or has changed
                if item_name not in existing_config[category]:
                    existing_config[category][item_name] = item_data
                else:
                    # Update only if different, preserving existing values
                    # especially ownership status
                    for key, value in item_data.items():
                        existing_config[category][item_name][key] = value
        
        # Save the merged configuration
        debug_print(f"Attempting to save blueprint configuration...")
        with open(CONFIG_FILE, 'w') as f:
            json.dump(existing_config, f, indent=4)
        debug_print(f"Blueprint configuration saved successfully to: {CONFIG_FILE}")
        return True
    except Exception as e:
        debug_print(f"Error saving blueprint configuration: {e}")
        return False

def update_blueprint_attribute(config, category, blueprint_name, attribute, value):
    """
    Update an attribute for a specific blueprint
    
    Args:
        config: The blueprint configuration dictionary
        category: Category of the blueprint (ship_blueprints, capital_ship_blueprints, components)
        blueprint_name: Name of the blueprint
        attribute: The attribute to update ('owned', 'invented', 'me', or 'te')
        value: New value for the attribute
    """
    # Make sure the category exists in config
    if category not in config:
        config[category] = {}
    
    # If blueprint doesn't exist in config, create it with defaults
    if blueprint_name not in config[category]:
        config[category][blueprint_name] = {
            'owned': False,
            'invented': False,
            'me': 0,  # Default ME% is 0
            'te': 0   # Default TE% is 0
        }
    
    # Handle special case for 'owned' which takes a string but stores a boolean
    if attribute == 'owned':
        config[category][blueprint_name][attribute] = (value == 'Owned')
    else:
        config[category][blueprint_name][attribute] = value
    
    # Save the updated config
    success = save_blueprint_ownership(config)
    debug_print("Configuration " + ("saved successfully." if success else "failed to save."))
    
    return config

def update_blueprint_ownership(config, category, blueprint_name, ownership_status):
    """
    Update ownership status for a specific blueprint
    
    Args:
        config: The blueprint configuration dictionary
        category: Category of the blueprint (ship_blueprints, capital_ship_blueprints, components)
        blueprint_name: Name of the blueprint
        ownership_status: New ownership status (Owned or Unowned)
    """
    return update_blueprint_attribute(config, category, blueprint_name, 'owned', ownership_status)

def update_blueprint_invention(config, category, blueprint_name, is_invented):
    """
    Update invention status for a specific blueprint
    
    Args:
        config: The blueprint configuration dictionary
        category: Category of the blueprint (ship_blueprints, capital_ship_blueprints, components)
        blueprint_name: Name of the blueprint
        is_invented: Boolean indicating whether the blueprint is invented
    """
    return update_blueprint_attribute(config, category, blueprint_name, 'invented', is_invented)

def update_blueprint_me(config, category, blueprint_name, me_value):
    """
    Update material efficiency for a specific blueprint
    
    Args:
        config: The blueprint configuration dictionary
        category: Category of the blueprint (ship_blueprints, capital_ship_blueprints, components)
        blueprint_name: Name of the blueprint
        me_value: Material Efficiency percentage (0-10)
    """
    # Validate ME value
    me_value = max(0, min(10, int(me_value)))
    return update_blueprint_attribute(config, category, blueprint_name, 'me', me_value)

def update_blueprint_te(config, category, blueprint_name, te_value):
    """
    Update time efficiency for a specific blueprint
    
    Args:
        config: The blueprint configuration dictionary
        category: Category of the blueprint (ship_blueprints, capital_ship_blueprints, components)
        blueprint_name: Name of the blueprint
        te_value: Time Efficiency percentage (0-20)
    """
    # Validate TE value
    te_value = max(0, min(20, int(te_value)))
    return update_blueprint_attribute(config, category, blueprint_name, 'te', te_value)

def get_blueprint_attribute(config, category, blueprint_name, attribute, default_value=None):
    """
    Get a specific blueprint attribute from configuration
    
    Args:
        config: Blueprint configuration dictionary
        category: Category of blueprint (ship_blueprints, capital_ship_blueprints, components)
        blueprint_name: Name of the blueprint
        attribute: Name of the attribute to retrieve
        default_value: Default value if attribute not found
        
    Returns:
        Attribute value or default value if not found
    """
    try:
        if category not in config or blueprint_name not in config[category]:
            return default_value
            
        bp_data = config[category][blueprint_name]
        
        if isinstance(bp_data, dict) and attribute in bp_data:
            return bp_data[attribute]
        return default_value
    except Exception as e:
        debug_print(f"Error getting {attribute} for {blueprint_name}: {e}")
        return default_value

def get_blueprint_ownership(config, category, blueprint_name):
    """
    Get ownership status for a specific blueprint
    
    Args:
        config: The blueprint configuration dictionary
        category: Category of the blueprint (ship_blueprints, capital_ship_blueprints, components)
        blueprint_name: Name of the blueprint
        
    Returns:
        String 'Owned' or 'Unowned'
    """
    owned = get_blueprint_attribute(config, category, blueprint_name, 'owned', False)
    return "Owned" if owned else "Unowned"

def get_blueprint_me(config, category, blueprint_name):
    """
    Get material efficiency value for a blueprint
    
    Args:
        config: Blueprint configuration dictionary
        category: Category of blueprint (ship_blueprints, capital_ship_blueprints, components)
        blueprint_name: Name of the blueprint
        
    Returns:
        Material Efficiency level (default: 0)
    """
    return get_blueprint_attribute(config, category, blueprint_name, 'me', 0)

def get_blueprint_te(config, category, blueprint_name):
    """
    Get time efficiency value for a blueprint
    
    Args:
        config: Blueprint configuration dictionary
        category: Category of blueprint (ship_blueprints, capital_ship_blueprints, components)
        blueprint_name: Name of the blueprint
        
    Returns:
        Time Efficiency level (default: 0)
    """
    return get_blueprint_attribute(config, category, blueprint_name, 'te', 0)

def apply_blueprint_ownership(config, registry):
    """
    Apply blueprint ownership settings from configuration to the registry
    
    Args:
        config: The blueprint configuration dictionary
        registry: The ModuleRegistry instance
    """
    debug_print("Applying blueprint ownership settings to registry...")
    
    if not config:
        debug_print("No blueprint configuration provided, skipping ownership application")
        return
    
    owned_counts = {'ships': 0, 'capital_ships': 0}
    
    # Map config categories to registry attributes and status attribute names
    mappings = [
        ('ship_blueprints', 'ships', 'owned_status'),
        ('capital_ship_blueprints', 'capital_ships', 'owned_status'),
        ('components', 'components', 'owned_status'),
        ('component_blueprints', 'capital_components', 'blueprint_owned')
    ]
    
    # Apply ownership status for each category
    for config_category, registry_attr, status_attr in mappings:
        if config_category in config and hasattr(registry, registry_attr):
            registry_dict = getattr(registry, registry_attr)
            debug_print(f"Processing {len(config[config_category])} items in {config_category}")
            
            for item_name, item_data in config[config_category].items():
                if item_name in registry_dict:
                    owned_value = item_data.get('owned', False)
                    setattr(registry_dict[item_name], status_attr, owned_value)
                    
                    # Count owned ships for reporting
                    if owned_value and registry_attr in ['ships', 'capital_ships']:
                        owned_counts[registry_attr] += 1
                        debug_print(f"Setting {registry_attr[:-1]} {item_name} ownership to: True")
                    elif registry_attr in ['ships', 'capital_ships']:
                        debug_print(f"{registry_attr[:-1].capitalize()} {item_name} remains unowned")
    
    debug_print(f"Blueprint ownership application complete: {owned_counts['ships']} owned ships, "
                f"{owned_counts['capital_ships']} owned capital ships")

def migrate_blueprint_config(config):
    """
    Migrate old blueprint configuration format to new format
    
    Args:
        config: Old configuration dictionary
    
    Returns:
        Updated configuration dictionary
    """
    new_config = create_default_blueprint_config()
    
    # Function to clean up keys (remove _data suffix if present)
    def clean_key(key):
        if key.endswith('_data'):
            return key[:-5]  # Remove _data suffix
        return key
    
    # Migrate ships
    if 'ships' in config:
        # Create a clean ships dictionary without duplicates
        clean_ships = {}
        for ship_name, ship_data in config['ships'].items():
            clean_name = clean_key(ship_name)
            
            # Convert legacy boolean format to dictionary
            new_data = {}
            if isinstance(ship_data, bool):
                new_data = {
                    'owned': ship_data,
                    'invented': False,
                    'me': 0,
                    'te': 0
                }
            # Convert legacy string format to dictionary
            elif isinstance(ship_data, str):
                new_data = {
                    'owned': ship_data == 'Owned',
                    'invented': ship_data == 'Invented',
                    'me': 0,
                    'te': 0
                }
            # Modern format - copy the dictionary
            elif isinstance(ship_data, dict):
                new_data = ship_data.copy()
                # Ensure all expected keys exist
                if 'owned' not in new_data:
                    new_data['owned'] = False
                if 'invented' not in new_data:
                    new_data['invented'] = False
                if 'me' not in new_data:
                    new_data['me'] = 0
                if 'te' not in new_data:
                    new_data['te'] = 0
            
            # Store with clean name, overwriting any duplicates with the same clean name
            clean_ships[clean_name] = new_data
            
        # Replace ships in new_config with cleaned dictionary
        new_config['ship_blueprints'] = clean_ships
    
    # Migrate capital ships
    if 'capital_ships' in config:
        # Create a clean capital ships dictionary without duplicates
        clean_cap_ships = {}
        for ship_name, ship_data in config['capital_ships'].items():
            clean_name = clean_key(ship_name)
            
            # Convert legacy boolean format to dictionary
            new_data = {}
            if isinstance(ship_data, bool):
                new_data = {
                    'owned': ship_data,
                    'invented': False,
                    'me': 0,
                    'te': 0
                }
            # Convert legacy string format to dictionary
            elif isinstance(ship_data, str):
                new_data = {
                    'owned': ship_data == 'Owned',
                    'invented': ship_data == 'Invented',
                    'me': 0,
                    'te': 0
                }
            # Modern format - copy the dictionary
            elif isinstance(ship_data, dict):
                new_data = ship_data.copy()
                # Ensure all expected keys exist
                if 'owned' not in new_data:
                    new_data['owned'] = False
                if 'invented' not in new_data:
                    new_data['invented'] = False
                if 'me' not in new_data:
                    new_data['me'] = 0
                if 'te' not in new_data:
                    new_data['te'] = 0
            
            # Store with clean name, overwriting any duplicates with the same clean name
            clean_cap_ships[clean_name] = new_data
            
        # Replace capital_ships in new_config with cleaned dictionary
        new_config['capital_ship_blueprints'] = clean_cap_ships
    
    # Migrate components
    if 'components' in config:
        # Create a clean components dictionary without duplicates
        clean_components = {}
        for component_name, component_data in config['components'].items():
            clean_name = clean_key(component_name)
            
            # Convert legacy boolean format to dictionary
            new_data = {}
            if isinstance(component_data, bool):
                new_data = {
                    'owned': component_data,
                    'invented': False,
                    'me': 0,
                    'te': 0
                }
            # Convert legacy string format to dictionary
            elif isinstance(component_data, str):
                new_data = {
                    'owned': component_data == 'Owned',
                    'invented': component_data == 'Invented',
                    'me': 0,
                    'te': 0
                }
            # Modern format - copy the dictionary
            elif isinstance(component_data, dict):
                new_data = component_data.copy()
                # Ensure all expected keys exist
                if 'owned' not in new_data:
                    new_data['owned'] = False
                if 'invented' not in new_data:
                    new_data['invented'] = False
                if 'me' not in new_data:
                    new_data['me'] = 0
                if 'te' not in new_data:
                    new_data['te'] = 0
            
            # Store with clean name, overwriting any duplicates with the same clean name
            clean_components[clean_name] = new_data
            
        # Replace components in new_config with cleaned dictionary
        new_config['components'] = clean_components
    
    # Migrate component blueprints
    if 'component_blueprints' in config:
        # Create a clean component blueprints dictionary without duplicates
        clean_component_blueprints = {}
        for blueprint_name, blueprint_data in config['component_blueprints'].items():
            clean_name = clean_key(blueprint_name)
            
            # Convert legacy boolean format to dictionary
            new_data = {}
            if isinstance(blueprint_data, bool):
                new_data = {
                    'owned': blueprint_data,
                    'invented': False,
                    'me': 0,
                    'te': 0
                }
            # Convert legacy string format to dictionary
            elif isinstance(blueprint_data, str):
                new_data = {
                    'owned': blueprint_data == 'Owned',
                    'invented': blueprint_data == 'Invented',
                    'me': 0,
                    'te': 0
                }
            # Modern format - copy the dictionary
            elif isinstance(blueprint_data, dict):
                new_data = blueprint_data.copy()
                # Ensure all expected keys exist
                if 'owned' not in new_data:
                    new_data['owned'] = False
                if 'invented' not in new_data:
                    new_data['invented'] = False
                if 'me' not in new_data:
                    new_data['me'] = 0
                if 'te' not in new_data:
                    new_data['te'] = 0
            
            # Store with clean name, overwriting any duplicates with the same clean name
            clean_component_blueprints[clean_name] = new_data
            
        # Replace component_blueprints in new_config with cleaned dictionary
        new_config['component_blueprints'] = clean_component_blueprints
    
    # Save the migrated configuration to ensure it's cleaned up
    success = save_blueprint_ownership(new_config)
    if success:
        debug_print("Configuration saved successfully.")
    else:
        debug_print("Failed to save configuration.")
    
    return new_config
