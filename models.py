"""
Module models for EVE Production Calculator

This file contains the data model classes for ships, components, and PI materials
"""
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

class PiMaterialModule:
    """Representation of a PI material with all its attributes and requirements"""
    def __init__(self, 
                 name: str, 
                 display_name: str, 
                 requirements: Dict[str, int], 
                 details: str,
                 pi_level: str,
                 planet_types: List[str] = None,
                 outputs: Dict[str, int] = None):
        self.name = name
        self.display_name = display_name
        self.requirements = requirements or {}
        self.details = details
        self.pi_level = pi_level  # P0, P1, P2, P3, P4
        self.planet_types = planet_types or []  # Types of planets the material can be harvested from
        self.outputs = outputs or {}  # What this material produces if processed
        self.module_type = 'pi_material'  # Always 'pi_material' for this class
