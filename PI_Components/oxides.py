# Oxides data structure

# Display name for the dropdown menu
display_name = "Oxides"

# Blueprint ownership status
owned_status = "Unowned"

# Component quantities required for Oxides production
oxides_requirements = {
    "Oxygen": 1,
    "Oxidizing Compound": 1
}

# Specifications and attributes
oxides_specifications = {
    "example_use": "(No direct use) Used to make Condensates, Gel-Matrix Biopaste (P3)",
    "input_type": "P1 + P1",
    "tier": "P2",
    "more_info": "https://wiki.eveuniversity.org/Planetary_Commodities#:~:text=Transcranial%20Microcontroller%20Image%3A%20Gas%20Planet,116%2BImage%3A%20Temperate%20Planet%20Industrial%20Fibers"
}

# Production details
oxides_production_details = {
    "facility_requirements": ["Advanced Industry Facility"],
    "production_time": 3600,  # 1 hour in seconds
    "invention": False,  # Not inventable (direct P2 production)
    "base_materials_efficiency": 0  # ME0
}
