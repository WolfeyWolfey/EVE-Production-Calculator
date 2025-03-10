"""
Resource Calculator for EVE Production Calculator

This module provides centralized calculation logic for all EVE resource requirements
"""
from typing import Dict, Any, List, Union, Optional
from module_registry import ModuleRegistry, ShipModule, CapitalShipModule, ComponentModule

class RequirementsCalculator:
    """
    Centralized calculator for all EVE resource requirements
    
    This class handles all resource calculations for ships, components,
    capital ships, PI materials, and ore refining.
    """
    def __init__(self, module_registry: ModuleRegistry):
        """
        Initialize the calculator with the module registry
        
        Args:
            module_registry: The central registry containing all module data
        """
        self.registry = module_registry
        self.blueprint_config = None  # Will be set externally
    
    def set_blueprint_config(self, blueprint_config: Dict[str, Any]):
        """
        Set the blueprint configuration to use for ME values
        
        Args:
            blueprint_config: Blueprint configuration dictionary
        """
        self.blueprint_config = blueprint_config
    
    def get_me_level(self, category: str, blueprint_name: str) -> int:
        """
        Get the material efficiency level for a specific blueprint
        
        Args:
            category: Category of blueprint (ships, capital_ships, components)
            blueprint_name: Name of the blueprint
            
        Returns:
            Material Efficiency level (default: 0)
        """
        from blueprint_config import get_blueprint_me
        
        if self.blueprint_config:
            return get_blueprint_me(self.blueprint_config, category, blueprint_name)
        return 0
    
    def calculate_ship_requirements(self, ship_name: str) -> Dict[str, Union[int, float]]:
        """
        Calculate material requirements for a ship with material efficiency
        
        Args:
            ship_name: Name of the ship to calculate for
            
        Returns:
            Dictionary of materials and quantities required
        """
        ship = self.registry.get_ship(ship_name)
        if not ship:
            return {}
            
        # Get ME% for this specific ship
        me_level = self.get_me_level('ships', ship_name)
        return self._apply_material_efficiency(ship.requirements, me_level)
    
    def calculate_capital_ship_requirements(self, capital_ship_name: str) -> Dict[str, Union[int, float]]:
        """
        Calculate material requirements for a capital ship with material efficiency
        
        Args:
            capital_ship_name: Name of the capital ship to calculate for
            
        Returns:
            Dictionary of materials and quantities required
        """
        capital_ship = self.registry.get_capital_ship(capital_ship_name)
        if not capital_ship:
            return {}
            
        # Get ME% for this specific capital ship
        me_level = self.get_me_level('capital_ships', capital_ship_name)
        return self._apply_material_efficiency(capital_ship.requirements, me_level)
    
    def calculate_component_requirements(self, component_name: str) -> Dict[str, Union[int, float]]:
        """
        Calculate material requirements for a component with material efficiency
        
        Args:
            component_name: Name of the component to calculate for
            
        Returns:
            Dictionary of materials and quantities required
        """
        component = self.registry.get_component(component_name)
        if not component:
            return {}
            
        # Get ME% for this specific component
        me_level = self.get_me_level('components', component_name)
        return self._apply_material_efficiency(component.requirements, me_level)
    
    def calculate_pi_requirements(self, pi_material_name: str) -> Dict[str, Union[int, float]]:
        """
        Calculate material requirements for a PI material with material efficiency
        
        Args:
            pi_material_name: Name of the PI material to calculate for
            
        Returns:
            Dictionary of materials and quantities required
        """
        pi_material = self.registry.get_pi_material(pi_material_name)
        if not pi_material:
            return {}
        
        # For P0 materials (raw materials), there are no requirements
        if pi_material.pi_level == "P0":
            return {}
            
        return self._apply_material_efficiency(pi_material.requirements, self.get_me_level('pi', pi_material_name))
    
    def calculate_ore_requirements(self, ore_name: str) -> Dict[str, Union[int, float]]:
        """
        Calculate material requirements for ore refining with efficiency
        
        Args:
            ore_name: Name of the ore to calculate for
            
        Returns:
            Dictionary of materials and quantities required
        """
        # This function would need access to ore data
        # This is a placeholder implementation until ore data is available
        return {}
    
    def calculate_ore_refining(self, ore_name: str, quantity: int, efficiency: float) -> Dict[str, int]:
        """
        Calculate refined minerals from ore
        
        Args:
            ore_name: Name of the ore to refine
            quantity: Quantity of ore to refine
            efficiency: Refining efficiency as a percentage (0-100)
            
        Returns:
            Dictionary of minerals and quantities produced
        """
        # This function would need access to ore data which is not in the registry yet
        # This is a placeholder implementation
        return {}
    
    def _apply_material_efficiency(self, requirements: Dict[str, int], me_level: int) -> Dict[str, Union[int, float]]:
        """
        Apply material efficiency to requirements
        
        Args:
            requirements: Dictionary of base material requirements
            me_level: Material Efficiency level (0-10)
            
        Returns:
            Dictionary with material efficiency applied
        """
        if me_level < 0:
            me_level = 0
        elif me_level > 10:
            me_level = 10
            
        result = {}
        for material, amount in requirements.items():
            # Apply ME formula: base * (1 - (ME_level / 100))
            me_multiplier = 1 - (me_level / 100)
            adjusted_amount = amount * me_multiplier
            
            # Round up to nearest whole number
            result[material] = round(adjusted_amount)
            
        return result
    
    def aggregate_requirements(self, requirements_list: List[Dict[str, Union[int, float]]]) -> Dict[str, Union[int, float]]:
        """
        Aggregate multiple requirement dictionaries into one
        
        Args:
            requirements_list: List of requirement dictionaries to aggregate
            
        Returns:
            Aggregated dictionary of materials and quantities
        """
        result = {}
        for requirements in requirements_list:
            for material, amount in requirements.items():
                if material in result:
                    result[material] += amount
                else:
                    result[material] = amount
        
        return result
