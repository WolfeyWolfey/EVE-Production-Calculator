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
    
    def calculate_ship_requirements(self, ship_name: str, me_level: int) -> Dict[str, Union[int, float]]:
        """
        Calculate material requirements for a ship with material efficiency
        
        Args:
            ship_name: Name of the ship to calculate for
            me_level: Material Efficiency level (0-10)
            
        Returns:
            Dictionary of materials and quantities required
        """
        ship = self.registry.get_ship(ship_name)
        if not ship:
            return {}
            
        return self._apply_material_efficiency(ship.requirements, me_level)
    
    def calculate_capital_ship_requirements(self, capital_ship_name: str, me_level: int) -> Dict[str, Union[int, float]]:
        """
        Calculate material requirements for a capital ship with material efficiency
        
        Args:
            capital_ship_name: Name of the capital ship to calculate for
            me_level: Material Efficiency level (0-10)
            
        Returns:
            Dictionary of materials and quantities required
        """
        capital_ship = self.registry.get_capital_ship(capital_ship_name)
        if not capital_ship:
            return {}
            
        return self._apply_material_efficiency(capital_ship.requirements, me_level)
    
    def calculate_component_requirements(self, component_name: str, me_level: int) -> Dict[str, Union[int, float]]:
        """
        Calculate material requirements for a component with material efficiency
        
        Args:
            component_name: Name of the component to calculate for
            me_level: Material Efficiency level (0-10)
            
        Returns:
            Dictionary of materials and quantities required
        """
        component = self.registry.get_component(component_name)
        if not component:
            return {}
            
        return self._apply_material_efficiency(component.requirements, me_level)
    
    def calculate_pi_requirements(self, pi_level: str, item_name: str, quantity: int) -> Dict[str, int]:
        """
        Calculate material requirements for PI production
        
        Args:
            pi_level: PI level (p0_materials, p1_materials, etc.)
            item_name: Name of the PI item to calculate for
            quantity: Quantity to produce
            
        Returns:
            Dictionary of materials and quantities required
        """
        if pi_level not in self.registry.pi_data:
            return {}
            
        pi_items = self.registry.pi_data[pi_level]
        if item_name not in pi_items:
            return {}
            
        item_data = pi_items[item_name]
        if 'ingredients' not in item_data:
            return {}
            
        # Scale ingredients by quantity
        result = {}
        for ingredient, amount in item_data['ingredients'].items():
            result[ingredient] = amount * quantity
            
        return result
    
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
