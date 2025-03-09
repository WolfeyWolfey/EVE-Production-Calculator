# EVE Online Production Calculator

A Python application for calculating resource requirements for manufacturing ships and components in EVE Online.

## Features

- **Ore Refining Calculator:** Calculate mineral yields from different asteroid ore types
- **Retriever Production:** View and calculate mineral requirements for building Retriever mining barges
- **Bowhead Production:** Calculate the minerals and PI materials needed for capital components used in Bowhead freighter construction
- **Planetary Interaction (PI) Data:** Information about planetary materials and their uses (future calculator planned)

## Requirements

- Python 3.6 or higher
- Tkinter (included with most Python installations)

## Installation

No installation is required beyond having Python with Tkinter.

1. Clone or download this repository
2. Run `python main.py` to start the application

## Project Structure

The project is organized into modules for better maintainability:

- `main.py` - Main entry point for the application
- `gui.py` - Contains the GUI code using Tkinter
- `ore_data.py` - Data for asteroid ores and their refined mineral yields
- `retriever_data.py` - Blueprint requirements for the Retriever mining barge
- `capital_components_data.py` - Data for capital ship components
- `bowhead_data.py` - Specific requirements for Bowhead freighter construction
- `planetary_data.py` - Planetary Interaction (PI) materials data

## Usage

1. Launch the application using `python main.py`
2. Navigate between tabs to access different calculators:
   - **Ore Refining:** Select an ore type and input quantity to calculate mineral yields
   - **Retriever Production:** View mineral requirements for Retriever production, calculate batch requirements
   - **Bowhead Production:** Select components to include in calculation, view total mineral and PI material requirements
   - **PI Calculator:** (Coming soon) Calculate planetary material requirements

## Extending the Application

The modular design makes it easy to add new features:

1. To add new ore types or update existing data, modify `ore_data.py`
2. To add new ship blueprints, create a new data file following the pattern in `retriever_data.py`
3. To add production chains for other capital ships, modify `capital_components_data.py` and create new ship-specific files

## Data Sources

The data in this application is based on EVE Online game data. Note that game mechanics and values may change with game updates.

## License

This project is provided for educational purposes. EVE Online is a registered trademark of CCP Games.
