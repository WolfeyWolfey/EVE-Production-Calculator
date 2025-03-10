# Providence Freighter blueprint requirements

# Display name for the dropdown menu
display_name = "Providence Freighter"

# Blueprint ownership status
owned_status = "Unowned"

# Component quantities required for Providence construction
providence_requirements = {
    "Capital Propulsion Engine": 15,
    "Capital Armor Plates": 5,
    "Capital Cargo Bay": 40,
    "Capital Construction Parts": 5,
    "U-C Trigger Neurolink Conduit": 16,
    "Radar-FTL Interlink Communicator": 1,
    "Auto-Integrity Preservation Seal": 400,
    "Life Support Backup Unit": 200,
    "Capital Core Temperature Regulator": 1
}

# Total mineral requirements
providence_minerals = {
    "Tritanium": 3050000,
    "Pyerite": 11055000,
    "Mexallon": 3050000,
    "Isogen": 850000,
    "Nocxium": 85750,
    "Zydrine": 43450,
    "Megacyte": 21750
}

# Planetary and advanced material requirements
providence_pi_materials = {
    "Self-Harmonizing Power Core": 40,
    "Organic Mortar Applicators": 25,
    "Integrity Response Drones": 25,
    "Supertensile Plastics": 1600,
    "Test Cultures": 1600,
    "Viral Agent": 1600,
    "Nanites": 1600,
    "Pressurized Oxidizers": 25160,
    "Reinforced Carbon Fiber": 35160,
    "Hypnagogic Neurolink Enhancer": 640,
    "Ultradian-Cycling Neurolink Stabilizer": 16,
    "Chiral Structures": 5000,
    "Water": 5000
}

# Ship specifications and attributes
providence_specifications = {
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
providence_production_details = {
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
