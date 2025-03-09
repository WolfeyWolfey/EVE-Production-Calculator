# Planetary Interaction (PI) data for EVE Online
# This file contains information about planetary materials and their properties

# P0 Raw Materials (extractable from planets)
p0_materials = {
    "Aqueous Liquids": ["Oceanic", "Temperate", "Storm", "Gas"],
    "Base Metals": ["Barren", "Temperate", "Plasma", "Lava"],
    "Carbon Compounds": ["Temperate", "Ice", "Gas"],
    "Complex Organisms": ["Oceanic", "Temperate"],
    "Felsic Magma": ["Plasma", "Lava"],
    "Heavy Metals": ["Plasma", "Lava", "Barren"],
    "Ionic Solutions": ["Storm", "Gas"],
    "Microorganisms": ["Barren", "Temperate"],
    "Noble Gas": ["Ice", "Gas"],
    "Noble Metals": ["Barren", "Plasma"],
    "Non-CS Crystals": ["Plasma", "Lava", "Ice"],
    "Reactive Gas": ["Gas", "Storm"],
    "Suspended Plasma": ["Storm", "Plasma"],
    "Autotrophs": ["Temperate", "Oceanic"]
}

# P1 Processed Materials
p1_materials = {
    "Bacteria": {"input": "Microorganisms", "planets": ["Barren", "Temperate"]},
    "Biofuels": {"input": "Carbon Compounds", "planets": ["Temperate", "Ice", "Gas"]},
    "Biomass": {"input": "Complex Organisms", "planets": ["Oceanic", "Temperate"]},
    "Chiral Structures": {"input": "Non-CS Crystals", "planets": ["Plasma", "Lava", "Ice"]},
    "Electrolytes": {"input": "Ionic Solutions", "planets": ["Storm", "Gas"]},
    "Industrial Fibers": {"input": "Autotrophs", "planets": ["Temperate", "Oceanic"]},
    "Oxidizing Compound": {"input": "Reactive Gas", "planets": ["Gas", "Storm"]},
    "Oxygen": {"input": "Aqueous Liquids", "planets": ["Oceanic", "Temperate", "Storm", "Gas"]},
    "Plasmoids": {"input": "Suspended Plasma", "planets": ["Storm", "Plasma"]},
    "Precious Metals": {"input": "Noble Metals", "planets": ["Barren", "Plasma"]},
    "Proteins": {"input": "Complex Organisms", "planets": ["Oceanic", "Temperate"]},
    "Reactive Metals": {"input": "Base Metals", "planets": ["Barren", "Temperate", "Plasma", "Lava"]},
    "Silicon": {"input": "Felsic Magma", "planets": ["Plasma", "Lava"]},
    "Toxic Metals": {"input": "Heavy Metals", "planets": ["Plasma", "Lava", "Barren"]},
    "Water": {"input": "Aqueous Liquids", "planets": ["Oceanic", "Temperate", "Storm", "Gas"]}
}

# P2 Refined Commodities
p2_materials = {
    "Mechanical Parts": {
        "inputs": ["Precious Metals", "Reactive Metals"],
        "uses": ["Structure fuel", "T2 components", "Robotics"]
    },
    "Consumer Electronics": {
        "inputs": ["Chiral Structures", "Toxic Metals"],
        "uses": ["T2 components", "Research", "Robotics", "Supercomputers"]
    },
    "Construction Blocks": {
        "inputs": ["Toxic Metals", "Reactive Metals"],
        "uses": ["T2 components", "Starbase structures"]
    },
    "Coolant": {
        "inputs": ["Water", "Electrolytes"],
        "uses": ["Structure fuel", "Advanced electronics"]
    },
    "Enriched Uranium": {
        "inputs": ["Toxic Metals", "Precious Metals"],
        "uses": ["Structure fuel", "Starbase reactors"]
    },
    "Polyaramids": {
        "inputs": ["Industrial Fibers", "Oxidizing Compound"],
        "uses": ["Advanced composites", "Membranes", "Transmitters"]
    },
    "Rocket Fuel": {
        "inputs": ["Electrolytes", "Plasmoids"],
        "uses": ["T2 missiles production"]
    },
    "Superconductors": {
        "inputs": ["Water", "Plasmoids"],
        "uses": ["Advanced electronics", "Ukomi coils"]
    },
    "Test Cultures": {
        "inputs": ["Water", "Bacteria"],
        "uses": ["Biotech", "Vaccines", "Organic Mortar Applicators"]
    }
}

# P3 Advanced Commodities
p3_materials = {
    "Robotics": {
        "inputs": ["Consumer Electronics", "Mechanical Parts"],
        "uses": ["POS fuel", "Advanced ship production", "Integrity Response Drones"]
    },
    "Synthetic Synapses": {
        "inputs": ["Supertensile Plastics", "Biocells"],
        "uses": ["Wetware", "Integrity Response Drones"]
    },
    "Ukomi Superconductors": {
        "inputs": ["Superconductors", "Precious Metals"],
        "uses": ["Advanced components", "Self-Harmonizing Power Core"]
    },
    "Nanotransistors": {
        "inputs": ["Consumer Electronics", "Microfiber Shielding"],
        "uses": ["Capital ship construction", "Self-Harmonizing Power Core"]
    },
    "Vaccines": {
        "inputs": ["Livestock", "Test Cultures"],
        "uses": ["Medical components", "Organic Mortar Applicators"]
    }
}

# P4 Advanced Commodities (used in capital ship construction)
p4_materials = {
    "Self-Harmonizing Power Core": {
        "inputs": ["Nanotransistors", "Ukomi Superconductors"],
        "uses": ["Capital component: Capital Propulsion Engine"]
    },
    "Recursive Computing Module": {
        "inputs": ["Nanite Compound", "High-Tech Transmitters"],
        "uses": ["Capital component: Capital Shield Emitter"]
    },
    "Organic Mortar Applicators": {
        "inputs": ["Vaccines", "Livestock"],
        "uses": ["Capital component: Capital Armor Plates"]
    },
    "Integrity Response Drones": {
        "inputs": ["Robotics", "Synthetic Synapses"],
        "uses": ["Capital component: Capital Ship Maintenance Bay"]
    }
}
