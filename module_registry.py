"""
Module Registry for EVE Production Calculator

This system manages all data modules (ships, components, etc.) with a unified interface
"""
import os
import json
import importlib.util
from typing import Dict, List, Any, Optional, Set, Tuple

class ShipModule:
    """Representation of a ship with all its attributes and requirements"""
    def __init__(self, 
                 name: str, 
                 display_name: str, 
                 requirements: Dict[str, int], 
                 details: str, 
                 faction: Optional[str] = None, 
                 ship_type: Optional[str] = None, 
                 owned_status: Optional[str] = None):
        self.name = name
        self.display_name = display_name
        self.requirements = requirements
        self.details = details
        self.faction = faction
        self.ship_type = ship_type
        self.owned_status = owned_status
        self.module_type = 'ship'  # Always 'ship' for this class

class CapitalShipModule:
    """Representation of a capital ship with all its attributes and components"""
    def __init__(self, 
                 name: str, 
                 display_name: str, 
                 requirements: Dict[str, int], 
                 details: str,
                 capital_component_data: Dict[str, Dict[str, Any]] = None,
                 owned_status: Optional[str] = None):
        self.name = name
        self.display_name = display_name
        self.requirements = requirements
        self.details = details
        self.capital_component_data = capital_component_data or {}
        self.owned_status = owned_status
        self.module_type = 'capital_ship'  # Always 'capital_ship' for this class

class ComponentModule:
    """Representation of a component with all its attributes and requirements"""
    def __init__(self, 
                 name: str, 
                 display_name: str, 
                 requirements: Dict[str, int], 
                 details: str,
                 owned_status: Optional[str] = None):
        self.name = name
        self.display_name = display_name
        self.requirements = requirements
        self.details = details
        self.owned_status = owned_status
        self.module_type = 'component'  # Always 'component' for this class

class ModuleRegistry:
    """
    Central registry for all modules in the application.
    
    This class provides a unified interface for accessing ships, components,
    capital ships, and PI materials.
    """
    def __init__(self):
        self.ships: Dict[str, ShipModule] = {}
        self.capital_ships: Dict[str, CapitalShipModule] = {}
        self.components: Dict[str, ComponentModule] = {}
        self.pi_data: Dict[str, Dict[str, Any]] = {
            'p0_materials': {},
            'p1_materials': {},
            'p2_materials': {},
            'p3_materials': {},
            'p4_materials': {}
        }
        
        # Track available factions and ship types for filtering
        self.factions: Set[str] = set(["All"])
        self.ship_types: Set[str] = set(["All"])

    def register_ship(self, ship: ShipModule) -> None:
        """Register a ship in the registry"""
        self.ships[ship.name] = ship
        
        # Track faction and ship type for filtering
        if ship.faction:
            self.factions.add(ship.faction)
        if ship.ship_type:
            self.ship_types.add(ship.ship_type)
    
    def register_capital_ship(self, capital_ship: CapitalShipModule) -> None:
        """Register a capital ship in the registry"""
        self.capital_ships[capital_ship.name] = capital_ship
    
    def register_component(self, component: ComponentModule) -> None:
        """Register a component in the registry"""
        self.components[component.name] = component
    
    def register_pi_data(self, pi_level: str, materials: Dict[str, Any]) -> None:
        """Register PI materials by level"""
        if pi_level in self.pi_data:
            self.pi_data[pi_level] = materials
    
    def get_ship(self, name: str) -> Optional[ShipModule]:
        """Get a ship by name"""
        return self.ships.get(name)
        
    def get_capital_ship(self, name: str) -> Optional[CapitalShipModule]:
        """Get a capital ship by name"""
        return self.capital_ships.get(name)
        
    def get_component(self, name: str) -> Optional[ComponentModule]:
        """Get a component by name"""
        return self.components.get(name)
    
    def get_all_ships(self) -> Dict[str, ShipModule]:
        """Get all registered ships"""
        return self.ships
        
    def get_all_capital_ships(self) -> Dict[str, CapitalShipModule]:
        """Get all registered capital ships"""
        return self.capital_ships
        
    def get_all_components(self) -> Dict[str, ComponentModule]:
        """Get all registered components"""
        return self.components
    
    def get_filtered_ships(self, faction: str = "All", ship_type: str = "All") -> Dict[str, ShipModule]:
        """
        Get ships filtered by faction and ship type
        
        Args:
            faction: The faction to filter by, or "All" for no filtering
            ship_type: The ship type to filter by, or "All" for no filtering
        
        Returns:
            Dictionary of ships matching the criteria
        """
        # If both filters are "All", return all ships
        if faction == "All" and ship_type == "All":
            return self.ships
            
        # Filter by criteria
        filtered_ships = {}
        for name, ship in self.ships.items():
            faction_match = faction == "All" or ship.faction == faction
            type_match = ship_type == "All" or ship.ship_type == ship_type
            
            if faction_match and type_match:
                filtered_ships[name] = ship
                
        return filtered_ships
    
    def get_factions(self) -> List[str]:
        """Get sorted list of all available factions"""
        return sorted(list(self.factions))
    
    def get_ship_types(self) -> List[str]:
        """Get sorted list of all available ship types"""
        return sorted(list(self.ship_types))

