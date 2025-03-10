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
    
    Args:
        config: The blueprint configuration dictionary to save
    
    Returns:
        True if successful, False otherwise
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
            'me': 0,  # Default ME% is 0
            'te': 0   # Default TE% is 0
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
            'me': 0,  # Default ME% is 0
            'te': 0   # Default TE% is 0
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
            'me': me_value,
            'te': 0  # Default TE value
        }
    else:
        # Update the ME value
        config[category][blueprint_name]['me'] = me_value
    
    # Save the updated config
    save_blueprint_ownership(config)
    
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

def apply_blueprint_ownership(config, module_registry):
    """
    Apply blueprint ownership information to modules in the registry
    
    Args:
        config: Blueprint configuration dictionary
        module_registry: Module registry containing ships, components, etc.
    """
    if not config:
        return
    
    # Apply to ships
    if 'ships' in config and hasattr(module_registry, 'ships'):
        for ship_name, ship_data in config['ships'].items():
            if ship_name in module_registry.ships:
                # Get the owned status from the config - handle both string and boolean formats
                if 'owned' in ship_data:
                    # Convert string to boolean if needed
                    ownership = ship_data['owned']
                    if isinstance(ownership, str):
                        ownership = (ownership.lower() == 'owned' or ownership.lower() == 'true')
                    module_registry.ships[ship_name].owned_status = ownership
                
                # Set the invention status
                if 'invented' in ship_data:
                    module_registry.ships[ship_name].invention_status = ship_data['invented']
                
                # Set ME and TE if present
                if 'me' in ship_data:
                    module_registry.ships[ship_name].me = ship_data['me']
                
                if 'te' in ship_data:
                    module_registry.ships[ship_name].te = ship_data['te']
            else:
                # Try looking for the ship by display name
                for reg_ship_name, ship in module_registry.ships.items():
                    if hasattr(ship, 'display_name') and ship.display_name == ship_name:
                        # Get the owned status from the config - handle both string and boolean formats
                        if 'owned' in ship_data:
                            # Convert string to boolean if needed
                            ownership = ship_data['owned']
                            if isinstance(ownership, str):
                                ownership = (ownership.lower() == 'owned' or ownership.lower() == 'true')
                            ship.owned_status = ownership
                        
                        # Set the invention status
                        if 'invented' in ship_data:
                            ship.invention_status = ship_data['invented']
                        
                        # Set ME and TE if present
                        if 'me' in ship_data:
                            ship.me = ship_data['me']
                        
                        if 'te' in ship_data:
                            ship.te = ship_data['te']
                        break
    
    # Apply to capital ships
    if 'capital_ships' in config and hasattr(module_registry, 'capital_ships'):
        for ship_name, ship_data in config['capital_ships'].items():
            if ship_name in module_registry.capital_ships:
                # Get the owned status from the config - handle both string and boolean formats
                if 'owned' in ship_data:
                    # Convert string to boolean if needed
                    ownership = ship_data['owned']
                    if isinstance(ownership, str):
                        ownership = (ownership.lower() == 'owned' or ownership.lower() == 'true')
                    module_registry.capital_ships[ship_name].owned_status = ownership
                
                # Set the invention status
                if 'invented' in ship_data:
                    module_registry.capital_ships[ship_name].invention_status = ship_data['invented']
                
                # Set ME and TE if present
                if 'me' in ship_data:
                    module_registry.capital_ships[ship_name].me = ship_data['me']
                
                if 'te' in ship_data:
                    module_registry.capital_ships[ship_name].te = ship_data['te']
            else:
                # Try looking for the ship by display name
                for reg_ship_name, ship in module_registry.capital_ships.items():
                    if hasattr(ship, 'display_name') and ship.display_name == ship_name:
                        # Get the owned status from the config - handle both string and boolean formats
                        if 'owned' in ship_data:
                            # Convert string to boolean if needed
                            ownership = ship_data['owned']
                            if isinstance(ownership, str):
                                ownership = (ownership.lower() == 'owned' or ownership.lower() == 'true')
                            ship.owned_status = ownership
                        
                        # Set the invention status
                        if 'invented' in ship_data:
                            ship.invention_status = ship_data['invented']
                        
                        # Set ME and TE if present
                        if 'me' in ship_data:
                            ship.me = ship_data['me']
                        
                        if 'te' in ship_data:
                            ship.te = ship_data['te']
                        break
    
    # Apply to components
    if 'components' in config and hasattr(module_registry, 'components'):
        for comp_name, comp_data in config['components'].items():
            if comp_name in module_registry.components:
                # Get the owned status from the config - handle both string and boolean formats
                if 'owned' in comp_data:
                    # Convert string to boolean if needed
                    ownership = comp_data['owned']
                    if isinstance(ownership, str):
                        ownership = (ownership.lower() == 'owned' or ownership.lower() == 'true')
                    module_registry.components[comp_name].owned_status = ownership
                
                # Set the invention status
                if 'invented' in comp_data:
                    module_registry.components[comp_name].invention_status = comp_data['invented']
                
                # Set ME and TE if present
                if 'me' in comp_data:
                    module_registry.components[comp_name].me = comp_data['me']
                
                if 'te' in comp_data:
                    module_registry.components[comp_name].te = comp_data['te']
            else:
                # Try looking for the component by display name
                for reg_comp_name, comp in module_registry.components.items():
                    if hasattr(comp, 'display_name') and comp.display_name == comp_name:
                        # Get the owned status from the config - handle both string and boolean formats
                        if 'owned' in comp_data:
                            # Convert string to boolean if needed
                            ownership = comp_data['owned']
                            if isinstance(ownership, str):
                                ownership = (ownership.lower() == 'owned' or ownership.lower() == 'true')
                            comp.owned_status = ownership
                        
                        # Set the invention status
                        if 'invented' in comp_data:
                            comp.invention_status = comp_data['invented']
                        
                        # Set ME and TE if present
                        if 'me' in comp_data:
                            comp.me = comp_data['me']
                        
                        if 'te' in comp_data:
                            comp.te = comp_data['te']
                        break

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
    
    # Save the migrated configuration to ensure it's cleaned up
    save_blueprint_ownership(new_config)
    
    return new_config
