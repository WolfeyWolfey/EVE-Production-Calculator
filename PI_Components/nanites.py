# Nanites data structure

# Display name for the dropdown menu
display_name = "Nanites"

# Blueprint ownership status
owned_status = "Unowned"

# Component quantities required for Nanites production
nanites_requirements = {
    "Reactive Metals": 1,
    "Bacteria": 1
}

# Specifications and attributes
nanites_specifications = {
    "example_use": "Used in Nanite Repair Paste (consumable); input for Biotech Reports, Transcranial Microcontrollers (P3)",
    "input_type": "P1 + P1",
    "tier": "P2",
    "more_info": "https://wiki.eveuniversity.org/Planetary_Commodities#:~:text=Image%3A%20Lava%20Planet%20%20Silicon,Biotech%20Research%20Reports%2C%20Transcranial%20Microcontroller"
}

# Production details
nanites_production_details = {
    "facility_requirements": ["Advanced Industry Facility"],
    "production_time": 3600,  # 1 hour in seconds
    "invention": False,  # Not inventable (direct P2 production)
    "base_materials_efficiency": 0  # ME0
}
