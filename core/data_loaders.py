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

from core.module_registry import ModuleRegistry
from core.models import ShipModule, CapitalShipModule, ComponentModule, PiMaterialModule

def load_ships(registry: ModuleRegistry, base_path: str):
    """
    Load ship data from JSON files into the registry
    
    Args:
        registry: The module registry to populate
        base_path: Base path of the application
    """
    ships_folder = os.path.join(base_path, 'core', 'data', 'ships')
    
    # Debug output
    debug_print(f"Loading ships from folder: {ships_folder}")
    
    if not os.path.exists(ships_folder):
        debug_print(f"Ships folder not found: {ships_folder}")
        return
    
    ship_files = glob.glob(os.path.join(ships_folder, "*.json"))
    debug_print(f"Found {len(ship_files)} ship files")
    
    for ship_file in ship_files:
        try:
            with open(ship_file, 'r') as f:
                ships_data = json.load(f)
                debug_print(f"Loading ships from file: {ship_file}")
                
                # Check if the file uses the array format with a "ships" key
                if "ships" in ships_data and isinstance(ships_data["ships"], list):
                    # Extract filename to determine faction
                    filename = os.path.basename(ship_file)
                    faction = filename.split('_')[1].split('.')[0] if '_' in filename else "unknown"
                    debug_print(f"Processing array-style ship data for faction: {faction}")
                    
                    # Process each ship in the array
                    for ship_data in ships_data["ships"]:
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
                        except Exception as e:
                            debug_print(f"Error adding ship {ship_name}: {e}")
                else:
                    # Each file might have a faction key
                    for faction, ships in ships_data.items():
                        for ship_name, ship_data in ships.items():
                            try:
                                # Safe fallback for display name
                                display_name = ship_data.get('display_name', ship_name)
                                
                                # Load ship into registry
                                registry.ships[ship_name] = ShipModule(
                                    name=ship_name,
                                    display_name=display_name,
                                    requirements=ship_data.get('requirements', {}),
                                    details=ship_data.get('details', ''),
                                    faction=faction,
                                    ship_type=ship_data.get('ship_type', 'Unknown'),
                                    owned_status=False  # Default to unowned
                                )
                                debug_print(f"Added ship: {display_name} from faction {faction}")
                            except Exception as e:
                                debug_print(f"Error loading ship {ship_name}: {e}")
        except Exception as e:
            debug_print(f"Error loading ship file {ship_file}: {e}")

def load_components(registry: ModuleRegistry, base_path: str):
    """
    Load component data from JSON files into the registry
    
    Args:
        registry: The module registry to populate
        base_path: Base path of the application
    """
    components_folder = os.path.join(base_path, 'core', 'data', 'components')
    debug_print(f"Loading components from folder: {components_folder}")
    
    if not os.path.exists(components_folder):
        debug_print(f"Components folder not found: {components_folder}")
        return
    
    component_files = glob.glob(os.path.join(components_folder, "*.json"))
    debug_print(f"Found {len(component_files)} component files")
    
    for component_file in component_files:
        try:
            with open(component_file, 'r') as f:
                components_data = json.load(f)
                debug_print(f"Loading components from file: {component_file}")
                
                # Check if we're dealing with capital components
                is_capital = 'capital' in os.path.basename(component_file).lower()
                
                # Handle possible nested structure where components are under a key
                if is_capital and 'capital_components' in components_data:
                    components_data = components_data['capital_components']
                elif not is_capital and 'components' in components_data:
                    components_data = components_data['components']
                
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
                            debug_print(f"Added capital component: {display_name}")
                        else:
                            registry.components[component_name] = component
                            debug_print(f"Added component: {display_name}")
                    except Exception as e:
                        debug_print(f"Error loading component {component_name}: {e}")
        except Exception as e:
            debug_print(f"Error loading component file {component_file}: {e}")

def load_capital_ships(registry: ModuleRegistry, base_path: str):
    """
    Load capital ship data from JSON files into the registry
    
    Args:
        registry: The module registry to populate
        base_path: Base path of the application
    """
    capital_ships_folder = os.path.join(base_path, 'core', 'data', 'capital_ships')
    debug_print(f"Loading capital ships from folder: {capital_ships_folder}")
    
    if not os.path.exists(capital_ships_folder):
        debug_print(f"Capital ships folder not found: {capital_ships_folder}")
        return
    
    ship_files = glob.glob(os.path.join(capital_ships_folder, "*.json"))
    debug_print(f"Found {len(ship_files)} capital ship files")
    
    for ship_file in ship_files:
        try:
            with open(ship_file, 'r') as f:
                ships_data = json.load(f)
                debug_print(f"Loading capital ships from file: {ship_file}")
                
                # Each file might have a faction key
                for faction, ships in ships_data.items():
                    for ship_name, ship_data in ships.items():
                        try:
                            # Safe fallback for display name
                            display_name = ship_data.get('display_name', ship_name)
                            
                            # Load ship into registry
                            registry.capital_ships[ship_name] = CapitalShipModule(
                                name=ship_name,
                                display_name=display_name,
                                components=ship_data.get('components', {}),
                                details=ship_data.get('details', ''),
                                faction=faction,
                                ship_type=ship_data.get('ship_type', 'Capital'),
                                owned_status=False  # Default to unowned
                            )
                            debug_print(f"Added capital ship: {display_name} from faction {faction}")
                        except Exception as e:
                            debug_print(f"Error loading capital ship {ship_name}: {e}")
        except Exception as e:
            debug_print(f"Error loading capital ship file {ship_file}: {e}")

