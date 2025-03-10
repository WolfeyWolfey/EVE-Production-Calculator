# Mechanical Parts data structure

# Display name for the dropdown menu
display_name = "Mechanical Parts"

# Blueprint ownership status
owned_status = "Unowned"

# Component quantities required for Mechanical Parts production
mechanical_parts_requirements = {
    "Precious Metals": 1,
    "Reactive Metals": 1
}

# Specifications and attributes
mechanical_parts_specifications = {
    "example_use": "Used in structure fuel, Tech II components; input for Planetary Vehicles, Robotics (P3)",
    "input_type": "P1 + P1",
    "tier": "P2",
    "more_info": "https://wiki.eveuniversity.org/Planetary_Commodities#:~:text=Livestock%20None%20known%20Biotech%20Research,Fuel%2C%20T2%20components%20Planetary%20Vehicles"
}

# Production details
mechanical_parts_production_details = {
    "facility_requirements": ["Advanced Industry Facility"],
    "production_time": 3600,  # 1 hour in seconds
    "invention": False,  # Not inventable (direct P2 production)
    "base_materials_efficiency": 0  # ME0
}
