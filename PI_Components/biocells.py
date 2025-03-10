# Biocells data structure

# Display name for the dropdown menu
display_name = "Biocells"

# Blueprint ownership status
owned_status = "Unowned"

# Component quantities required for Biocells production
biocells_requirements = {
    "Precious Metals": 1,
    "Biofuels": 1
}

# Specifications and attributes
biocells_specifications = {
    "example_use": "Used in capital ship components; component for Transcranial Microcontrollers (P3)",
    "input_type": "P1 + P1",
    "tier": "P2",
    "more_info": "https://wiki.eveuniversity.org/Planetary_Commodities#:~:text=Image%3A%20Barren%20Planet%20%20Precious,Biotech%20Research%20Reports%2C%20Smartfab%20Units"
}

# Production details
biocells_production_details = {
    "facility_requirements": ["Advanced Industry Facility"],
    "production_time": 3600,  # 1 hour in seconds
    "invention": False,  # Not inventable (direct P2 production)
    "base_materials_efficiency": 0  # ME0
}
