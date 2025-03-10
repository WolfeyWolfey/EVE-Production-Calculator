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

def update_blueprint_invention(config, category, blueprint_name, is_invented):
    """
    Update invention status for a specific blueprint
    
    Args:
        config: The blueprint configuration dictionary
        category: Category of the blueprint (ships, capital_ships, components)
        blueprint_name: Name of the blueprint
        is_invented: Boolean indicating whether the blueprint is invented
    """
    if 'invention_status' not in config:
        config['invention_status'] = {}
        
    if category not in config['invention_status']:
        config['invention_status'][category] = {}
    
    # Special handling for individual capital components
    if ':' in blueprint_name and category == 'components':
        module_name, component_name = blueprint_name.split(':', 1)
        if 'component_blueprints' not in config['invention_status']:
            config['invention_status']['component_blueprints'] = {}
        
        if module_name not in config['invention_status']['component_blueprints']:
            config['invention_status']['component_blueprints'][module_name] = {}
        
        config['invention_status']['component_blueprints'][module_name][component_name] = is_invented
    else:
        config['invention_status'][category][blueprint_name] = is_invented
    
    save_blueprint_ownership(config)
    return True

def apply_blueprint_ownership(config, module_registry):
    """
    Apply loaded blueprint ownership settings to module registry
    
    Args:
        config: Blueprint configuration dictionary
        module_registry: ModuleRegistry containing all modules
    """
    # Apply ownership for ships
    if 'ships' in config:
        all_ships = module_registry.get_all_ships()
        for ship_name, ship in all_ships.items():
            if ship.display_name in config['ships']:
                ship.owned_status = config['ships'][ship.display_name]
    
    # Apply ownership for capital ships
    if 'capital_ships' in config:
        all_capital_ships = module_registry.get_all_capital_ships()
        for cap_ship_name, capital_ship in all_capital_ships.items():
            if capital_ship.display_name in config['capital_ships']:
                capital_ship.owned_status = config['capital_ships'][capital_ship.display_name]
    
    # Apply ownership for components
    if 'components' in config:
        all_components = module_registry.get_all_components()
        for comp_name, component in all_components.items():
            if component.display_name in config['components']:
                component.owned_status = config['components'][component.display_name]

def get_blueprint_ownership(config, category, blueprint_name):
    """Get ownership status for a specific blueprint"""
    if category in config and blueprint_name in config[category]:
        return config[category][blueprint_name]
    return "Unowned"  # Default status
