"""
Capital Components Module

Loads capital component data from the capitalcomponents.json file and provides it in the format
expected by the ModuleRegistry.
"""
import os
import json

# The display name for this component type
display_name = "Capital Components"

# Load the capital components from the JSON file
components_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "capitalcomponents.json")

# Initialize variables to store component data
capital_components_requirements = {}
capital_components_details = {}
owned_status = "Unowned"

# Try to load the data from the JSON file
try:
    with open(components_path, 'r') as f:
        capital_components_data = json.load(f)
    
    # Extract all components from the JSON
    if 'capital_components' in capital_components_data:
        components = capital_components_data['capital_components']
        
        # For each component, create the required attributes
        for component_key, component_data in components.items():
            # Set the requirements dictionary with the same name as the module
            globals()[component_key + '_requirements'] = component_data.get('requirements', {})
            
            # Set the details for each component
            globals()[component_key + '_details'] = component_data.get('details', '')
            
            # Set display name for each component
            globals()[component_key + '_display_name'] = component_data.get('display_name', component_key)
            
            # Set owned status
            globals()[component_key + '_owned_status'] = component_data.get('owned_status', 'Unowned')
            
except Exception as e:
    print(f"Error loading capital components data: {e}")
