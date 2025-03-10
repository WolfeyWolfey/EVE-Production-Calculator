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
                 faction: Optional[str] = None,
                 ship_type: Optional[str] = None,
                 capital_component_data: Dict[str, Dict[str, Any]] = None,
                 owned_status: Optional[str] = None):
        self.name = name
        self.display_name = display_name
        self.requirements = requirements
        self.details = details
        self.faction = faction
        self.ship_type = ship_type
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
            faction: Optional faction to filter by, or "All" for no filtering
            ship_type: Optional ship type to filter by, or "All" for no filtering
            
        Returns:
            Dictionary of ships matching the filter criteria
        """
        if faction == "All" and ship_type == "All":
            return self.ships
            
        filtered_ships = {}
        for name, ship in self.ships.items():
            faction_match = faction == "All" or ship.faction == faction
            type_match = ship_type == "All" or ship.ship_type == ship_type
            
            if faction_match and type_match:
                filtered_ships[name] = ship
                
        return filtered_ships
    
    def get_ships_by_filter(self, faction: Optional[str] = None, ship_type: Optional[str] = None, owned_only: bool = False) -> List[ShipModule]:
        """
        Get ships filtered by faction, ship type, and ownership
        
        Args:
            faction: Optional faction to filter by, or None for no filtering
            ship_type: Optional ship type to filter by, or None for no filtering
            owned_only: If True, only return ships that are owned
            
        Returns:
            List of ShipModule objects matching the filter criteria
        """
        filtered_ships = []
        for name, ship in self.ships.items():
            faction_match = faction is None or ship.faction == faction
            type_match = ship_type is None or ship.ship_type == ship_type
            ownership_match = not owned_only or ship.owned_status == "Owned"
            
            if faction_match and type_match and ownership_match:
                filtered_ships.append(ship)
                
        return filtered_ships
    
    def get_capital_ships_by_filter(self, faction: Optional[str] = None, ship_type: Optional[str] = None, owned_only: bool = False) -> List[CapitalShipModule]:
        """
        Get capital ships filtered by faction, ship type, and ownership
        
        Args:
            faction: Optional faction to filter by, or None for no filtering
            ship_type: Optional ship type to filter by, or None for no filtering
            owned_only: If True, only return capital ships that are owned
            
        Returns:
            List of CapitalShipModule objects matching the filter criteria
        """
        filtered_ships = []
        for name, ship in self.capital_ships.items():
            faction_match = faction is None or ship.faction == faction
            type_match = ship_type is None or ship.ship_type == ship_type
            ownership_match = not owned_only or ship.owned_status == "Owned"
            
            if faction_match and type_match and ownership_match:
                filtered_ships.append(ship)
                
        return filtered_ships
    
    def get_factions(self) -> List[str]:
        """Get sorted list of all available factions"""
        return sorted(list(self.factions))
    
    def get_ship_types(self) -> List[str]:
        """Get sorted list of all available ship types"""
        return sorted(list(self.ship_types))

    def get_ship_by_display_name(self, display_name: str) -> Optional[ShipModule]:
        """
        Get a ship by its display name
        
        Args:
            display_name: The display name of the ship to find
            
        Returns:
            ShipModule if found, None otherwise
        """
        for name, ship in self.ships.items():
            if ship.display_name == display_name:
                return ship
        return None
    
    def get_capital_ship_by_display_name(self, display_name: str) -> Optional[CapitalShipModule]:
        """
        Get a capital ship by its display name
        
        Args:
            display_name: The display name of the capital ship to find
            
        Returns:
            CapitalShipModule if found, None otherwise
        """
        for name, capital_ship in self.capital_ships.items():
            if capital_ship.display_name == display_name:
                return capital_ship
        return None
    
    def get_component_by_display_name(self, display_name: str) -> Optional[ComponentModule]:
        """
        Get a component by its display name
        
        Args:
            display_name: The display name of the component to find
            
        Returns:
            ComponentModule if found, None otherwise
        """
        for name, component in self.components.items():
            if component.display_name == display_name:
                return component
        return None

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
        # We're now loading capital ships from JSON, so this is no longer needed
        # self.load_capital_ships()
        self.load_components()
        self.load_pi_data()
        return self.registry
    
    def load_ships_from_json(self) -> None:
        """
        Load all ship data from JSON file and register in the ModuleRegistry
        """
        ships_json_path = os.path.join(os.path.dirname(__file__), "data", "ships.json")
        
        with open(ships_json_path, 'r') as f:
            ships_data = json.load(f)
        
        # Track loaded ships count
        ship_count = 0
        capital_ship_count = 0
        
        # Process ships recursively using the original method that handles the nested structure
        for faction_key, faction_data in ships_data.items():
            # Skip the special capital_ships entry as we'll handle it separately
            if faction_key == "capital_ships":
                continue
                
            # Process each ship category within the faction
            self._process_ship_category(faction_key, faction_data)
            ship_count += self._count_ships_in_data(faction_data)
        
        # Process capital ships specifically
        if "capital_ships" in ships_data:
            capital_ships_data = ships_data["capital_ships"]
            self._process_capital_ships(capital_ships_data)
            capital_ship_count = self._count_ships_in_data(capital_ships_data)
            
        print(f"Loaded {ship_count} ships and {capital_ship_count} capital ships")
        
    def _count_ships_in_data(self, data):
        """Count the number of ship entries in a nested data structure"""
        count = 0
        if isinstance(data, dict):
            # If this dict has ship characteristics, count it as one ship
            if "display_name" in data and "requirements" in data:
                return 1
                
            # Otherwise, recurse into its values
            for value in data.values():
                count += self._count_ships_in_data(value)
                
        return count
    
    def _process_ship_category(self, parent_key, category_data):
        """Process a category of ships (e.g., faction or ship class)"""
        if isinstance(category_data, dict):
            # Check if this is a ship entry
            if "display_name" in category_data and "requirements" in category_data:
                # Create and register the ship
                ship = ShipModule(
                    name=parent_key,
                    display_name=category_data.get('display_name'),
                    requirements=category_data.get('requirements', {}),
                    details=category_data.get('details', ''),
                    faction=category_data.get('faction', ''),
                    ship_type=category_data.get('ship_type', ''),
                    owned_status='Unowned'  # Force Unowned status by default
                )
                self.registry.register_ship(ship)
                
                # Track factions and ship types for filtering
                if ship.faction and ship.faction not in self.registry.factions:
                    self.registry.factions.add(ship.faction)
                    
                if ship.ship_type and ship.ship_type not in self.registry.ship_types:
                    self.registry.ship_types.add(ship.ship_type)
            else:
                # Recurse into child categories
                for key, value in category_data.items():
                    self._process_ship_category(key, value)
    
    def _process_capital_ships(self, capital_ships_data):
        """Process capital ships specifically"""
        if isinstance(capital_ships_data, dict):
            for category, ships in capital_ships_data.items():
                if isinstance(ships, dict):
                    for ship_key, ship_data in ships.items():
                        if "display_name" in ship_data and "requirements" in ship_data:
                            # Create and register the capital ship
                            capital_ship = CapitalShipModule(
                                name=ship_key,
                                display_name=ship_data.get('display_name'),
                                requirements=ship_data.get('requirements', {}),
                                details=ship_data.get('details', ''),
                                faction=ship_data.get('faction', ''),
                                ship_type=ship_data.get('ship_type', ''),
                                owned_status='Unowned'  # Force Unowned status by default
                            )
                            self.registry.register_capital_ship(capital_ship)
    
    def load_capital_ships(self) -> None:
        """
        [DEPRECATED] Load capital ships from Python modules
        This method is kept for backward compatibility but is no longer used.
        Capital ships are now loaded from the ships.json file.
        """
        pass
    
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
