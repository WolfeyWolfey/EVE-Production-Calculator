# Polytextiles data structure

# Display name for the dropdown menu
display_name = "Polytextiles"

# Blueprint ownership status
owned_status = "Unowned"

# Component quantities required for Polytextiles production
polytextiles_requirements = {
    "Industrial Fibers": 1,
    "Biofuels": 1
}

# Specifications and attributes
polytextiles_specifications = {
    "example_use": "Used to make Hazmat Detection Systems, Industrial Explosives (P3)",
    "input_type": "P1 + P1",
    "tier": "P2",
    "more_info": "https://wiki.eveuniversity.org/Planetary_Commodities#:~:text=Image%3A%20Gas%20Planet%20%2B%20117,Hazmat%20Detection%20Systems%2C%20Industrial%20Explosives"
}

# Production details
polytextiles_production_details = {
    "facility_requirements": ["Advanced Industry Facility"],
    "production_time": 3600,  # 1 hour in seconds
    "invention": False,  # Not inventable (direct P2 production)
    "base_materials_efficiency": 0  # ME0
}
