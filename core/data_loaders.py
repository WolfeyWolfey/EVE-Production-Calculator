"""
Data loaders for EVE Production Calculator

This file contains functions for loading data from JSON files into the module registry
"""
import os
import json
import importlib.util
import sys
from utils.debug import debug_print
from typing import Dict, List, Any, Optional, Set, Tuple
import glob

from core.module_registry import ModuleRegistry
from core.models import ShipModule, CapitalShipModule, ComponentModule, PiMaterialModule

def load_ships(registry: ModuleRegistry, base_path: str):
    """
    Load ship data from JSON files into the registry
    
    Args:
        registry: The module registry
        base_path: Base path of the application
    """
    # Store existing ownership status before loading
    existing_ownership = {}
    for ship in registry.get_all_ships():
        existing_ownership[ship.name] = ship.owned_status
    
    # Initialize counters
    ship_count = 0
    capital_ship_count = 0
    
    # Create ships directory if it doesn't exist
    ships_dir = os.path.join(base_path, 'data', 'ships')
    if not os.path.exists(ships_dir):
        os.makedirs(ships_dir)
    
    # Get all JSON files in the ships directory
    ship_files = glob.glob(os.path.join(ships_dir, '*.json'))
    
    # If no files in ships directory, check for legacy ships.json in data directory
    if not ship_files:
        legacy_ship_path = os.path.join(base_path, 'data', 'ships.json')
        if os.path.exists(legacy_ship_path):
            ship_files = [legacy_ship_path]
    
    if not ship_files:
        debug_print("No ship data files found")
        return
    
    try:
        # Combine all ship data from all files
        all_ship_data = {}
        
        for ship_file in ship_files:
            debug_print(f"Loading ship data from: {ship_file}")
            try:
                with open(ship_file, 'r') as f:
                    file_data = json.load(f)
                    
                # Check if this file contains capital ships as a top-level key
                if 'capital_ships' in file_data:
                    # Process capital ships directly
                    capital_ships_data = file_data.pop('capital_ships')
                    for ship_type, ships in capital_ships_data.items():
                        for ship_name, ship_data in ships.items():
                            if 'display_name' in ship_data:
                                # Create capital ship module
                                capital_ship = CapitalShipModule(
                                    name=ship_name,
                                    display_name=ship_data.get('display_name', ship_name.title()),
                                    requirements=ship_data.get('requirements', {}),
                                    details=ship_data.get('details', ''),
                                    faction=ship_data.get('faction', 'unknown'),
                                    ship_type=ship_data.get('ship_type', ship_type),
                                    # Use existing ownership status if available, otherwise default to "Unowned"
                                    owned_status=ship_data.get('owned_status', "Unowned") == "Owned"
                                )
                                
                                # Register the capital ship
                                registry.register_capital_ship(capital_ship)
                                capital_ship_count += 1
                
                # Merge the remaining data (regular ships)
                for key, value in file_data.items():
                    if key in all_ship_data:
                        # If the key already exists, merge the nested dictionaries
                        if isinstance(value, dict) and isinstance(all_ship_data[key], dict):
                            all_ship_data[key].update(value)
                    else:
                        # If the key doesn't exist, add it
                        all_ship_data[key] = value
            
            except Exception as e:
                debug_print(f"Error loading ship data from {ship_file}: {e}")
        
        # Process regular ships (hierarchical structure by faction)
        for faction, faction_data in all_ship_data.items():
            if isinstance(faction_data, dict):
                # Process each ship class (frigates, destroyers, etc.)
                for ship_class, class_data in faction_data.items():
                    if isinstance(class_data, dict):
                        # Process tech levels (tech1, tech2, etc.)
                        for tech_level, tech_data in class_data.items():
                            if isinstance(tech_data, dict):
                                # Process individual ships
                                for ship_name, ship_data in tech_data.items():
                                    if isinstance(ship_data, dict) and 'display_name' in ship_data:
                                        # Create ship module
                                        ship = ShipModule(
                                            name=ship_name,
                                            display_name=ship_data.get('display_name', ship_name.title()),
                                            requirements=ship_data.get('requirements', {}),
                                            details=ship_data.get('details', ''),
                                            faction=ship_data.get('faction', faction),
                                            ship_type=ship_data.get('ship_type', ship_class),
                                            # Use existing ownership status if available, otherwise use from data or default to "Unowned"
                                            owned_status=ship_data.get('owned_status', "Unowned") == "Owned"
                                        )
                                        
                                        # Register the ship
                                        registry.register_ship(ship)
                                        ship_count += 1
        
        debug_print(f"Loaded {ship_count} ships and {capital_ship_count} capital ships from {len(ship_files)} files")
    
    except Exception as e:
        debug_print(f"Error loading ships: {e}")

