"""
Blueprint configuration manager for EVE Production Calculator
Handles saving and loading blueprint ownership status
"""

import os
import json

# Constants
CONFIG_FILE = "blueprint_ownership.json"

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
    config_path = os.path.join(os.path.dirname(__file__), CONFIG_FILE)
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                return migrate_blueprint_config(config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading blueprint configuration: {e}")
            return create_default_blueprint_config()
    else:
        # Create default configuration
        config = create_default_blueprint_config()
        save_blueprint_ownership(config)
        return config

def save_blueprint_ownership(config):
    """
    Save blueprint ownership configuration to file
    """
    config_path = os.path.join(os.path.dirname(__file__), CONFIG_FILE)
    
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except IOError as e:
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
            'me': 0  # Default ME% is 0
        }
    else:
        # Update the ownership status
        config[category][blueprint_name]['owned'] = ownership_status == 'Owned'
    
    # Save the updated config
    save_blueprint_ownership(config)
    
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
            'me': 0  # Default ME% is 0
        }
    else:
        # Update the invention status
        config[category][blueprint_name]['invented'] = is_invented
    
    # Save the updated config
    save_blueprint_ownership(config)
    
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
            'me': me_value
        }
    else:
        # Update the ME value
        config[category][blueprint_name]['me'] = me_value
    
    # Save the updated config
    save_blueprint_ownership(config)
    
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

def apply_blueprint_ownership(config, module_registry):
    """
    Apply ownership settings from config to module registry
    
    Args:
        config: Blueprint configuration dictionary
        module_registry: Module registry to apply settings to
    """
    # Apply ownership for ships
    if 'ships' in config:
        all_ships = module_registry.get_all_ships()
        for ship_name, ship in all_ships.items():
            if ship.display_name in config['ships']:
                if isinstance(config['ships'][ship.display_name], dict):
                    ship.owned_status = config['ships'][ship.display_name].get('owned', False)
                else:
                    # Legacy format - string 'Owned' or 'Unowned'
                    ownership_value = config['ships'][ship.display_name]
                    ship.owned_status = ownership_value == 'Owned' if isinstance(ownership_value, str) else ownership_value
    
    # Apply ownership for capital ships
    if 'capital_ships' in config:
        all_capital_ships = module_registry.get_all_capital_ships()
        for cap_ship_name, capital_ship in all_capital_ships.items():
            if capital_ship.display_name in config['capital_ships']:
                if isinstance(config['capital_ships'][capital_ship.display_name], dict):
                    capital_ship.owned_status = config['capital_ships'][capital_ship.display_name].get('owned', False)
                else:
                    # Legacy format
                    ownership_value = config['capital_ships'][capital_ship.display_name]
                    capital_ship.owned_status = ownership_value == 'Owned' if isinstance(ownership_value, str) else ownership_value
    
    # Apply ownership for components
    if 'components' in config:
        all_components = module_registry.get_all_components()
        for comp_name, component in all_components.items():
            if component.display_name in config['components']:
                if isinstance(config['components'][component.display_name], dict):
                    component.owned_status = config['components'][component.display_name].get('owned', False)
                else:
                    # Legacy format
                    ownership_value = config['components'][component.display_name]
                    component.owned_status = ownership_value == 'Owned' if isinstance(ownership_value, str) else ownership_value

def migrate_blueprint_config(config):
    """
    Migrate older blueprint config format to new format with ME%
    
    This function converts old string-based blueprint ownership values 
    to the new dictionary format with ownership, invention, and ME% values
    
    Args:
        config: The blueprint configuration to migrate
        
    Returns:
        Updated blueprint configuration
    """
    # Check if migration is needed
    migration_needed = False
    
    # Check ships
    if 'ships' in config:
        for ship_name, value in list(config['ships'].items()):
            if isinstance(value, str) or isinstance(value, bool):
                migration_needed = True
                owned_status = value == 'Owned' if isinstance(value, str) else value
                config['ships'][ship_name] = {
                    'owned': owned_status,
                    'invented': False,
                    'me': 0
                }
    
    # Check capital ships
    if 'capital_ships' in config:
        for ship_name, value in list(config['capital_ships'].items()):
            if isinstance(value, str) or isinstance(value, bool):
                migration_needed = True
                owned_status = value == 'Owned' if isinstance(value, str) else value
                config['capital_ships'][ship_name] = {
                    'owned': owned_status,
                    'invented': False,
                    'me': 0
                }
    
    # Check components
    if 'components' in config:
        for comp_name, value in list(config['components'].items()):
            if isinstance(value, str) or isinstance(value, bool):
                migration_needed = True
                owned_status = value == 'Owned' if isinstance(value, str) else value
                config['components'][comp_name] = {
                    'owned': owned_status,
                    'invented': False,
                    'me': 0
                }
    
    # Clean up old invention status
    if 'invention_status' in config:
        # Migrate invention status to new format
        if 'ships' in config.get('invention_status', {}):
            for ship_name, invented in config['invention_status']['ships'].items():
                if ship_name in config['ships']:
                    config['ships'][ship_name]['invented'] = invented
        
        if 'capital_ships' in config.get('invention_status', {}):
            for ship_name, invented in config['invention_status']['capital_ships'].items():
                if ship_name in config['capital_ships']:
                    config['capital_ships'][ship_name]['invented'] = invented
        
        if 'components' in config.get('invention_status', {}):
            for comp_name, invented in config['invention_status']['components'].items():
                if comp_name in config['components']:
                    config['components'][comp_name]['invented'] = invented
        
        # Remove old invention status
        config.pop('invention_status', None)
    
    # If we were using the old settings with global ME%, migrate it
    if 'settings' in config and 'material_efficiency' in config['settings']:
        me_value = config['settings']['material_efficiency']
        
        # Apply the global ME% to all blueprints
        for category in ['ships', 'capital_ships', 'components']:
            if category in config:
                for name, data in config[category].items():
                    if isinstance(data, dict):
                        data['me'] = me_value
        
        # Remove old settings
        config.pop('settings', None)
    
    if migration_needed:
        print("Blueprint configuration migrated to new format")
    
    return config
