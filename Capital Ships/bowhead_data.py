# Bowhead Freighter blueprint requirements
# This file contains the specific requirements for the Bowhead freighter

# Display name for the dropdown menu
display_name = "Bowhead Freighter"


# Blueprint ownership status
owned_status = "Unowned"

# Component quantities required for Bowhead construction
bowhead_requirements = {
    "Capital Propulsion Engine": 10,
    "Capital Armor Plates": 5,
    "Capital Shield Emitter": 5,
    "Capital Cargo Bay": 8,
    "Capital Construction Parts": 5,
    "Capital Ship Maintenance Bay": 7
}

# Ship specifications and attributes
bowhead_specifications = {
    "cargohold_capacity": 300000,
    "ship_maintenance_bay": 1350000,
    "hull_hp": 54000,
    "armor_hp": 54000,
    "shield_hp": 67500,
    "sig_radius": 500,
    "max_velocity": 139,
    "mass": 890000000,
    "volume": 950000,
    "ship_class": "Freighter (Industrial)",
    "manufacturer": "ORE"
}

# Production details
bowhead_production_details = {
    "production_time": 172800,  # 48 hours in seconds
    "facility_requirements": ["Capital Ship Assembly Array", "Sotiyo Engineering Complex"],
    "skills_required": {
        "Industry": 5,
        "Advanced Industry": 4,
        "Capital Ship Construction": 3,
        "Science": 4
    },
    "invention": False,  # Not inventable (direct T1 production)
    "base_materials_efficiency": 0  # ME0
}
