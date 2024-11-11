# Load the distances from the CSV file
import csv
import datetime
import math

from Package import Package
import Truck
from hash_map import hashmap

# Load distances from CSV file
with open("CSV/Distance.csv") as distfile:
    distance_csv = csv.reader(distfile)
    distance_csv_list = []
    next(distance_csv)  # Skip first line to remove header
    for row in distance_csv:
        distance_csv_list.append(row)

# Load locations from CSV file
with open("CSV/Locations.csv") as locfile:
    locations_csv = csv.reader(locfile)
    locations_csv_list = []
    next(locations_csv)  # Skip first line to remove header
    for row in locations_csv:
        locations_csv_list.append(row)

# Load packages from CSV file
with open("CSV/Packages.csv") as packfile:
    packages_csv = csv.reader(packfile)
    packages_csv_list = []
    next(packages_csv)  # Skip first line to remove header
    for row in packages_csv:
        packages_csv_list.append(row)

# Function to load packages from CSV file into a hash table
def hash_load(filename, hash_table):
    with open(filename) as package_file:
        package_data = csv.reader(package_file)
        next(package_data)  # Skip first line to remove header
        for package in package_data:  # Set attributes
            pack_id = int(package[0])
            pack_address = package[1]
            pack_city = package[2]
            pack_zipcode = package[4]
            pack_deadline = package[5]
            pack_weight = package[6]
            pack_status = "At Hub"

            # Create package object and insert into hash table
            package_obj = Package(pack_id, pack_address, pack_city, pack_zipcode, pack_deadline,
                                  pack_weight, pack_status)

            hash_table.insert(pack_id, package_obj)

# Function to calculate distance between two locations
def distance_between(x, y):
    distance = distance_csv_list[x][y]
    if distance == '':
        distance = distance_csv_list[y][x]
    return float(distance)

# Function to get index of a location in the locations list
def get_index(address):
    for row in locations_csv_list:
        if address in row[2]:
            return int(row[0])

# Initialize hash table
hash_table = hashmap()

# Function to load packages to trucks and sort them based on distance from current address
def load_trucks(trucks):
    loaded_packages = set()
    must_be_together = {13, 14, 15, 19, 16, 20}
    late_packages = {6, 25, 28, 32}
    t_2_pack = {3,9,18, 36, 38}

    # Handle 'must be together' packages and assign to Truck 1
    truck_1 = next((truck for truck in trucks if truck.ID == 1))
    if truck_1:
        for pid in must_be_together:
            pack = hash_table.lookup(pid)
            if pack and len(truck_1.packages) < truck_1.capacity:
                truck_1.packages.append(pack.ID)
                loaded_packages.add(pid)
            else:
                # Truck 1 is at capacity
                pass
    # Handle t_2_pack packages and assign to Truck 2
    truck_2 = next((truck for truck in trucks if truck.ID == 2))
    if truck_2:
        for pid in t_2_pack:
            pack = hash_table.lookup(pid)
            if pack and len(truck_2.packages) < truck_2.capacity:
                truck_2.packages.append(pack.ID)
                loaded_packages.add(pid)
            else:
                # Truck 2 is at capacity
                pass

    # Handle late_packages and assign to Truck 3
    truck_3 = next((truck for truck in trucks if truck.ID == 3))
    if truck_3:
        truck_3.depart_time = min(truck_1.time, truck_2.time)
        for pid in late_packages:
            pack = hash_table.lookup(pid)
            if pack and len(truck_3.packages) < truck_3.capacity:
                truck_3.packages.append(pack.ID)
                loaded_packages.add(pid)
            else:
                # Truck 3 is at capacity
                pass

    # Assign remaining packages to any available truck
    all_package_ids = set(range(1, len(packages_csv_list) + 1))
    remaining_packages = all_package_ids - loaded_packages

    for pid in remaining_packages:
        pack = hash_table.lookup(pid)
        if pack:
            # Assign to the next truck with available capacity
            for truck in trucks:
                if len(truck.packages) < truck.capacity:
                    truck.packages.append(pack.ID)
                    loaded_packages.add(pid)
                    break
            else:
                # All trucks are at capacity
                pass
    for truck in trucks:
        packages_list_load = []
        # Load packages to array for sorting
        for pack_id in truck.packages:
            pack = hash_table.lookup(pack_id)
            packages_list_load.append(pack)
        truck.packages.clear()

        # Sort packages by distance from current address
        while len(packages_list_load) > 0:
            nearest_distance = math.inf
            nearest_package = None

            # Check each package
            for pack in packages_list_load:
                distance = distance_between(get_index(truck.address), get_index(pack.address))
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_package = pack
            # Add nearest package to truck
            truck.packages.append(nearest_package.ID)
            # Remove nearest package from array
            packages_list_load.remove(nearest_package)

            # Update truck's address, time, and miles
            truck.address = nearest_package.address
            truck.miles += nearest_distance
            truck.time += datetime.timedelta(hours=nearest_distance / 18)
            # Update nearest package's status
            nearest_package.delivery_time = truck.time
            nearest_package.depart_time = truck.depart_time

