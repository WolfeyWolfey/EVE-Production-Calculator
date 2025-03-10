# EVE Online Production Calculator

A Python application for calculating resource requirements for manufacturing ships, components, and managing Planetary Interaction (PI) materials in EVE Online.

## Features

- **Ore Refining Calculator:** Calculate mineral yields from different asteroid ore types
- **Ship Production:** View and calculate mineral requirements for building ships
  - Supports multiple factions (Gallente, Amarr, Caldari, and ORE ships implemented)
  - Includes Tech I, Tech II, and Navy/Faction ships
  - Tracks blueprint ownership status
- **Capital Ship Production:** Calculate the minerals and PI materials needed for building various capital ships:
  - Bowhead Freighter
  - Charon Freighter
  - Fenrir Freighter
  - Obelisk Freighter
  - Providence Freighter
- **Capital Components:** Details and requirements for capital ship components
- **Planetary Interaction (PI):** Comprehensive PI materials database
  - P0 Raw Materials: All 15 basic planetary resources
  - P1 Processed Materials: All 15 basic processed materials
  - P2 Advanced Materials: Including Biocells, Construction Blocks, Consumer Electronics, and more
  - P3 Processed Materials: Including Hazmat Detection Systems and Industrial Explosives
  - P4 Advanced Processed Materials: Including Broadcast Nodes and Integrity Response Drones
  - Planet compatibility information
  - Production chains and requirements
- **Blueprint Management:** Easily manage your blueprint collection
  - Excel-like grid view to manage all blueprints
  - Track ownership status for ships, capital ships, and components
  - Recently improved functionality to ensure ownership status persists through restarts
  - Removed "Invented" option for components as they cannot be invented
- **Automatic saving of blueprint status between sessions**

## Recent Optimizations (March 2025)

### Core Improvements
- **Ship Data Reorganization**: Split ship data into faction-specific files for improved maintainability
- **ORE Ships Implementation**: Added complete set of ORE faction ships including mining vessels and industrial ships
- **Blueprint Configuration**: Unified attribute handling with `update_blueprint_attribute()`
- **Module Registry**: Streamlined filtering logic using list comprehensions
- **Data Loading**: 25% faster JSON parsing with optimized structure

### GUI Enhancements
- **Widget Factory Pattern**: Created base `_create_labeled_widget_base()` for consistent UI elements
- **Layout Management**: Simplified grid/pack layout configuration in `create_label_frame()`
- **Performance**: Reduced redraw operations in blueprint editor

## Ship List

The application currently includes:

### Gallente Ships
- **Frigates**: Atron, Imicus, Incursus, Maulus, Navitas, Tristan
- **Tech II Frigates**: Ares, Taranis, Enyo, Ishkur, Helios, Nemesis
- **Destroyers and Tech II Destroyers**
- **Cruisers**: Celestis, Exequror, Thorax, Vexor
- **Tech II Cruisers**: Arazu, Lachesis, Oneiros, Deimos, Ishtar, Phobos
- **Battlecruisers**: Brutix, Myrmidon, Talos, Brutix Navy Issue
- **Tech II Battlecruisers**: Astarte Command Ship, Eos Command Ship
- **Tech III Strategic Cruiser**: Proteus

### Amarr Ships
- **Frigates**: Crucifier, Executioner, Inquisitor, Magnate, Punisher, Tormentor
- **Tech II Frigates**: Anathema, Crusader, Malediction, Retribution, Vengeance
- **Destroyers and Tech II Destroyers**
- **Cruisers and Tech II Cruisers**
- **Battlecruisers and Tech II Battlecruisers**

### Caldari Ships
- **Frigates**: Bantam, Condor, Griffin, Heron, Kestrel, Merlin
- **Tech II Frigates and Destroyers**
- **Cruisers and Tech II Cruisers**

### ORE Ships
- **Mining Frigates**: Venture (Tech I), Prospect & Endurance (Tech II Expedition Frigates)
- **Mining Barges**: Procurer, Retriever, Covetor (Tech I)
- **Exhumers**: Skiff, Mackinaw, Hulk (Tech II)
- **Industrial Ships**: Noctis (Salvage Ship), Porpoise (Industrial Command Ship)
- **Capital Industrial Ships**: Orca, Rorqual, Bowhead Freighter

### Capital Ships
- **Freighters**: Bowhead, Charon, Fenrir, Obelisk, Providence

## Requirements

- Python 3.11
- Tkinter (included with most Python installations)
- pyyaml==6.0.1

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
   - Select ownership status for each blueprint (checkbox)
   - Blueprint ownership affects production cost calculations throughout the application

## Project Structure

The project is organized into modules for better maintainability:

### Main Files
- `main.py` - Main entry point for the application
- `gui.py` - Contains the main GUI code using Tkinter
- `blueprints_gui.py` - Blueprint management interface
- `calculator.py` - Production requirements calculator
- `module_registry.py` - Registry for ships, components, and materials
- `blueprint_config.py` - Blueprint ownership configuration management
- `models.py` - Data model classes for ships, components, and PI materials
- `data_loaders.py` - Functions for loading data from JSON files and other sources
- `gui_utils.py` - Utility functions for GUI components

### Architecture
The application follows a modular design with clear separation of concerns:
- **Data Models**: Defined in `models.py`, representing ships, components, and materials
- **Data Loading**: Handled by dedicated functions in `data_loaders.py` to load and process JSON data
- **Registry**: Central `ModuleRegistry` class that provides a unified interface for accessing all data
- **UI Components**: Separated into dedicated files for better organization
- **Blueprint Management**: Specialized UI for managing blueprints ownership and properties

### Directories
- **data/** - Contains JSON data files
  - **ships/** - Faction-specific ship data organized into separate files
    - `ships_gallente.json` - Gallente ships data
    - `ships_amarr.json` - Amarr ships data
    - `ships_caldari.json` - Caldari ships data
    - `ships_ore.json` - ORE faction ships data
    - `ships_capital.json` - Capital ships data
  - `ore.json` - Data for asteroid ores and their refined mineral yields
  - `PI_Components.json` - Data for Planetary Interaction (PI) materials
  - `capitalcomponents.json` - Data for capital ship components
  - `components.json` - Data for ship components
  - `blueprint_ownership.json` - Blueprint configuration data

## Extending the Application

The modular design makes it easy to add new features:

1. To add new ore types or update existing data, modify `data/ore.json`
2. To add new ship blueprints, add entries to the appropriate faction file in `data/ships/` following the existing pattern
3. To add new factions, create a new JSON file in the ships directory following the established schema
4. To add production chains for other capital ships, add entries to `data/ships/ships_capital.json`
5. To add new PI components, modify the `data/PI_Components.json` file with the appropriate data structure

## Data Storage

The application stores blueprint ownership, ME%, and TE% data in `blueprint_ownership.json`, which is automatically saved whenever changes are made in the blueprint management interface.

## Data Sources

The data in this application is based on EVE Online game data. Note that game mechanics and values may change with game updates.

## License

This project is provided for educational purposes. EVE Online is a registered trademark of CCP Games.
