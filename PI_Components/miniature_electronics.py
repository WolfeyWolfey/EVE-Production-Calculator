# Miniature Electronics data structure

# Display name for the dropdown menu
display_name = "Miniature Electronics"

# Blueprint ownership status
owned_status = "Unowned"

# Component quantities required for Miniature Electronics production
miniature_electronics_requirements = {
    "Silicon": 1,
    "Chiral Structures": 1
}

# Specifications and attributes
miniature_electronics_specifications = {
    "example_use": "Used in Tech II components; input for Planetary Vehicles, Smartfab Units (P3)",
    "input_type": "P1 + P1",
    "tier": "P2",
    "more_info": "https://wiki.eveuniversity.org/Planetary_Commodities#:~:text=Microfiber%20Shielding%20None%20known%20Data,Components%20Planetary%20Vehicles%2C%20Smartfab%20Units"
}

# Production details
miniature_electronics_production_details = {
    "facility_requirements": ["Advanced Industry Facility"],
    "production_time": 3600,  # 1 hour in seconds
    "invention": False,  # Not inventable (direct P2 production)
    "base_materials_efficiency": 0  # ME0
}