class ModuleLoader:
    """
    Loads modules from various data sources into the registry
    """
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.registry = ModuleRegistry()
    
    def load_all(self) -> ModuleRegistry:
        """Load all module types and return the populated registry"""
        self.load_ships_from_json()
        self.load_capital_ships()
        self.load_components()
        self.load_pi_data()
        return self.registry
    
    def load_ships_from_json(self) -> None:
        """Load ships from JSON data files"""
        ships_json_path = os.path.join(self.base_path, 'data', 'ships.json')
        
        if not os.path.exists(ships_json_path):
            print(f"Ships data file not found: {ships_json_path}")
            return
            
        try:
            with open(ships_json_path, 'r') as file:
                ships_data = json.load(file)
                
            # Process all ships in the data
            for faction_key, faction_data in ships_data.items():
                for category_key, category_data in faction_data.items():
                    for tech_level_key, tech_level_data in category_data.items():
                        for ship_key, ship_data in tech_level_data.items():
                            ship = ShipModule(
                                name=ship_key,
                                display_name=ship_data.get('display_name', ship_key),
                                requirements=ship_data.get('requirements', {}),
                                details=ship_data.get('details', ''),
                                faction=ship_data.get('faction', ''),
                                ship_type=ship_data.get('ship_type', ''),
                                owned_status=ship_data.get('owned_status', 'Unowned')
                            )
                            self.registry.register_ship(ship)
                            
        except Exception as e:
            print(f"Error loading ships from JSON: {e}")
    
    def load_capital_ships(self) -> None:
        """Load capital ships from Python modules"""
        capital_ships_dir = os.path.join(self.base_path, 'Capital Ships')
        
        if not os.path.exists(capital_ships_dir):
            print(f"Capital ships directory not found: {capital_ships_dir}")
            return
            
        for filename in os.listdir(capital_ships_dir):
            if filename.endswith('.py'):
                # Module name is the filename without extension
                module_name = filename[:-3]
                
                # Construct absolute path to the module
                module_path = os.path.join(capital_ships_dir, filename)
                
                try:
                    # Create a module spec and load the module
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Check if module has required attributes
                    if hasattr(module, 'display_name'):
                        # Create capital ship module
                        capital_ship = CapitalShipModule(
                            name=module_name,
                            display_name=getattr(module, 'display_name', module_name),
                            requirements=getattr(module, 'requirements', {}),
                            details=getattr(module, 'details', ''),
                            capital_component_data=getattr(module, 'capital_component_data', {}),
                            owned_status=getattr(module, 'owned_status', 'Unowned')
                        )
                        
                        # Register capital ship
                        self.registry.register_capital_ship(capital_ship)
                    else:
                        print(f"Module {module_name} doesn't have display_name")
                except Exception as e:
                    print(f"Error loading capital ship module {module_path}: {e}")
    
    def load_components(self) -> None:
        """Load components from Python modules"""
        components_dir = os.path.join(self.base_path, 'Components')
        
        if not os.path.exists(components_dir):
            print(f"Components directory not found: {components_dir}")
            return
            
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
                            owned_status=getattr(module, 'owned_status', 'Unowned')
                        )
                        
                        # Register component
                        self.registry.register_component(component)
                    else:
                        print(f"Module {module_name} doesn't have display_name")
                except Exception as e:
                    print(f"Error loading component module {module_path}: {e}")
    
    def load_pi_data(self) -> None:
        """Load PI data from Python module"""
        pi_data_path = os.path.join(self.base_path, 'planetary_data.py')
        
        if not os.path.exists(pi_data_path):
            print(f"PI data file not found: {pi_data_path}")
            return
            
        try:
            # Create a module spec and load the module
            spec = importlib.util.spec_from_file_location('planetary_data', pi_data_path)
            pi_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(pi_module)
            
            # Register PI data by level
            for level in ['p0_materials', 'p1_materials', 'p2_materials', 'p3_materials', 'p4_materials']:
                if hasattr(pi_module, level):
                    self.registry.register_pi_data(level, getattr(pi_module, level, {}))
        except Exception as e:
            print(f"Error loading PI data: {e}")
