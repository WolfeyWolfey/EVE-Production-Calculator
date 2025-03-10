"""
Module Registry for EVE Production Calculator

This system manages the registry of all data modules (ships, components, etc.) with a unified interface
"""
import os
from typing import Dict, List, Any, Optional, Set, Tuple

from core.models import ShipModule, CapitalShipModule, ComponentModule, PiMaterialModule

class ModuleRegistry:
    """Central registry for all modules in the application.
    
    This class provides a unified interface for accessing ships, components,
    capital ships, and PI materials.
    """
    def __init__(self):
        self.ships: Dict[str, ShipModule] = {}
        self.capital_ships: Dict[str, CapitalShipModule] = {}
        self.components: Dict[str, ComponentModule] = {}
        self.capital_components: Dict[str, ComponentModule] = {}  # Explicitly store capital components
        self.pi_materials: Dict[str, PiMaterialModule] = {}
        self.pi_data: Dict[str, Dict[str, Any]] = {
            'p0_materials': {},
            'p1_materials': {},
            'p2_materials': {},
            'p3_materials': {},
            'p4_materials': {}
        }
        self.ores: Dict[str, Any] = {}
        
        # Track available factions and ship types for filtering
        self.factions: Set[str] = set(["All"])
        self.ship_types: Set[str] = set(["All"])
    
    def register_ship(self, ship: ShipModule):
        """
        Register a ship in the registry
        
        Args:
            ship: The ship to register
        """
        self.ships[ship.name] = ship
        
        # Add faction to available factions
        if ship.faction and ship.faction not in self.factions:
            self.factions.add(ship.faction)
            
        # Add ship type to available ship types
        if ship.ship_type and ship.ship_type not in self.ship_types:
            self.ship_types.add(ship.ship_type)
    
    def register_capital_ship(self, capital_ship: CapitalShipModule):
        """
        Register a capital ship in the registry
        
        Args:
            capital_ship: The capital ship to register
        """
        self.capital_ships[capital_ship.name] = capital_ship
        
        # Add faction to available factions if not already present
        if capital_ship.faction and capital_ship.faction not in self.factions:
            self.factions.add(capital_ship.faction)
            
        # Add ship type to available ship types if not already present
        if capital_ship.ship_type and capital_ship.ship_type not in self.ship_types:
            self.ship_types.add(capital_ship.ship_type)
    
    def register_component(self, component: ComponentModule):
        """
        Register a component in the registry
        
        Args:
            component: The component to register
        """
        self.components[component.name] = component
    
    def register_capital_component(self, component: ComponentModule):
        """
        Register a capital component in the registry
        
        Args:
            component: The capital component to register
        """
        self.capital_components[component.name] = component
    
    def register_pi_data(self, pi_level: str, materials: Dict[str, Any]):
        """
        Register PI materials by level
        
        Args:
            pi_level: The PI level (p0_materials, p1_materials, etc.)
            materials: Dictionary of materials for this level
        """
        self.pi_data[pi_level] = materials
    
    def register_pi_material(self, pi_material: PiMaterialModule):
        """
        Register a PI material in the registry
        
        Args:
            pi_material: The PI material to register
        """
        self.pi_materials[pi_material.name] = pi_material
    
    def get_ship(self, name: str):
        """
        Get a ship by name
        
        Args:
            name: The name of the ship to find
            
        Returns:
            ShipModule if found, None otherwise
        """
        return self.ships.get(name)
    
    def get_capital_ship(self, name: str):
        """
        Get a capital ship by name
        
        Args:
            name: The name of the capital ship to find
            
        Returns:
            CapitalShipModule if found, None otherwise
        """
        return self.capital_ships.get(name)
    
    def get_component(self, name: str):
        """
        Get a component by name
        
        Args:
            name: The name of the component to find
            
        Returns:
            ComponentModule if found, None otherwise
        """
        return self.components.get(name)
    
    def get_capital_component(self, name: str):
        """
        Get a capital component by name
        
        Args:
            name: The name of the capital component to find
            
        Returns:
            ComponentModule if found, None otherwise
        """
        return self.capital_components.get(name)
    
    def get_pi_material(self, name: str):
        """
        Get a PI material by name
        
        Args:
            name: The name of the PI material to find
            
        Returns:
            PiMaterialModule if found, None otherwise
        """
        return self.pi_materials.get(name)
    
    def get_pi_material_by_display_name(self, display_name: str):
        """
        Get a PI material by display name
        
        Args:
            display_name: The display name of the PI material to find
            
        Returns:
            PiMaterialModule if found, None otherwise
        """
        for material in self.pi_materials.values():
            if material.display_name == display_name:
                return material
        return None
    
    def get_pi_materials_by_level(self, pi_level: str):
        """
        Get PI materials filtered by level (P0, P1, P2, P3, P4)
        
        Args:
            pi_level: The PI level to filter by
            
        Returns:
            List of PiMaterialModule objects at the specified level
        """
        return [m for m in self.pi_materials.values() if m.pi_level == pi_level]
    
    def get_all_pi_materials(self):
        """
        Get all registered PI materials
        
        Returns:
            List of all PiMaterialModule objects
        """
        return list(self.pi_materials.values())
    
    def get_all_ships(self):
        """
        Get all registered ships
        
        Returns:
            List of all ShipModule objects
        """
        return list(self.ships.values())
    
    def get_all_capital_ships(self):
        """
        Get all registered capital ships
        
        Returns:
            List of all CapitalShipModule objects
        """
        return list(self.capital_ships.values())
    
    def get_all_components(self):
        """
        Get all registered components
        
        Returns:
            List of all ComponentModule objects
        """
        return list(self.components.values())
    
    def get_all_capital_components(self):
        """
        Get all registered capital components
        
        Returns:
            List of all ComponentModule objects
        """
        return list(self.capital_components.values())
    
    def get_all_ships_combined(self):
        """
        Get all registered ships and capital ships combined in a single list
        
        Returns:
            List of all ShipModule and CapitalShipModule objects
        """
        return list(self.ships.values()) + list(self.capital_ships.values())
    
    def get_filtered_ships(self, faction: str = "All", ship_type: str = "All"):
        """
        Get ships filtered by faction and ship type
        
        Args:
            faction: Optional faction to filter by, or "All" for no filtering
            ship_type: Optional ship type to filter by, or "All" for no filtering
            
        Returns:
            Dictionary of ships matching the filter criteria
        """
        filtered_ships = {}
        
        for name, ship in self.ships.items():
            # Apply faction filter if not "All"
            if faction != "All" and ship.faction != faction:
                continue
                
            # Apply ship type filter if not "All"
            if ship_type != "All" and ship.ship_type != ship_type:
                continue
                
            # Ship passed all filters, add it to filtered_ships
            filtered_ships[name] = ship
            
        return filtered_ships
    
    def get_ships_by_filter(self, faction: Optional[str] = None, ship_type: Optional[str] = None, owned_only: bool = False):
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
        
        for ship in self.ships.values():
            # Apply faction filter if provided
            if faction and faction != "All" and ship.faction != faction:
                continue
                
            # Apply ship type filter if provided
            if ship_type and ship_type != "All" and ship.ship_type != ship_type:
                continue
                
            # Apply ownership filter if requested
            if owned_only:
                # Handle both boolean and string ownership values
                if isinstance(ship.owned_status, bool) and not ship.owned_status:
                    continue
                elif isinstance(ship.owned_status, str) and ship.owned_status.lower() != "owned":
                    continue
            
            # Ship passed all filters, add it to filtered_ships
            filtered_ships.append(ship)
            
        return filtered_ships
    
    def get_capital_ships_by_filter(self, faction: Optional[str] = None, ship_type: Optional[str] = None, owned_only: bool = False):
        """
        Get capital ships filtered by faction, ship type, and ownership
        
        Args:
            faction: Optional faction to filter by, or None for no filtering
            ship_type: Optional ship type to filter by, or None for no filtering
            owned_only: If True, only return capital ships that are owned
            
        Returns:
            List of CapitalShipModule objects matching the filter criteria
        """
        filtered_capital_ships = []
        
        for capital_ship in self.capital_ships.values():
            # Apply faction filter if provided
            if faction and faction != "All" and capital_ship.faction != faction:
                continue
                
            # Apply ship type filter if provided
            if ship_type and ship_type != "All" and capital_ship.ship_type != ship_type:
                continue
                
            # Apply ownership filter if requested
            if owned_only:
                # Handle both boolean and string ownership values
                if isinstance(capital_ship.owned_status, bool) and not capital_ship.owned_status:
                    continue
                elif isinstance(capital_ship.owned_status, str) and capital_ship.owned_status.lower() != "owned":
                    continue
            
            # Capital ship passed all filters, add it to filtered_capital_ships
            filtered_capital_ships.append(capital_ship)
            
        return filtered_capital_ships
    
    def get_ships_combined_by_filter(self, faction: Optional[str] = None, ship_type: Optional[str] = None, owned_only: bool = False):
        """
        Get both regular ships and capital ships filtered by faction, ship type, and ownership
        
        Args:
            faction: Optional faction to filter by, or None for no filtering
            ship_type: Optional ship type to filter by, or None for no filtering
            owned_only: If True, only return ships that are owned
            
        Returns:
            List of ShipModule and CapitalShipModule objects matching the filter criteria
        """
        # Get filtered regular ships
        filtered_ships = self.get_ships_by_filter(faction, ship_type, owned_only)
        
        # Get filtered capital ships
        filtered_capital_ships = self.get_capital_ships_by_filter(faction, ship_type, owned_only)
        
        # Combine the results
        return filtered_ships + filtered_capital_ships
        
    def get_factions(self):
        """
        Get sorted list of all available factions
        
        Returns:
            Sorted list of faction names
        """
        return sorted(list(self.factions))
    
    def get_ship_types(self):
        """
        Get sorted list of all available ship types
        
        Returns:
            Sorted list of ship type names
        """
        return sorted(list(self.ship_types))
    
    def get_ship_by_display_name(self, display_name: str):
        """
        Get a ship by its display name
        
        Args:
            display_name: The display name of the ship to find
            
        Returns:
            ShipModule if found, None otherwise
        """
        for ship in self.ships.values():
            if ship.display_name == display_name:
                return ship
        return None
    
    def get_capital_ship_by_display_name(self, display_name: str):
        """
        Get a capital ship by its display name
        
        Args:
            display_name: The display name of the capital ship to find
            
        Returns:
            CapitalShipModule if found, None otherwise
        """
        for capital_ship in self.capital_ships.values():
            if capital_ship.display_name == display_name:
                return capital_ship
        return None
    
    def get_ship_by_display_name_combined(self, display_name: str):
        """
        Get any ship (regular or capital) by its display name
        
        Args:
            display_name: The display name of the ship to find
            
        Returns:
            ShipModule or CapitalShipModule if found, None otherwise
        """
        # First check regular ships
        ship = self.get_ship_by_display_name(display_name)
        if ship:
            return ship
            
        # If not found, check capital ships
        return self.get_capital_ship_by_display_name(display_name)
    
    def get_component_by_display_name(self, display_name: str):
        """
        Get a component by its display name
        
        Args:
            display_name: The display name of the component to find
            
        Returns:
            ComponentModule if found, None otherwise
        """
        # First check regular components
        for component in self.components.values():
            if component.display_name == display_name:
                return component
                
        # If not found, check capital components
        for component in self.capital_components.values():
            if component.display_name == display_name:
                return component
                
        return None
    
    def get_capital_component_by_display_name(self, display_name: str):
        """
        Get a capital component by its display name
        
        Args:
            display_name: The display name of the capital component to find
            
        Returns:
            ComponentModule if found, None otherwise
        """
        for component in self.capital_components.values():
            if component.display_name == display_name:
                return component
        return None
    
    def get_ore_by_display_name(self, display_name: str):
        """
        Get an ore by its display name
        
        Args:
            display_name: The display name of the ore to find
            
        Returns:
            OreModule if found, None otherwise
        """
        return self.ores.get(display_name)
    
    def get_all_ores(self):
        """
        Get all registered ores
        
        Returns:
            List of OreModule objects
        """
        return list(self.ores.values())
    
    def get_components_by_filter(self, owned_only: bool = False):
        """
        Get components filtered by ownership
        
        Args:
            owned_only: If True, only return components that are owned
            
        Returns:
            List of ComponentModule objects matching the filter criteria
        """
        filtered_components = []
        
        # Process regular components
        for component in self.components.values():
            # Apply ownership filter if requested
            if owned_only:
                # Handle both boolean and string ownership values
                if isinstance(component.owned_status, bool) and not component.owned_status:
                    continue
                elif isinstance(component.owned_status, str) and component.owned_status.lower() != "owned":
                    continue
            
            # Component passed all filters, add it to filtered_components
            filtered_components.append(component)
        
        # Process capital components
        for component in self.capital_components.values():
            # Apply ownership filter if requested
            if owned_only:
                # Handle both boolean and string ownership values
                if isinstance(component.owned_status, bool) and not component.owned_status:
                    continue
                elif isinstance(component.owned_status, str) and component.owned_status.lower() != "owned":
                    continue
            
            # Component passed all filters, add it to filtered_components
            filtered_components.append(component)
            
        return filtered_components
