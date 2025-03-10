# Industrial Explosives data structure

# Display name for the dropdown menu
display_name = "Industrial Explosives"

# Blueprint ownership status
owned_status = "Unowned"

# Component quantities required for Industrial Explosives production
industrial_explosives_requirements = {
    "Polytextiles": 1,
    "Fertilizer": 1
}

# Specifications and attributes
industrial_explosives_specifications = {
    "example_use": "Used in advanced manufacturing processes",
    "input_type": "P2 + P2",
    "tier": "P3",
    "more_info": "https://wiki.eveuniversity.org/Planetary_Commodities"
}

# Production details
industrial_explosives_production_details = {
    "facility_requirements": ["Advanced Industry Facility"],
    "production_time": 7200,  # 2 hours in seconds
    "invention": False,  # Not inventable (direct P3 production)
    "base_materials_efficiency": 0  # ME0
}