# Create truck objects
truck_1 = Truck.Truck(1, 16, 18, None, [ ], 0,
                "4001 South 700 East", datetime.timedelta(hours=8))
truck_2 = Truck.Truck(2, 16, 18, None, [ ], 0,
                "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))
truck_3 = Truck.Truck(3, 16, 18, None, [ ], 0,
                "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

# Create list of trucks
trucks = [truck_1, truck_2, truck_3]

# Load packages to hash table
hash_load("CSV/Packages.csv", hash_table)

# Load packages to trucks and sort them based on distance from current address
load_trucks(trucks)

# Function to print all package status and total mileage
def print_all_package_status_and_total_mileage():
    total_miles = 0
    for truck in trucks:
        print(f"Truck {truck.ID} packages: {truck.packages}")
        total_miles += truck.miles
        for pack_id in truck.packages:
            pack = hash_table.lookup(pack_id)

            print(f"Package ID: {pack.ID}, Address: {pack.address},"
                  f"Status: {pack.status}, Delivery Time: {pack.delivery_time}")
    print(f"Total Mileage: {total_miles}")

# Function to get single package status with a time
def get_single_package_status_with_time(package_id, time):
    pack = hash_table.lookup(package_id)
    if pack.ID == 9 and time >= datetime.timedelta(hours=10, minutes=20, seconds=0):
        pack.address = "410 S. State St."
        pack.city = "Salt Lake City"
        pack.zipcode = "84111"
    if pack:
        pack.delivery_status(time)
        print(f"Package ID: {pack.ID}, Address: {pack.address},"
              f"Status: {pack.status}, Delivery Time: {pack.delivery_time}")
    else:
        print(f"Package with ID {package_id} not found.")

# Function to get all package status with a time
def get_all_package_status_with_time(time):
    total_miles = 0
    for truck in trucks:
        print(f"Truck {truck.ID} packages: {truck.packages}")
        total_miles += truck.miles
    print(f"Total Mileage: {total_miles}")
    for pack_id in range(1, len(packages_csv_list) + 1):
        get_single_package_status_with_time(pack_id, time)



# Main function to interact with the user
def main():
    while True:
        print("***************************************")
        print("1. Print All Package Status and Total Mileage")
        print("2. Get a Single Package Status with a Time")
        print("3. Get All Package Status with a Time")
        print("4. Exit the Program")
        print("***************************************")
        choice = input("Enter your choice: ")

        if choice == '1':
            print_all_package_status_and_total_mileage()
        elif choice == '2':
            package_id = int(input("Enter Package ID: "))
            time_str = input("Enter time (HH:MM:SS): ")
            time = datetime.timedelta(hours=int(time_str.split(':')[0]),
                                      minutes=int(time_str.split(':')[1]),
                                      seconds=int(time_str.split(':')[2]))
            get_single_package_status_with_time(package_id, time)
        elif choice == '3':
            time_str = input("Enter time (HH:MM:SS): ")
            time = datetime.timedelta(hours=int(time_str.split(':')[0]),
                                      minutes=int(time_str.split(':')[1]),
                                      seconds=int(time_str.split(':')[2]))
            get_all_package_status_with_time(time)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main()