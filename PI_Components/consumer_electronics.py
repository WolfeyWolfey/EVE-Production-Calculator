# Consumer Electronics data structure

# Display name for the dropdown menu
display_name = "Consumer Electronics"

# Blueprint ownership status
owned_status = "Unowned"

# Component quantities required for Consumer Electronics production
consumer_electronics_requirements = {
    "Chiral Structures": 1,
    "Toxic Metals": 1
}

# Specifications and attributes
consumer_electronics_specifications = {
    "example_use": "Used in Tech II and research components; input for Robotics, Supercomputers (P3)",
    "input_type": "P1 + P1",
    "tier": "P2",
    "more_info": "https://wiki.eveuniversity.org/Planetary_Commodities#:~:text=Image%3A%20Lava%20Planet%20%2098,component%2C%20Research%20component%20Robotics%2C%20Supercomputers"
}

# Production details
consumer_electronics_production_details = {
    "facility_requirements": ["Advanced Industry Facility"],
    "production_time": 3600,  # 1 hour in seconds
    "invention": False,  # Not inventable (direct P2 production)
    "base_materials_efficiency": 0  # ME0
}
