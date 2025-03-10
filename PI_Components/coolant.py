# Coolant data structure

# Display name for the dropdown menu
display_name = "Coolant"

# Blueprint ownership status
owned_status = "Unowned"

# Component quantities required for Coolant production
coolant_requirements = {
    "Water": 1,
    "Electrolytes": 1
}

# Specifications and attributes
coolant_specifications = {
    "example_use": "Used in structure fuel (fuel blocks); input for Condensates, Supercomputers (P3)",
    "input_type": "P1 + P1",
    "tier": "P2",
    "more_info": "https://wiki.eveuniversity.org/Planetary_Commodities#:~:text=Image%3A%20Gas%20Planet%20%20102,Coolant%20Structure%20Fuel%20Condensates%2C%20Supercomputers"
}

# Production details
coolant_production_details = {
    "facility_requirements": ["Advanced Industry Facility"],
    "production_time": 3600,  # 1 hour in seconds
    "invention": False,  # Not inventable (direct P2 production)
    "base_materials_efficiency": 0  # ME0
}
