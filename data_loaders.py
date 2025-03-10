"""
Data loaders for EVE Production Calculator

This file contains functions for loading data from JSON files into the module registry
"""
import os
import json
import importlib.util
from typing import Dict, List, Any, Optional, Set, Tuple

from module_registry import ModuleRegistry
from models import ShipModule, CapitalShipModule, ComponentModule, PiMaterialModule

def load_ships(registry: ModuleRegistry, base_path: str):
    """
    Load all ship data from JSON file and register in the ModuleRegistry
    
    Args:
        registry: The module registry to populate
        base_path: Base path of the application
    """
    ships_path = os.path.join(base_path, 'data', 'ships.json')
    
    try:
        with open(ships_path, 'r') as f:
            ships_data = json.load(f)
        
        # Track loaded ships count
        ship_count = 0
        capital_ship_count = 0
        
        # Load regular ships
        for faction, faction_data in ships_data.items():
            if faction == "capital_ships":
                # Handle capital ships separately
                process_capital_ships(registry, faction_data)
                capital_ship_count = len(registry.get_all_capital_ships())
            else:
                process_ship_category(registry, faction, faction_data)
                ship_count = len(registry.get_all_ships())
        
        print(f"Loaded {ship_count} ships and {capital_ship_count} capital ships")
            
    except Exception as e:
        print(f"Error loading ships from JSON: {e}")

def process_ship_category(registry: ModuleRegistry, parent_key: str, category_data: Dict):
    """
    Process a category of ships (e.g., faction or ship class)
    
    Args:
        registry: The module registry to populate
        parent_key: Key of the parent category (e.g., faction name)
        category_data: Data for the category
    """
    if isinstance(category_data, dict):
        # Check if this entry has display_name and requirements (direct ship entry)
        if "display_name" in category_data and "requirements" in category_data:
            # This is a direct ship entry
            ship = ShipModule(
                name=parent_key,
                display_name=category_data.get("display_name", parent_key),
                requirements=category_data.get("requirements", {}),
                details=category_data.get("details", ""),
                faction=category_data.get("faction", ""),
                ship_type=category_data.get("ship_type", ""),
                owned_status=False
            )
            registry.register_ship(ship)
        else:
            # This is a category, process its children
            for key, value in category_data.items():
                process_ship_category(registry, key, value)

def process_capital_ships(registry: ModuleRegistry, capital_ships_data: Dict):
    """
    Process capital ships specifically
    
    Args:
        registry: The module registry to populate
        capital_ships_data: Data for capital ships
    """
    if isinstance(capital_ships_data, dict):
        for category, ships in capital_ships_data.items():
            if isinstance(ships, dict):
                for ship_key, ship_data in ships.items():
                    if "display_name" in ship_data and "requirements" in ship_data:
                        # Create and register the capital ship
                        capital_ship = CapitalShipModule(
                            name=ship_key,
                            display_name=ship_data.get('display_name', ship_key),
                            requirements=ship_data.get('requirements', {}),
                            details=ship_data.get('details', ''),
                            faction=ship_data.get('faction', ''),
                            ship_type=ship_data.get('ship_type', ''),
                            capital_component_data=ship_data.get('capital_components', {}),
                            owned_status=False
                        )
                        registry.register_capital_ship(capital_ship)

def load_components(registry: ModuleRegistry, base_path: str):
    """
    Load components from JSON files and Python modules
    
    Args:
        registry: The module registry to populate
        base_path: Base path of the application
    """
    # First try to load from JSON file (for capital components)
    components_path = os.path.join(base_path, 'data', 'capitalcomponents.json')
    
    try:
        if os.path.exists(components_path):
            with open(components_path, 'r') as f:
                components_data = json.load(f)
            
            for component_name, component_data in components_data.items():
                component = ComponentModule(
                    name=component_name,
                    display_name=component_data.get("display_name", component_name),
                    requirements=component_data.get("requirements", {}),
                    details=component_data.get("details", ""),
                    owned_status=False
                )
                registry.register_component(component)
                
            print(f"Loaded {len(components_data)} capital components from JSON")
    except Exception as e:
        print(f"Error loading components from JSON: {e}")
    
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
                            owned_status=False
                        )
                        
                        # Register component
                        registry.register_component(component)
                        components_loaded += 1
                except Exception as e:
                    print(f"Error loading component module {module_path}: {e}")
        
        print(f"Loaded {components_loaded} components from Python modules")

def load_pi_data(registry: ModuleRegistry, base_path: str):
    """
    Load PI data from JSON file
    
    Args:
        registry: The module registry to populate
        base_path: Base path of the application
    """
    pi_data_path = os.path.join(base_path, 'data', 'PI_Components.json')
    
    try:
        with open(pi_data_path, 'r') as f:
            pi_data = json.load(f)
        
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
        
        print(f"Loaded PI materials: P0={len([m for m in registry.pi_materials.values() if m.pi_level == 'P0'])}, " + 
              f"P1={len([m for m in registry.pi_materials.values() if m.pi_level == 'P1'])}, " +
              f"P2={len([m for m in registry.pi_materials.values() if m.pi_level == 'P2'])}, " +
              f"P3={len([m for m in registry.pi_materials.values() if m.pi_level == 'P3'])}, " +
              f"P4={len([m for m in registry.pi_materials.values() if m.pi_level == 'P4'])}")
        
    except Exception as e:
        print(f"Error loading PI data: {e}")

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
        print(f"Error loading ore data: {e}")
        # Fallback to the original ore_data if JSON loading fails
        try:
            import importlib.util
            old_ore_data_path = os.path.join(base_path, 'ore_data.py')
            spec = importlib.util.spec_from_file_location('ore_data', old_ore_data_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print("Falling back to original ore_data.py")
            return module.ore_data
        except Exception as e2:
            print(f"Fatal error, could not load ore data: {e2}")
            return {}
