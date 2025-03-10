# Enriched Uranium data structure

# Display name for the dropdown menu
display_name = "Enriched Uranium"

# Blueprint ownership status
owned_status = "Unowned"

# Component quantities required for Enriched Uranium production
enriched_uranium_requirements = {
    "Toxic Metals": 1,
    "Precious Metals": 1
}

# Specifications and attributes
enriched_uranium_specifications = {
    "example_use": "Used in structure fuel (fuel blocks); input for Nuclear Reactors (P3)",
    "input_type": "P1 + P1",
    "tier": "P2",
    "more_info": "https://wiki.eveuniversity.org/Planetary_Commodities#:~:text=Structure%20Fuel%20Condensates%2C%20Supercomputers%20Image%3A,104Image%3A%20Temperate%20Planet%20Proteins%20Bacteria"
}

# Production details
enriched_uranium_production_details = {
    "facility_requirements": ["Advanced Industry Facility"],
    "production_time": 3600,  # 1 hour in seconds
    "invention": False,  # Not inventable (direct P2 production)
    "base_materials_efficiency": 0  # ME0
}
