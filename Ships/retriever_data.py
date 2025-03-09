# Retriever Mining Barge blueprint requirements
# Material quantities are for ME0 (no material efficiency research)

# Display name for the dropdown menu
display_name = "Retriever Mining Barge"

# Blueprint ownership status
owned_status = "Unowned"
retriever_requirements = {
    "Tritanium": 2742672,
    "Pyerite": 755721,
    "Mexallon": 86574,
    "Isogen": 57980,
    "Nocxium": 4937,
    "Zydrine": 2002,
    "Megacyte": 643
}

# Placeholder for additional Retriever-related data
# For example, variants, skills that affect production, etc.

# Add time required to manufacture
retriever_production_time = 14400  # seconds (4 hours)

# Add blueprint details
retriever_blueprint_details = {
    "Material Efficiency": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # ME research levels
    "Time Efficiency": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],      # TE research levels
    "Invention chance": None,                                   # T1 ship, no invention
    "Copy time": 1080,                                          # seconds (18 minutes)
    "ME research time base": 1260                               # seconds (21 minutes)
}
