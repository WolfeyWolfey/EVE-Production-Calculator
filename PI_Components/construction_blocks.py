# Construction Blocks data structure

# Display name for the dropdown menu
display_name = "Construction Blocks"

# Blueprint ownership status
owned_status = "Unowned"

# Component quantities required for Construction Blocks production
construction_blocks_requirements = {
    "Toxic Metals": 1,
    "Reactive Metals": 1
}

# Specifications and attributes
construction_blocks_specifications = {
    "example_use": "Used in Tech II component construction; input for Robotics, Smartfab Units (P3)",
    "input_type": "P1 + P1",
    "tier": "P2",
    "more_info": "https://wiki.eveuniversity.org/Planetary_Commodities#:~:text=Image%3A%20Lava%20Planet%20%2098,component%2C%20Research%20component%20Robotics%2C%20Supercomputers"
}

# Production details
construction_blocks_production_details = {
    "facility_requirements": ["Advanced Industry Facility"],
    "production_time": 3600,  # 1 hour in seconds
    "invention": False,  # Not inventable (direct P2 production)
    "base_materials_efficiency": 0  # ME0
}
