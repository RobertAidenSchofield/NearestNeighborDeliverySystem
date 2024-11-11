class Truck:
    def __init__(
        self, ID,capacity, max_speed, load, packages, miles, address, depart_time
    ):
        self.ID = ID
        self.capacity = capacity
        self.max_speed = max_speed
        self.load = load
        self.packages = packages
        self.miles = miles
        self.address = address
        self.time = depart_time
        self.depart_time = depart_time

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s,%s," % (
            self.capacity,
            self.max_speed,
            self.load,
            self.packages,
            self.miles,
            self.address,
            self.depart_time,
        )