def load_pi_data(registry: ModuleRegistry, base_path: str):
    """
    Load PI data from JSON files in the PI folder
    
    Args:
        registry: The module registry to populate
        base_path: Base path of the application
    """
    pi_folder = os.path.join(base_path, 'core', 'data', 'PI')
    
    # If the PI folder doesn't exist, fallback to the legacy file
    if not os.path.exists(pi_folder):
        legacy_pi_path = os.path.join(base_path, 'core', 'data', 'PI_Components.json')
        debug_print(f"PI folder not found, trying legacy path: {legacy_pi_path}")
        
        try:
            with open(legacy_pi_path, 'r') as f:
                pi_data = json.load(f)
                debug_print(f"Loading PI data from legacy file: {legacy_pi_path}")
                load_pi_data_from_dict(registry, pi_data)
        except Exception as e:
            debug_print(f"Error loading legacy PI data: {e}")
        return
    
    # Process each PI level file (P0, P1, P2, P3, P4)
    pi_files = glob.glob(os.path.join(pi_folder, "*.json"))
    debug_print(f"Found {len(pi_files)} PI data files")
    
    for pi_file in pi_files:
        try:
            with open(pi_file, 'r', encoding='utf-8') as f:
                pi_data = json.load(f)
                debug_print(f"Loading PI data from file: {pi_file}")
                
                # Extract PI level from filename (P0, P1, P2, P3, P4)
                filename = os.path.basename(pi_file)
                pi_level = filename.split('_')[0] if '_' in filename else 'unknown'
                
                # PI files use a category key with an array of materials
                for category_name, materials_list in pi_data.items():
                    if isinstance(materials_list, list):
                        # Process array-style PI data
                        for material_data in materials_list:
                            try:
                                material_name = material_data.get('name', 'Unknown Material')
                                
                                registry.pi_materials[material_name] = PiMaterialModule(
                                    name=material_name,
                                    display_name=material_name,
                                    pi_level=pi_level,
                                    requirements={},  # Empty requirements for P0 materials
                                    details=material_data.get('description', ''),
                                    planet_types=material_data.get('harvestable_planet_types', []),
                                    outputs={'refines_to': material_data.get('refines_to_P1', '')}
                                )
                                debug_print(f"Added PI material: {material_name} (Level: {pi_level})")
                            except Exception as e:
                                debug_print(f"Error adding PI material {material_name}: {e}")
        except Exception as e:
            debug_print(f"Error loading PI file {pi_file}: {e}")

def load_pi_data_from_dict(registry: ModuleRegistry, pi_data: Dict[str, Any]):
    """
    Load PI data from a dictionary
    
    Args:
        registry: The module registry to populate
        pi_data: Dictionary containing PI data
    """
    try:
        # Process each PI level
        for pi_level, materials in pi_data.items():
            debug_print(f"Loading PI level: {pi_level}")
            
            # Clean up pi_level to match expected format (p0, p1, p2, etc.)
            clean_level = pi_level.lower().replace('_materials', '')
            
            # Add to registry.pi_data
            if clean_level not in registry.pi_data:
                registry.pi_data[clean_level] = {}
            
            # Process each material in this level
            for material_name, material_data in materials.items():
                try:
                    # Add to registry
                    registry.pi_materials[material_name] = PiMaterialModule(
                        name=material_name,
                        display_name=material_data.get('display_name', material_name),
                        requirements=material_data.get('requirements', {}),
                        details=material_data.get('details', ''),
                        pi_level=clean_level,
                        planet_types=material_data.get('planet_types', []),
                        outputs=material_data.get('outputs', {})
                    )
                    
                    # Also track in PI data by level
                    registry.pi_data[clean_level][material_name] = material_data
                    
                    debug_print(f"Added PI material: {material_name} (Level: {clean_level})")
                except Exception as e:
                    debug_print(f"Error loading PI material {material_name}: {e}")
    except Exception as e:
        debug_print(f"Error in load_pi_data_from_dict: {e}")

def load_ore_data(registry: ModuleRegistry, base_path: str):
    """
    Load ore data from JSON files
    
    Args:
        registry: The module registry to populate
        base_path: Base path of the application
    """
    # Try multiple possible ore data file names
    possible_ore_paths = [
        os.path.join(base_path, 'core', 'data', 'ores.json'),
        os.path.join(base_path, 'core', 'data', 'ore.json')
    ]
    
    for ore_path in possible_ore_paths:
        debug_print(f"Trying to load ore data from: {ore_path}")
        
        if os.path.exists(ore_path):
            try:
                with open(ore_path, 'r', encoding='utf-8') as f:
                    ore_data = json.load(f)
                    debug_print(f"Loaded ore data with {len(ore_data)} entries")
                    registry.ores = ore_data
                    return
            except Exception as e:
                debug_print(f"Error loading ore data from {ore_path}: {e}")
    
    debug_print("Could not find any ore data files")
