"""
Data loaders for EVE Production Calculator

This file contains functions for loading data from JSON files into the module registry
"""
import os
import json
import importlib.util
import sys
from core.utils.debug import debug_print
from typing import Dict, List, Any, Optional, Set, Tuple
import glob
from pathlib import Path

from core.module_registry import ModuleRegistry
from core.models import ShipModule, CapitalShipModule, ComponentModule, PiMaterialModule

# Cache for loaded JSON data to avoid repeated file reads
_json_cache = {}

def _load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Load a JSON file with caching to avoid repeated file reads
    
    Args:
        file_path: Path to the JSON file to load
    
    Returns:
        The loaded JSON data as a dictionary
    """
    if file_path in _json_cache:
        return _json_cache[file_path]
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            _json_cache[file_path] = data
            return data
    except json.JSONDecodeError as e:
        debug_print(f"JSON parsing error in {file_path}: {str(e)}")
        return {}
    except Exception as e:
        debug_print(f"Error loading file {file_path}: {str(e)}")
        return {}

def _process_array_ships(registry: ModuleRegistry, ships_data: List[Dict], faction: str) -> int:
    """
    Process ships data in array format
    
    Args:
        registry: The module registry to populate
        ships_data: List of ship data dictionaries
        faction: The faction of the ships
        
    Returns:
        Number of ships loaded
    """
    ships_loaded = 0
    for ship_data in ships_data:
        try:
            ship_name = ship_data.get("name", "Unknown Ship")
            
            # Create ship module
            registry.ships[ship_name] = ShipModule(
                name=ship_name,
                display_name=ship_name,
                requirements=ship_data.get("materials", {}),
                details=ship_data.get("description", ""),
                faction=ship_data.get("faction", faction),
                ship_type=ship_data.get("type", "Unknown"),
                owned_status=False  # Default to unowned
            )
            debug_print(f"Added ship: {ship_name} from faction {faction}")
            ships_loaded += 1
        except Exception as e:
            debug_print(f"Error adding ship {ship_name}: {e}")
    
    return ships_loaded

def _add_ship_to_registry(registry: ModuleRegistry, ship_name: str, ship_data: Dict, faction: str, category: str = None) -> bool:
    """
    Add a ship to the module registry
    
    Args:
        registry: The module registry to populate
        ship_name: Name of the ship
        ship_data: Ship data dictionary
        faction: The faction of the ship
        category: Optional category for the ship
        
    Returns:
        True if ship was added successfully, False otherwise
    """
    # Skip if not a proper ship entry (must have requirements)
    if not isinstance(ship_data, dict) or 'requirements' not in ship_data:
        return False
        
    try:
        # Safe fallback for display name
        display_name = ship_data.get('display_name', ship_name)
        
        # Determine ship type
        if category:
            ship_type = ship_data.get('ship_type', category.rstrip('s').capitalize())
        else:
            ship_type = ship_data.get('ship_type', 'Unknown')
        
        # Special handling for Bowhead Freighter - it should always be ORE faction
        if ship_name.lower() == "bowhead" or display_name.lower() == "bowhead freighter":
            debug_print(f"Special handling for Bowhead Freighter: setting faction to ORE")
            ship_faction = "ORE"
        else:
            # Get faction from ship data if available, otherwise use file-based faction
            ship_faction = ship_data.get('faction', faction)
        
        # Load ship into registry
        if faction == "capital_ships":
            registry.capital_ships[ship_name] = CapitalShipModule(
                name=ship_name,
                display_name=display_name,
                requirements=ship_data.get('requirements', {}),
                details=ship_data.get('details', ''),
                faction=ship_faction,
                ship_type=ship_type,
                owned_status=False  # Default to unowned
            )
        else:
            registry.ships[ship_name] = ShipModule(
                name=ship_name,
                display_name=display_name,
                requirements=ship_data.get('requirements', {}),
                details=ship_data.get('details', ''),
                faction=ship_faction,
                ship_type=ship_type,
                owned_status=False  # Default to unowned
            )
            
        debug_print(f"Added {'capital ' if faction == 'capital_ships' else ''}ship: {display_name} from faction {ship_faction}")
        return True
    except Exception as e:
        debug_print(f"Error adding ship {ship_name}: {e}")
        return False

def _process_hierarchical_ship_data(registry: ModuleRegistry, faction: str, categories: Dict, metadata_keys: List[str]) -> int:
    """
    Process hierarchical ship data
    
    Args:
        registry: The module registry to populate
        faction: The faction of the ships
        categories: Dictionary of ship categories
        metadata_keys: Keys to skip as they are metadata, not ships
        
    Returns:
        Number of ships loaded
    """
    ships_loaded = 0
    
    # Skip metadata entries
    if faction in metadata_keys:
        return 0
        
    # Handle legacy format where ships might be directly under faction
    if isinstance(categories, dict) and 'display_name' in categories:
        if _add_ship_to_registry(registry, faction, categories, faction):
            ships_loaded += 1
        return ships_loaded
    
    # Check if this is a category dict (like frigates, cruisers, etc.)
    if not isinstance(categories, dict):
        return 0
        
    for category, tech_levels in categories.items():
        # Skip metadata entries
        if category in metadata_keys:
            continue
            
        # Handle case where ships might be directly under category
        if isinstance(tech_levels, dict) and 'display_name' in tech_levels:
            if _add_ship_to_registry(registry, category, tech_levels, faction):
                ships_loaded += 1
            continue
            
        # Check if this is a tech level dict (like tech1, tech2, etc.)
        if not isinstance(tech_levels, dict):
            continue
            
        for tech_level, ships in tech_levels.items():
            # Skip metadata entries
            if tech_level in metadata_keys:
                continue
                
            # Handle case where ships might be directly under tech level
            if isinstance(ships, dict) and 'display_name' in ships:
                if _add_ship_to_registry(registry, tech_level, ships, faction, category):
                    ships_loaded += 1
                continue
                
            # Finally, iterate through the actual ships
            if not isinstance(ships, dict):
                continue
                
            for ship_name, ship_data in ships.items():
                # Skip metadata entries
                if ship_name in metadata_keys:
                    continue
                    
                if _add_ship_to_registry(registry, ship_name, ship_data, faction, category):
                    ships_loaded += 1
    
    return ships_loaded

def load_ships(registry: ModuleRegistry, base_path: str):
    """
    Load ship data from JSON files into the registry
    
    Args:
        registry: The module registry to populate
        base_path: Base path of the application
    """
    ships_folder = os.path.join(base_path, 'core', 'data', 'ships')
    
    debug_print(f"Loading ships from folder: {ships_folder}")
    
    if not os.path.exists(ships_folder):
        debug_print(f"Ships folder not found: {ships_folder}")
        return
    
    ship_files = glob.glob(os.path.join(ships_folder, "*.json"))
    debug_print(f"Found {len(ship_files)} ship files")
    
    ships_loaded = 0
    
    # Define metadata keys to skip - these are not actual ships
    metadata_keys = [
        "requirements", "specifications", "tech1", "tech2", 
        "capital_component_data", "navy_issue", "details", 
        "owned_status", "materials", "inputs", "outputs"
    ]
    
    for ship_file in ship_files:
        try:
            ships_data = _load_json_file(ship_file)
            filename = os.path.basename(ship_file)
            debug_print(f"Loading ships from file: {filename}")
            
            # Check if the file uses the array format with a "ships" key
            if "ships" in ships_data and isinstance(ships_data["ships"], list):
                # Extract filename to determine faction
                faction = filename.split('_')[1].split('.')[0] if '_' in filename else "unknown"
                debug_print(f"Processing array-style ship data for faction: {faction}")
                
                # Process each ship in the array
                ships_loaded += _process_array_ships(registry, ships_data["ships"], faction)
            else:
                # Each file might have a faction key, and ships are nested under categories and tech levels
                for faction, categories in ships_data.items():
                    ships_loaded += _process_hierarchical_ship_data(registry, faction, categories, metadata_keys)
        except Exception as e:
            debug_print(f"Error loading ship file {os.path.basename(ship_file)}: {e}")
    
    debug_print(f"Loaded {ships_loaded} ships from {len(ship_files)} files")

def load_components(registry: ModuleRegistry, base_path: str):
    """
    Load component data from JSON files into the registry
    
    Args:
        registry: The module registry to populate
        base_path: Base path of the application
    """
    debug_print("*** STARTING COMPONENT LOADING ***")
    
    # Define paths for component files
    data_path = os.path.join(base_path, 'core', 'data')
    components_folder = os.path.join(data_path, 'components')
    legacy_component_file = os.path.join(data_path, 'components.json')
    legacy_capital_file = os.path.join(data_path, 'capitalcomponents.json')
    
    component_files = []
    
    # Get component files from the components folder if it exists
    if os.path.exists(components_folder):
        component_files.extend(glob.glob(os.path.join(components_folder, "*.json")))
    
    # Add legacy files if they exist
    if os.path.exists(legacy_component_file):
        component_files.append(legacy_component_file)
    
    if os.path.exists(legacy_capital_file):
        component_files.append(legacy_capital_file)
    
    if not component_files:
        debug_print("No component files found.")
        return
    
    debug_print(f"Found {len(component_files)} component files to process")
    
    # Track loaded component counts
    total_regular = 0
    total_capital = 0
    
    for component_file in component_files:
        filename = os.path.basename(component_file)
        
        try:
            components_data = _load_json_file(component_file)
            
            # Determine if this is a capital component file
            # Only files with 'capital' in the name but NOT 'tech2' are treated as capital components
            is_capital = 'capital' in filename.lower() and 'tech2' not in filename.lower()
            
            # Extract nested component data if necessary
            if is_capital and 'capital_components' in components_data:
                components_data = components_data['capital_components']
            elif not is_capital and 'components' in components_data:
                components_data = components_data['components']
            
            file_components = 0
            
            for component_name, component_data in components_data.items():
                try:
                    # Safe fallback for display name
                    display_name = component_data.get('display_name', component_name)
                    
                    # Create component module
                    component = ComponentModule(
                        name=component_name,
                        display_name=display_name,
                        requirements=component_data.get('requirements', {}),
                        details=component_data.get('details', ''),
                        owned_status=False  # Default to unowned
                    )
                    
                    # Add to appropriate registry
                    if is_capital:
                        registry.capital_components[component_name] = component
                        total_capital += 1
                    else:
                        registry.components[component_name] = component
                        total_regular += 1
                    
                    file_components += 1
                except Exception as e:
                    debug_print(f"Error loading component {component_name}: {str(e)}")
            
            debug_print(f"Loaded {file_components} {'capital' if is_capital else 'regular'} components from {filename}")
            
        except Exception as e:
            debug_print(f"Error processing component file {filename}: {str(e)}")
    
    debug_print(f"Component loading complete: {total_regular} regular and {total_capital} capital components loaded")

def load_pi_data(registry: ModuleRegistry, base_path: str):
    """
    Load PI data from JSON files in the PI folder
    
    Args:
        registry: The module registry to populate
        base_path: Base path of the application
    """
    pi_folder = os.path.join(base_path, 'core', 'data', 'PI')
    
    if not os.path.exists(pi_folder):
        debug_print(f"PI folder not found: {pi_folder}")
        return
    
    pi_files = glob.glob(os.path.join(pi_folder, "*.json"))
    
    if not pi_files:
        debug_print("No PI files found.")
        return
    
    combined_pi_data = {
        'p0_materials': {},
        'p1_materials': {},
        'p2_materials': {},
        'p3_materials': {},
        'p4_materials': {}
    }
    
    for pi_file in pi_files:
        try:
            pi_data = _load_json_file(pi_file)
            
            # Merge data from this file into combined data
            for tier_key in combined_pi_data.keys():
                if tier_key in pi_data:
                    combined_pi_data[tier_key].update(pi_data[tier_key])
        except Exception as e:
            debug_print(f"Error loading PI file {os.path.basename(pi_file)}: {e}")
    
    # Load the combined data into the registry
    load_pi_data_from_dict(registry, combined_pi_data)

def load_pi_data_from_dict(registry: ModuleRegistry, pi_data: Dict[str, Any]):
    """
    Load PI data from a dictionary
    
    Args:
        registry: The module registry to populate
        pi_data: Dictionary containing PI data
    """
    # Store raw PI data in registry
    for tier_key, materials in pi_data.items():
        registry.pi_data[tier_key] = materials
    
    # Extract all PI materials into a flat dictionary for easy access
    for tier_key, materials in pi_data.items():
        for material_name, material_data in materials.items():
            try:
                # Get the tier from the key (p0, p1, etc.)
                tier = tier_key.replace('_materials', '')
                
                # Create PI material module
                pi_material = PiMaterialModule(
                    name=material_name,
                    display_name=material_data.get('display_name', material_name),
                    pi_level=tier,
                    requirements=material_data.get('inputs', {}),
                    details=material_data.get('details', '')
                )
                
                # Add to PI materials registry
                registry.pi_materials[material_name] = pi_material
            except Exception as e:
                debug_print(f"Error loading PI material {material_name}: {e}")

def load_ore_data(registry: ModuleRegistry, base_path: str):
    """
    Load ore data from JSON files
    
    Args:
        registry: The module registry to populate
        base_path: Base path of the application
    """
    ore_file = os.path.join(base_path, 'core', 'data', 'ore.json')
    
    if not os.path.exists(ore_file):
        debug_print(f"Ore file not found: {ore_file}")
        return
    
    try:
        ore_data = _load_json_file(ore_file)
        
        # Store ore data directly in registry
        registry.ores = ore_data
        
        debug_print(f"Loaded ore data: {len(ore_data)} ore types")
    except Exception as e:
        debug_print(f"Error loading ore data: {e}")
