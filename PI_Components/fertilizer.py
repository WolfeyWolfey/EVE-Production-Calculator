# Fertilizer data structure

# Display name for the dropdown menu
display_name = "Fertilizer"

# Blueprint ownership status
owned_status = "Unowned"

# Component quantities required for Fertilizer production
fertilizer_requirements = {
    "Proteins": 1,
    "Bacteria": 1
}

# Specifications and attributes
fertilizer_specifications = {
    "example_use": "(No direct use) Used to make Industrial Explosives, Cryoprotectant Solution (P3)",
    "input_type": "P1 + P1",
    "tier": "P2",
    "more_info": "https://wiki.eveuniversity.org/Planetary_Commodities#:~:text=Structure%20Fuel%20Nuclear%20Reactors%20Image%3A,Proteins%20Genetically%20Enhanced%20Livestock%20None"
}

# Production details
fertilizer_production_details = {
    "facility_requirements": ["Advanced Industry Facility"],
    "production_time": 3600,  # 1 hour in seconds
    "invention": False,  # Not inventable (direct P2 production)
    "base_materials_efficiency": 0  # ME0
}
