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
                return json.load(f)
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
    if category not in config:
        config[category] = {}
    
    # Special handling for individual capital components
    if ':' in blueprint_name and category == 'components':
        module_name, component_name = blueprint_name.split(':', 1)
        if 'component_blueprints' not in config:
            config['component_blueprints'] = {}
        
        if module_name not in config['component_blueprints']:
            config['component_blueprints'][module_name] = {}
        
        config['component_blueprints'][module_name][component_name] = ownership_status
    else:
        config[category][blueprint_name] = ownership_status
    
    save_blueprint_ownership(config)
    return True

def apply_blueprint_ownership(modules, config):
    """
    Apply loaded blueprint ownership settings to modules
    
    Args:
        modules: Dictionary of ship and component modules
        config: Blueprint configuration dictionary
    """
    # Apply ownership for ships
    if 'ships' in modules and 'ships' in config:
        for ship_name, ship_module in modules['ships'].items():
            if ship_module.display_name in config['ships']:
                ship_module.owned_status = config['ships'][ship_module.display_name]
    
    # Apply ownership for capital ships
    if 'capital_ships' in modules and 'capital_ships' in config:
        for ship_name, ship_module in modules['capital_ships'].items():
            if ship_module.display_name in config['capital_ships']:
                ship_module.owned_status = config['capital_ships'][ship_module.display_name]
    
    # Apply ownership for components
    if 'components' in modules and 'components' in config:
        for component_name, component_module in modules['components'].items():
            if component_module.display_name in config['components']:
                component_module.owned_status = config['components'][component_module.display_name]
    
    # Apply ownership for individual capital components
    if 'components' in modules and 'component_blueprints' in config:
        for module_name, components in config['component_blueprints'].items():
            for component_name, component_module in modules['components'].items():
                if component_module.display_name == module_name and hasattr(component_module, 'capital_component_data'):
                    for cap_component_name, ownership_status in components.items():
                        if cap_component_name in component_module.capital_component_data:
                            component_module.capital_component_data[cap_component_name]["blueprint_owned"] = ownership_status

def get_blueprint_ownership(config, category, blueprint_name):
    """Get ownership status for a specific blueprint"""
    if category in config and blueprint_name in config[category]:
        return config[category][blueprint_name]
    return "Unowned"  # Default status