def process_ship_category(registry: ModuleRegistry, parent_key: str, category_data: Dict, existing_ownership: Dict = None):
    """
    Process a ship category and add to registry
    
    Args:
        registry: The module registry
        parent_key: Parent key for the ships (e.g. faction)
        category_data: Data for this category
        existing_ownership: Dictionary of existing ownership values
    """
    # Check if this is a ship or a nested category
    if is_ship_data(category_data):
        # This is a ship, extract tier if available
        tier = category_data.get('tier', 1)
        
        # Create a ship module
        ship_module = ShipModule(
            name=parent_key.lower(),
            display_name=category_data.get('display_name', parent_key.title()),
            faction=category_data.get('faction', 'unknown'),
            ship_type=category_data.get('type', 'unknown'),
            tier=tier,
            # Use existing ownership status if available, otherwise default to False
            owned_status=existing_ownership.get(parent_key.lower(), False) if existing_ownership else False
        )
        
        # Register the ship
        registry.register_ship(ship_module)
    else:
        # This is a nested category, process each child
        for key, value in category_data.items():
            # Process child category
            process_ship_category(registry, key, value, existing_ownership)

def process_capital_ships(registry: ModuleRegistry, capital_ships_data: Dict, existing_ownership: Dict = None):
    """
    Process capital ships and add to registry
    
    Args:
        registry: The module registry
        capital_ships_data: Data for capital ships
        existing_ownership: Dictionary of existing ownership values
    """
    # Process each capital ship
    for ship_key, ship_data in capital_ships_data.items():
        # Create a capital ship module
        capital_ship = CapitalShipModule(
            name=ship_key.lower(),
            display_name=ship_data.get('display_name', ship_key.title()),
            ship_type=ship_data.get('type', 'unknown'),
            # Use existing ownership status if available, otherwise default to False
            owned_status=existing_ownership.get(ship_key.lower(), False) if existing_ownership else False
        )
        
        # Register the capital ship
        registry.register_capital_ship(capital_ship)

def is_ship_data(data: Dict) -> bool:
    """
    Check if a dictionary represents ship data
    
    Args:
        data: Dictionary to check
        
    Returns:
        True if this is ship data, False otherwise
    """
    # Ship data has display_name and requirements keys
    return isinstance(data, dict) and 'display_name' in data and 'requirements' in data

def load_capital_components(registry: ModuleRegistry, base_path: str):
    """
    Load capital components from JSON file
    
    Args:
        registry: The module registry to populate
        base_path: Base path of the application
    """
    # Load capital components from JSON file
    components_path = os.path.join(base_path, 'data', 'capitalcomponents.json')
    
    try:
        if os.path.exists(components_path):
            with open(components_path, 'r') as f:
                components_data = json.load(f)
            
            capital_components = components_data.get("capital_components", {})
            for component_name, component_data in capital_components.items():
                component = ComponentModule(
                    name=component_name,
                    display_name=component_data.get("display_name", component_name),
                    requirements=component_data.get("requirements", {}),
                    details=component_data.get("details", ""),
                    owned_status=component_data.get("owned_status", False)
                )
                registry.register_capital_component(component)
                
    except Exception as e:
        debug_print(f"Error loading capital components: {e}")

