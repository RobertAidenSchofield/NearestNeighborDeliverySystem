class Package:
    def __init__(self, ID, address, city, zipcode, deadline, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None
        self.truck = None

    def __str__(self):

        return "%s,%s,%s,%s,%s,%s,%s,%s,%s," % (
            self.ID,
            self.address,
            self.city,
            self.zipcode,
            self.deadline,
            self.weight,
            self.status,
            self.delivery_time,
            self.truck,
        )


    def delivery_status(self, time):
        if self.delivery_time < time:
            self.status = "Delivered"
        elif self.delivery_time > time:
            self.status = "En Route"
        else:
            self.status = "At Hub"