# Genetically Enhanced Livestock data structure

# Display name for the dropdown menu
display_name = "Genetically Enhanced Livestock"

# Blueprint ownership status
owned_status = "Unowned"

# Component quantities required for Genetically Enhanced Livestock production
genetically_enhanced_livestock_requirements = {
    "Biomass": 1,
    "Proteins": 1
}

# Specifications and attributes
genetically_enhanced_livestock_specifications = {
    "example_use": "(No direct use) Used to make Hermetic Membranes (P3)",
    "input_type": "P1 + P1",
    "tier": "P2",
    "more_info": "https://wiki.eveuniversity.org/Planetary_Commodities#:~:text=Image%3A%20Oceanic%20Planet%20%20105,Livestock%20None%20known%20Hermetic%20Membranes"
}

# Production details
genetically_enhanced_livestock_production_details = {
    "facility_requirements": ["Advanced Industry Facility"],
    "production_time": 3600,  # 1 hour in seconds
    "invention": False,  # Not inventable (direct P2 production)
    "base_materials_efficiency": 0  # ME0
}
