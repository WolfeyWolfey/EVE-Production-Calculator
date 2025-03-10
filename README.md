# EVE Online Production Calculator

A Python application for calculating resource requirements for manufacturing ships, components, and managing Planetary Interaction (PI) materials in EVE Online.

## Features

- **Ore Refining Calculator:** Calculate mineral yields from different asteroid ore types
- **Ship Production:** View and calculate mineral requirements for building ships like the Retriever mining barge
- **Capital Ship Production:** Calculate the minerals and PI materials needed for building various capital ships:
  - Bowhead Freighter
  - Charon Freighter
  - Fenrir Freighter
  - Obelisk Freighter
  - Providence Freighter
- **Capital Components:** Details and requirements for capital ship components
- **Planetary Interaction (PI):** Comprehensive PI materials database
  - P0 Raw Materials: All 15 basic planetary resources
  - P2 Advanced Materials: Including Biocells, Construction Blocks, Consumer Electronics, and more
  - P3 Processed Materials: Including Hazmat Detection Systems and Industrial Explosives
  - Planet compatibility information
  - Production chains and requirements
- **Blueprint Management:** Easily manage your blueprint collection
  - Excel-like grid view to manage all blueprints at once
  - Track ownership status (Unowned/Owned/Invented) for each blueprint
  - Organized by categories: Ships, Capital Ships, Components, and Capital Components
  - Automatic saving of blueprint status

## Requirements

- Python 3.6 or higher
- Tkinter (included with most Python installations)

## Installation

No installation is required beyond having Python with Tkinter.

1. Clone or download this repository
2. Run `python main.py` to start the application

## Usage

1. Launch the application by running `python main.py`
2. Use the tabs to navigate between different calculators:
   - Ore Calculator: Calculate mineral yields from refining ores
   - Ship Production: View the material requirements for ships
   - Capital Ship Production: View the material, component, and PI requirements for capital ships
   - PI Calculator: View PI materials and their production chains
3. Manage your blueprint collection:
   - Go to File > Blueprints to open the blueprint management grid
   - Select ownership status (Unowned/Owned/Invented) for each blueprint
   - Click "Save All" to save your changes
   - Blueprint ownership affects production cost calculations throughout the application

## Project Structure

The project is organized into modules for better maintainability:

### Main Files
- `main.py` - Main entry point for the application
- `gui.py` - Contains the GUI code using Tkinter
- `eve_production_calculator.py` - Core logic for the application
- `ore_data.py` - Data for asteroid ores and their refined mineral yields
- `planetary_data.py` - Integration of Planetary Interaction (PI) materials data
- `blueprint_config.py` - Blueprint ownership configuration management

### Directories
- **Ships/** - Contains data for T1 and T2 ships
  - `retriever_data.py` - Blueprint requirements for Retriever mining barge
  
- **Capital Ships/** - Contains data for all capital ships
  - `bowhead_data.py` - Specific requirements for Bowhead freighter
  - `charon_data.py` - Specific requirements for Charon freighter
  - `fenrir_data.py` - Specific requirements for Fenrir freighter
  - `obelisk_data.py` - Specific requirements for Obelisk freighter
  - `providence_data.py` - Specific requirements for Providence freighter
  
- **Components/** - Contains data for ship components
  - `capital_components_data.py` - Data for capital ship components
  
- **PI_Components/** - Contains detailed data for all planetary interaction materials
  - **P0 Raw Materials:** aqueous_liquids.py, autotrophs.py, base_metals.py, etc.
  - **P2 Advanced Materials:** biocells.py, construction_blocks.py, consumer_electronics.py, etc.
  - **P3 Processed Materials:** hazmat_detection_systems.py, industrial_explosives.py, etc.

## Extending the Application

The modular design makes it easy to add new features:

1. To add new ore types or update existing data, modify `ore_data.py`
2. To add new ship blueprints, create a new data file in the Ships directory following the pattern in `retriever_data.py`
3. To add production chains for other capital ships, add a new file in the Capital Ships directory
4. To add new PI components, create a new file in the PI_Components directory with the appropriate data structure

## Data Sources

The data in this application is based on EVE Online game data. Note that game mechanics and values may change with game updates.

## License

This project is provided for educational purposes. EVE Online is a registered trademark of CCP Games.