def load_components(registry: ModuleRegistry, base_path: str):
    """
    Load components from JSON files and Python modules
    
    Args:
        registry: The module registry to populate
        base_path: Base path of the application
    """
    # First load capital components
    load_capital_components(registry, base_path)
    
    # Load regular components from JSON file
    components_path = os.path.join(base_path, 'data', 'components.json')
    
    try:
        if os.path.exists(components_path):
            with open(components_path, 'r') as f:
                components_data = json.load(f)
            
            components = components_data.get("components", {})
            for component_name, component_data in components.items():
                component = ComponentModule(
                    name=component_name,
                    display_name=component_data.get("display_name", component_name),
                    requirements=component_data.get("requirements", {}),
                    details=component_data.get("details", ""),
                    owned_status=component_data.get("owned_status", False)
                )
                registry.register_component(component)
                
    except Exception as e:
        debug_print(f"Error loading components from JSON: {e}")
    
    # Also try loading from Python modules in Components directory
    components_dir = os.path.join(base_path, 'Components')
    
    if os.path.exists(components_dir):
        components_loaded = 0
        for filename in os.listdir(components_dir):
            if filename.endswith('.py'):
                # Module name is the filename without extension
                module_name = filename[:-3]
                
                # Construct absolute path to the module
                module_path = os.path.join(components_dir, filename)
                
                try:
                    # Create a module spec and load the module
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Check if module has required attributes
                    if hasattr(module, 'display_name'):
                        # Create component module
                        component = ComponentModule(
                            name=module_name,
                            display_name=getattr(module, 'display_name', module_name),
                            requirements=getattr(module, module_name + '_requirements', {}),
                            details=getattr(module, 'details', ''),
                            owned_status=getattr(module, 'owned_status', False)
                        )
                        
                        # Register component
                        registry.register_component(component)
                        components_loaded += 1
                except Exception as e:
                    debug_print(f"Error loading component module {module_path}: {e}")

def load_pi_data(registry: ModuleRegistry, base_path: str):
    """
    Load PI data from JSON files in the PI folder
    
    Args:
        registry: The module registry to populate
        base_path: Base path of the application
    """
    pi_folder = os.path.join(base_path, 'data', 'PI')
    
    # If the PI folder doesn't exist, fallback to the legacy file
    if not os.path.exists(pi_folder):
        legacy_pi_path = os.path.join(base_path, 'data', 'PI_Components.json')
        debug_print(f"PI folder not found, trying legacy path: {legacy_pi_path}")
        
        try:
            with open(legacy_pi_path, 'r') as f:
                pi_data = json.load(f)
                debug_print(f"Loading PI data from legacy file: {legacy_pi_path}")
                load_pi_data_from_dict(registry, pi_data)
        except Exception as e:
            debug_print(f"Error loading legacy PI data: {e}")
        return
    
    debug_print(f"Loading PI data from folder: {pi_folder}")
    
    # Load P0 components
    p0_path = os.path.join(pi_folder, 'P0_PI_Components.json')
    if os.path.exists(p0_path):
        try:
            with open(p0_path, 'r') as f:
                p0_data = json.load(f)
                debug_print(f"Loading P0 PI components from: {p0_path}")
                load_pi_data_from_dict(registry, p0_data)
        except Exception as e:
            debug_print(f"Error loading P0 PI data: {e}")
    else:
        debug_print(f"P0 PI components file not found: {p0_path}")
    
    # Load P1 components
    p1_path = os.path.join(pi_folder, 'P1_PI_Components.json')
    if os.path.exists(p1_path):
        try:
            with open(p1_path, 'r') as f:
                p1_data = json.load(f)
                debug_print(f"Loading P1 PI components from: {p1_path}")
                load_pi_data_from_dict(registry, p1_data)
        except Exception as e:
            debug_print(f"Error loading P1 PI data: {e}")
    else:
        debug_print(f"P1 PI components file not found: {p1_path}")
    
    # Load P2 components
    p2_path = os.path.join(pi_folder, 'P2_PI_Components.json')
    if os.path.exists(p2_path):
        try:
            with open(p2_path, 'r') as f:
                p2_data = json.load(f)
                debug_print(f"Loading P2 PI components from: {p2_path}")
                load_pi_data_from_dict(registry, p2_data)
        except Exception as e:
            debug_print(f"Error loading P2 PI data: {e}")
    else:
        debug_print(f"P2 PI components file not found: {p2_path}")
    
    # Load P3 components
    p3_path = os.path.join(pi_folder, 'P3_PI_Components.json')
    if os.path.exists(p3_path):
        try:
            with open(p3_path, 'r') as f:
                p3_data = json.load(f)
                debug_print(f"Loading P3 PI components from: {p3_path}")
                load_pi_data_from_dict(registry, p3_data)
        except Exception as e:
            debug_print(f"Error loading P3 PI data: {e}")
    else:
        debug_print(f"P3 PI components file not found: {p3_path}")
    
    # Load P4 components
    p4_path = os.path.join(pi_folder, 'P4_PI_Components.json')
    if os.path.exists(p4_path):
        try:
            with open(p4_path, 'r') as f:
                p4_data = json.load(f)
                debug_print(f"Loading P4 PI components from: {p4_path}")
                load_pi_data_from_dict(registry, p4_data)
        except Exception as e:
            debug_print(f"Error loading P4 PI data: {e}")
    else:
        debug_print(f"P4 PI components file not found: {p4_path}")
    
    debug_print("Finished loading all PI component files")

