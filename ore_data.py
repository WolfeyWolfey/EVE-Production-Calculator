# Ore data for EVE Online Production Calculator
# Refining yields for 100 units of ore at 100% efficiency

ore_data = {
    "Veldspar": {"Tritanium": 400},
    "Scordite": {"Tritanium": 150, "Pyerite": 90},
    "Pyroxeres": {"Pyerite": 90, "Mexallon": 30},
    "Plagioclase": {"Tritanium": 175, "Mexallon": 70},
    "Omber": {"Pyerite": 90, "Isogen": 75},
    "Kernite": {"Mexallon": 60, "Isogen": 120},
    "Jaspet": {"Mexallon": 150, "Nocxium": 50},
    "Hemorphite": {"Isogen": 90, "Nocxium": 240},
    "Hedbergite": {"Pyerite": 450, "Nocxium": 120},
    "Gneiss": {"Pyerite": 2000, "Mexallon": 1500, "Isogen": 800},
    "Dark Ochre": {"Mexallon": 1360, "Isogen": 1200, "Nocxium": 320},
    "Crokite": {"Pyerite": 800, "Mexallon": 2000, "Nocxium": 800},
    "Bistot": {"Pyerite": 3200, "Mexallon": 1200, "Zydrine": 160},
    "Arkonor": {"Pyerite": 3200, "Mexallon": 1200, "Megacyte": 120},
    "Spodumain": {"Tritanium": 48000, "Pyerite": 1000, "Mexallon": 160, "Isogen": 80, "Nocxium": 40},
    "Mercoxit": {"Morphite": 140}
}

# Additional metadata about ore types can be added here
ore_security_levels = {
    "Veldspar": "High-sec",
    "Scordite": "High-sec",
    "Pyroxeres": "High-sec",
    "Plagioclase": "High-sec",
    "Omber": "Low-sec",
    "Kernite": "Low-sec",
    "Jaspet": "Low-sec",
    "Hemorphite": "Low-sec",
    "Hedbergite": "Low-sec",
    "Gneiss": "Null-sec",
    "Dark Ochre": "Null-sec",
    "Crokite": "Null-sec",
    "Bistot": "Null-sec",
    "Arkonor": "Null-sec",
    "Spodumain": "Null-sec",
    "Mercoxit": "Null-sec"
}
