# Polyaramids data structure

# Display name for the dropdown menu
display_name = "Polyaramids"

# Blueprint ownership status
owned_status = "Unowned"

# Component quantities required for Polyaramids production
polyaramids_requirements = {
    "Industrial Fibers": 1,
    "Oxidizing Compound": 1
}

# Specifications and attributes
polyaramids_specifications = {
    "example_use": "Used to make Hermetic Membranes, High-Tech Transmitters (P3)",
    "input_type": "P1 + P1",
    "tier": "P2",
    "more_info": "https://wiki.eveuniversity.org/Planetary_Commodities#:~:text=Gel,Tech%20Transmitter"
}

# Production details
polyaramids_production_details = {
    "facility_requirements": ["Advanced Industry Facility"],
    "production_time": 3600,  # 1 hour in seconds
    "invention": False,  # Not inventable (direct P2 production)
    "base_materials_efficiency": 0  # ME0
}
