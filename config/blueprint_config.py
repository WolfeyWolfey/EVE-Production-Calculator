"""
Blueprint configuration manager for EVE Production Calculator
Handles saving and loading blueprint ownership status
"""

import os
import json

# Constants
CONFIG_FILENAME = "blueprint_ownership.json"
CONFIG_FILE = os.path.join(os.path.dirname(__file__), CONFIG_FILENAME)

def create_default_blueprint_config():
    """
    Create default blueprint configuration structure
    """
    return {
        'ships': {},
        'capital_ships': {},
        'components': {},
        'component_blueprints': {}  # For individual capital component blueprints
    }

def load_blueprint_ownership():
    """
    Load blueprint ownership configuration from file
    """
    print("Loading blueprint ownership from file...")
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                print(f"Loaded configuration from {CONFIG_FILE}")
                
                # Verify if any ships are set to owned
                owned_ships = []
                for ship_name, ship_data in config.get('ships', {}).items():
                    if ship_data.get('owned', False):
                        owned_ships.append(ship_name)
                
                if owned_ships:
                    print(f"Found {len(owned_ships)} owned ships in configuration: {', '.join(owned_ships)}")
                else:
                    print("No owned ships found in loaded configuration")
                
                return migrate_blueprint_config(config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading blueprint configuration: {e}")
            return create_default_blueprint_config()
    else:
        # Create default configuration
        print(f"Configuration file not found at {CONFIG_FILE}, creating default config")
        config = create_default_blueprint_config()
        save_blueprint_ownership(config)
        return config

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
                print(f"Could not read existing config file (will create new): {e}")
                
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
        print(f"Attempting to save blueprint configuration...")
        with open(CONFIG_FILE, 'w') as f:
            json.dump(existing_config, f, indent=4)
        print(f"Blueprint configuration saved successfully to: {CONFIG_FILE}")
        return True
    except Exception as e:
        print(f"Error saving blueprint configuration: {e}")
        return False

def update_blueprint_ownership(config, category, blueprint_name, ownership_status):
    """
    Update ownership status for a specific blueprint
    
    Args:
        config: The blueprint configuration dictionary
        category: Category of the blueprint (ships, capital_ships, components)
        blueprint_name: Name of the blueprint
        ownership_status: New ownership status (Owned or Unowned)
    """
    # Make sure the category exists in config
    if category not in config:
        config[category] = {}
    
    # If blueprint doesn't exist in config, create it
    if blueprint_name not in config[category]:
        config[category][blueprint_name] = {
            'owned': ownership_status == 'Owned',
            'invented': False,
            'me': 0,  # Default ME% is 0
            'te': 0   # Default TE% is 0
        }
    else:
        # Update the ownership status
        config[category][blueprint_name]['owned'] = ownership_status == 'Owned'
    
    # Save the updated config
    success = save_blueprint_ownership(config)
    if success:
        print("Configuration saved successfully.")
    else:
        print("Failed to save configuration.")
    
    return config

def update_blueprint_invention(config, category, blueprint_name, is_invented):
    """
    Update invention status for a specific blueprint
    
    Args:
        config: The blueprint configuration dictionary
        category: Category of the blueprint (ships, capital_ships, components)
        blueprint_name: Name of the blueprint
        is_invented: Boolean indicating whether the blueprint is invented
    """
    # Make sure the category exists in config
    if category not in config:
        config[category] = {}
    
    # If blueprint doesn't exist in config, create it
    if blueprint_name not in config[category]:
        config[category][blueprint_name] = {
            'owned': False,
            'invented': is_invented,
            'me': 0,  # Default ME% is 0
            'te': 0   # Default TE% is 0
        }
    else:
        # Update the invention status
        config[category][blueprint_name]['invented'] = is_invented
    
    # Save the updated config
    success = save_blueprint_ownership(config)
    if success:
        print("Configuration saved successfully.")
    else:
        print("Failed to save configuration.")
    
    return config

def update_blueprint_me(config, category, blueprint_name, me_value):
    """
    Update material efficiency for a specific blueprint
    
    Args:
        config: The blueprint configuration dictionary
        category: Category of the blueprint (ships, capital_ships, components)
        blueprint_name: Name of the blueprint
        me_value: Material Efficiency percentage (0-10)
    """
    # Make sure the category exists in config
    if category not in config:
        config[category] = {}
    
    # If blueprint doesn't exist in config, create it
    if blueprint_name not in config[category]:
        config[category][blueprint_name] = {
            'owned': False,
            'invented': False,
            'me': me_value,
            'te': 0  # Default TE value
        }
    else:
        # Update the ME value
        config[category][blueprint_name]['me'] = me_value
    
    # Save the updated config
    success = save_blueprint_ownership(config)
    if success:
        print("Configuration saved successfully.")
    else:
        print("Failed to save configuration.")
    
    return config

def update_blueprint_te(config, category, blueprint_name, te_value):
    """
    Update time efficiency for a specific blueprint
    
    Args:
        config: The blueprint configuration dictionary
        category: Category of the blueprint (ships, capital_ships, components)
        blueprint_name: Name of the blueprint
        te_value: Time Efficiency percentage (0-20)
    """
    # Make sure the category exists in config
    if category not in config:
        config[category] = {}
    
    # If blueprint doesn't exist in config, create it
    if blueprint_name not in config[category]:
        config[category][blueprint_name] = {
            'owned': False,
            'invented': False,
            'me': 0,  # Default ME value
            'te': te_value
        }
    else:
        # Update the TE value
        config[category][blueprint_name]['te'] = te_value
    
    # Save the updated config
    success = save_blueprint_ownership(config)
    if success:
        print("Configuration saved successfully.")
    else:
        print("Failed to save configuration.")
    
    return config

def get_blueprint_ownership(config, category, blueprint_name):
    """
    Get ownership status for a specific blueprint
    
    Args:
        config: The blueprint configuration dictionary
        category: Category of the blueprint (ships, capital_ships, components)
        blueprint_name: Name of the blueprint
        
    Returns:
        String 'Owned' or 'Unowned'
    """
    if category in config and blueprint_name in config[category]:
        return 'Owned' if config[category][blueprint_name].get('owned', False) else 'Unowned'
    return 'Unowned'

def get_blueprint_me(config, category, blueprint_name):
    """
    Get material efficiency value for a blueprint
    
    Args:
        config: Blueprint configuration dictionary
        category: Category of blueprint (ships, capital_ships, components)
        blueprint_name: Name of the blueprint
        
    Returns:
        Material Efficiency level (default: 0)
    """
    try:
        if category not in config or blueprint_name not in config[category]:
            return 0
            
        # Get the blueprint data
        bp_data = config[category][blueprint_name]
        
        # Handle different data formats
        if isinstance(bp_data, dict) and 'me' in bp_data:
            return bp_data['me']
        return 0
    except Exception as e:
        print(f"Error getting ME% for {blueprint_name}: {e}")
        return 0

def get_blueprint_te(config, category, blueprint_name):
    """
    Get time efficiency value for a blueprint
    
    Args:
        config: Blueprint configuration dictionary
        category: Category of blueprint (ships, capital_ships, components)
        blueprint_name: Name of the blueprint
        
    Returns:
        Time Efficiency level (default: 0)
    """
    try:
        if category not in config or blueprint_name not in config[category]:
            return 0
            
        # Get the blueprint data
        bp_data = config[category][blueprint_name]
        
        # Handle different data formats
        if isinstance(bp_data, dict) and 'te' in bp_data:
            return bp_data['te']
        return 0
    except Exception as e:
        print(f"Error getting TE% for {blueprint_name}: {e}")
        return 0

def apply_blueprint_ownership(config, registry):
    """
    Apply blueprint ownership settings from configuration to the registry
    
    Args:
        config: The blueprint configuration dictionary
        registry: The ModuleRegistry instance
    """
    print("Applying blueprint ownership settings to registry...")
    
    if not config:
        print("No blueprint configuration provided, skipping ownership application")
        return
    
    owned_ship_count = 0
    
    # Apply ship ownership
    if 'ships' in config:
        print(f"Processing {len(config['ships'])} ships in configuration")
        for ship_name, ship_data in config['ships'].items():
            # Find the ship in the registry
            if hasattr(registry, 'ships') and ship_name in registry.ships:
                owned_value = ship_data.get('owned', False)
                registry.ships[ship_name].owned_status = owned_value
                
                if owned_value:
                    owned_ship_count += 1
                    print(f"Setting ship {ship_name} ownership to: True")
                # Only print unowned ships in debug mode to reduce console output
                else:
                    print(f"Ship {ship_name} remains unowned")
    
    # Apply capital ship ownership
    owned_capital_count = 0
    if 'capital_ships' in config:
        print(f"Processing {len(config['capital_ships'])} capital ships in configuration")
        for ship_name, ship_data in config['capital_ships'].items():
            # Find the ship in the registry
            if hasattr(registry, 'capital_ships') and ship_name in registry.capital_ships:
                owned_value = ship_data.get('owned', False)
                registry.capital_ships[ship_name].owned_status = owned_value
                
                if owned_value:
                    owned_capital_count += 1
                    print(f"Setting capital ship {ship_name} ownership to: True")
                # Only print unowned ships in debug mode
                else:
                    print(f"Capital ship {ship_name} remains unowned")
    
    # Apply component ownership
    if 'components' in config and hasattr(registry, 'components'):
        for comp_name, comp_data in config['components'].items():
            if comp_name in registry.components:
                registry.components[comp_name].owned_status = comp_data.get('owned', False)
    
    # Apply capital component ownership
    if 'component_blueprints' in config and hasattr(registry, 'capital_components'):
        for comp_name, comp_data in config['component_blueprints'].items():
            if comp_name in registry.capital_components:
                registry.capital_components[comp_name].blueprint_owned = comp_data.get('owned', False)
    
    print(f"Blueprint ownership application complete: {owned_ship_count} owned ships, {owned_capital_count} owned capital ships")

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
        new_config['ships'] = clean_ships
    
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
        new_config['capital_ships'] = clean_cap_ships
    
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
        print("Configuration saved successfully.")
    else:
        print("Failed to save configuration.")
    
    return new_config