def load_pi_data_from_dict(registry: ModuleRegistry, pi_data: dict):
    """
    Process PI data from a dictionary and add to registry
    
    Args:
        registry: The module registry to populate
        pi_data: Dictionary containing PI component data
    """
    # Initialize counters for each PI level
    p0_count = 0
    p1_count = 0
    p2_count = 0
    p3_count = 0
    p4_count = 0
    
    # Process P0 materials (raw materials)
    if 'P0_Raw_Materials' in pi_data:
        for material in pi_data['P0_Raw_Materials']:
            name = material['name']
            
            # Create a standardized details string
            details = f"P0 Raw Material: {name}\n\n"
            details += f"Harvestable from: {', '.join(material.get('harvestable_planet_types', []))}\n\n"
            details += f"Refines to: {material.get('refines_to_P1', 'Unknown')}\n"
            
            # Create PiMaterialModule
            pi_material = PiMaterialModule(
                name=name.lower().replace(' ', '_'),
                display_name=name,
                requirements={},  # P0 materials have no requirements
                details=details,
                pi_level="P0",
                planet_types=material.get('harvestable_planet_types', []),
                outputs={material.get('refines_to_P1', ''): 1}
            )
            
            # Register in registry
            registry.register_pi_material(pi_material)
            p0_count += 1
    
    # Process P1 materials (processed materials)
    if 'P1_Processed_Materials' in pi_data:
        for material in pi_data['P1_Processed_Materials']:
            name = material['name']
            
            # Create a standardized details string
            details = f"P1 Processed Material: {name}\n\n"
            details += f"Produced from: {material.get('produced_from_P0', 'Unknown')}\n\n"
            if 'example_uses' in material and material['example_uses'] != "None known":
                details += f"Uses: {material['example_uses']}\n\n"
            if 'inputs_for_P2' in material:
                details += "Used in P2 Materials:\n"
                for output in material['inputs_for_P2']:
                    details += f"- {output}\n"
            
            # Create PiMaterialModule
            pi_material = PiMaterialModule(
                name=name.lower().replace(' ', '_'),
                display_name=name,
                requirements={material.get('produced_from_P0', ''): 3000},  # P1 standard requirement
                details=details,
                pi_level="P1"
            )
            
            # Register in registry
            registry.register_pi_material(pi_material)
            p1_count += 1
    
    # Process P2 materials (refined commodities)
    if 'P2_Refined_Commodities' in pi_data:
        for material in pi_data['P2_Refined_Commodities']:
            name = material['name']
            
            # Create a standardized details string
            details = f"P2 Refined Commodity: {name}\n\n"
            if 'inputs' in material:
                details += "Input Requirements:\n"
                for input_mat in material['inputs']:
                    details += f"- {input_mat}: 40\n"  # P2 standard requirement
            details += "\n"
            if 'example_uses' in material and material['example_uses'] != "(No direct use)":
                details += f"Uses: {material['example_uses']}\n\n"
            if 'inputs_for_P3' in material:
                details += "Used in P3 Materials:\n"
                for output in material['inputs_for_P3']:
                    details += f"- {output}\n"
            
            # Create input requirements dictionary
            requirements = {}
            if 'inputs' in material:
                for input_mat in material['inputs']:
                    requirements[input_mat] = 40  # P2 standard requirement
            
            # Create PiMaterialModule
            pi_material = PiMaterialModule(
                name=name.lower().replace(' ', '_'),
                display_name=name,
                requirements=requirements,
                details=details,
                pi_level="P2"
            )
            
            # Register in registry
            registry.register_pi_material(pi_material)
            p2_count += 1
    
    # Process P3 materials (specialized commodities)
    if 'P3_Specialized_Commodities' in pi_data:
        for material in pi_data['P3_Specialized_Commodities']:
            name = material['name']
            
            # Create a standardized details string
            details = f"P3 Specialized Commodity: {name}\n\n"
            if 'inputs' in material:
                details += "Input Requirements:\n"
                for input_mat in material['inputs']:
                    details += f"- {input_mat}: 10\n"  # P3 standard requirement
            details += "\n"
            if 'example_uses' in material and material['example_uses'] != "(No direct use)":
                details += f"Uses: {material['example_uses']}\n\n"
            if 'inputs_for_P4' in material:
                details += "Used in P4 Materials:\n"
                for output in material['inputs_for_P4']:
                    details += f"- {output}\n"
            
            # Create input requirements dictionary
            requirements = {}
            if 'inputs' in material:
                for input_mat in material['inputs']:
                    requirements[input_mat] = 10  # P3 standard requirement
            
            # Create PiMaterialModule
            pi_material = PiMaterialModule(
                name=name.lower().replace(' ', '_'),
                display_name=name,
                requirements=requirements,
                details=details,
                pi_level="P3"
            )
            
            # Register in registry
            registry.register_pi_material(pi_material)
            p3_count += 1
    
    # Process P4 materials (advanced commodities)
    if 'P4_Advanced_Commodities' in pi_data:
        for material in pi_data['P4_Advanced_Commodities']:
            name = material['name']
            
            # Create a standardized details string
            details = f"P4 Advanced Commodity: {name}\n\n"
            if 'inputs' in material:
                details += "Input Requirements:\n"
                for input_mat in material['inputs']:
                    details += f"- {input_mat}: 6\n"  # P4 standard requirement
            details += "\n"
            if 'ultimate_use' in material:
                details += f"Uses: {material['ultimate_use']}\n"
            
            # Create input requirements dictionary
            requirements = {}
            if 'inputs' in material:
                for input_mat in material['inputs']:
                    requirements[input_mat] = 6  # P4 standard requirement
            
            # Create PiMaterialModule
            pi_material = PiMaterialModule(
                name=name.lower().replace(' ', '_'),
                display_name=name,
                requirements=requirements,
                details=details,
                pi_level="P4"
            )
            
            # Register in registry
            registry.register_pi_material(pi_material)
            p4_count += 1
    
    # Log the total number of PI materials loaded
    debug_print(f"Registered PI materials: P0: {p0_count}, P1: {p1_count}, P2: {p2_count}, P3: {p3_count}, P4: {p4_count}")

def load_ore_data(base_path: str):
    """
    Load ore data from ore.json
    
    Args:
        base_path: Base path of the application
        
    Returns:
        dict: Dictionary of ore data
    """
    import json
    
    ore_data_path = os.path.join(base_path, 'data', 'ore.json')
    
    try:
        with open(ore_data_path, 'r') as f:
            ore_json = json.load(f)
            
        # Convert the structured JSON into a flat dictionary for compatibility with existing code
        flat_ore_data = {}
        for sec_level, ores in ore_json['ores'].items():
            for ore_key, ore_info in ores.items():
                flat_ore_data[ore_info['display_name']] = ore_info['yields']
                
        return flat_ore_data
        
    except (FileNotFoundError, json.JSONDecodeError) as e:
        debug_print(f"Error loading ore data: {e}")
        # Fallback to the original ore_data if JSON loading fails
        try:
            import importlib.util
            old_ore_data_path = os.path.join(base_path, 'ore_data.py')
            spec = importlib.util.spec_from_file_location('ore_data', old_ore_data_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            debug_print("Falling back to original ore_data.py")
            return module.ore_data
        except Exception as e2:
            debug_print(f"Fatal error, could not load ore data: {e2}")
            return {}
