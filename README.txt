# Package Delivery System

## Overview

This project is a package delivery system for the Western Governors University Parcel Service (WGUPS). The system is designed to load packages onto trucks, calculate the optimal delivery route based on distances, and track the status of each package.

## Features

- Load package, distance, and location data from CSV files.
- Use a hash table to store and retrieve package information efficiently.
- Load packages onto trucks based on specific rules and constraints.
- Calculate the distance between locations and sort packages for optimal delivery.
- Track the status of each package, including delivery time and current status.
- Provide user interaction to query package status and total mileage.

## Files

- `main.py`: The main script that runs the program.
- `Package.py`: Contains the `Package` class definition.
- `Truck.py`: Contains the `Truck` class definition.
- `hash_map.py`: Contains the `hashmap` class definition.
- `CSV/Distance.csv`: CSV file containing distance data between locations.
- `CSV/Locations.csv`: CSV file containing location data.
- `CSV/Packages.csv`: CSV file containing package data.

## Installation

1. Clone the repository to your local machine.
2. Ensure you have Python installed (version 3.6 or higher).
3. Install any required dependencies (if any).

## Usage

1. Run the `main.py` script to start the program.
2. Follow the on-screen prompts to interact with the system.

### Main Menu Options

1. **Print All Package Status and Total Mileage**: Prints the status of all packages and the total mileage of all trucks.
2. **Get a Single Package Status with a Time**: Allows you to query the status of a specific package at a given time.
3. **Get All Package Status with a Time**: Allows you to query the status of all packages at a given time.
4. **Exit the Program**: Exits the program.

## Data Loading

- **Distance Data**: Loaded from `CSV/Distance.csv`.
- **Location Data**: Loaded from `CSV/Locations.csv`.
- **Package Data**: Loaded from `CSV/Packages.csv` and stored in a hash table.

## Package Loading Rules

- Packages that must be delivered together are loaded onto Truck 1.
- Specific packages are loaded onto Truck 2.
- Late packages are loaded onto Truck 3.
- Remaining packages are distributed among the trucks based on available capacity.

## Distance Calculation

- The distance between two locations is calculated using the data from `CSV/Distance.csv`.
- If the distance is not directly available, the reverse distance is used.

## Sorting Packages

- Packages are sorted based on the distance from the current address of the truck.
- The nearest package is selected and added to the truck's delivery route.

## Tracking Package Status

- The status of each package is tracked, including delivery time and current status.
- The status can be queried at any given time.

## Example

To run the program, execute the following command in your terminal:

```bash
python main.py