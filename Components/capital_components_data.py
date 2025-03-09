# Capital Ship Components data for EVE Online Production Calculator
# Material requirements for individual capital components

# Display name for the dropdown menu
display_name = "Capital Ship Components"

# Blueprint ownership status
owned_status = "Unowned"

capital_component_data = {
    "Capital Propulsion Engine": {
        "minerals": {"Tritanium": 457050, "Pyerite": 110416, "Mexallon": 41994, "Isogen": 6938, "Nocxium": 2110, "Zydrine": 604, "Megacyte": 302},
        "pi_materials": {"Self-Harmonizing Power Core": 1},
        "blueprint_owned": owned_status
    },
    "Capital Armor Plates": {
        "minerals": {"Tritanium": 473141, "Pyerite": 111118, "Mexallon": 43324, "Isogen": 7109, "Nocxium": 2141, "Zydrine": 682, "Megacyte": 304},
        "pi_materials": {"Organic Mortar Applicators": 5},
        "blueprint_owned": owned_status
    },
    "Capital Shield Emitter": {
        "minerals": {"Tritanium": 400000, "Pyerite": 100000, "Mexallon": 40000, "Isogen": 6500, "Nocxium": 2000, "Zydrine": 500, "Megacyte": 300},  # Updated with estimated values
        "pi_materials": {"Recursive Computing Module": 1},
        "blueprint_owned": owned_status
    },
    "Capital Cargo Bay": {
        "minerals": {"Tritanium": 874902, "Pyerite": 72154, "Mexallon": 24616, "Isogen": 3504, "Nocxium": 998, "Zydrine": 286, "Megacyte": 64},
        "pi_materials": {},
        "blueprint_owned": owned_status
    },
    "Capital Construction Parts": {
        "minerals": {"Tritanium": 349387, "Pyerite": 84399, "Mexallon": 33956, "Isogen": 4594, "Nocxium": 1377, "Zydrine": 242, "Megacyte": 95},
        "pi_materials": {},
        "blueprint_owned": owned_status
    },
    "Capital Ship Maintenance Bay": {
        "minerals": {"Tritanium": 519083, "Pyerite": 170948, "Mexallon": 47981, "Isogen": 8109, "Nocxium": 2215, "Zydrine": 411, "Megacyte": 187},
        "pi_materials": {"Integrity Response Drones": 1},
        "blueprint_owned": owned_status
    }
}

# Production information for capital components
capital_component_production = {
    "facility_options": ["Outpost", "Engineering Complex", "Assembly Array"],
    "base_time": 14400,  # 4 hours base time
    "industry_skill_effect": 0.04,  # 4% reduction per level
    "required_blueprints": True  # Each component requires its own blueprint
}

# PI materials required for capital components
pi_materials_info = {
    "Self-Harmonizing Power Core": {
        "tier": "P4",
        "inputs": ["Nanotransistors", "Ukomi Superconductors"]
    },
    "Recursive Computing Module": {
        "tier": "P4",
        "inputs": ["Nanite Compound", "High-Tech Transmitters"]
    },
    "Organic Mortar Applicators": {
        "tier": "P4",
        "inputs": ["Vaccines", "Livestock"]
    },
    "Integrity Response Drones": {
        "tier": "P4",
        "inputs": ["Robotics", "Synthetic Synapses"]
    }
}
