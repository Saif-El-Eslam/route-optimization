from mongoengine import Document, StringField, IntField, DateTimeField, ListField, DecimalField

class Bus(Document):
    bus_number = StringField(required=True, max_length=20)
    capacity = IntField()
    current_location = StringField(max_length=100)
    status = StringField(max_length=20)

class Trip(Document):
    bus_id = IntField()
    driver_id = IntField()
    route = StringField(max_length=100)
    departure_time = DateTimeField()
    arrival_time = DateTimeField()
    status = StringField(max_length=20)

class Rider(Document):
    username = StringField(max_length=50)
    email = StringField(max_length=100)
    phone_number = StringField(max_length=15)

class RideRequest(Document):
    rider_id = IntField()
    request_time = DateTimeField()
    start_location = StringField(max_length=100)
    end_location = StringField(max_length=100)
    status = StringField(max_length=20)

class AssignedRide(Document):
    ride_request_id = IntField()
    trip_id = IntField()
    assignment_time = DateTimeField()

class BusTripRider(Document):
    assignment_id = IntField()
    rider_id = IntField()
    arrival_time = DateTimeField()
    status = StringField(max_length=20)

class Driver(Document):
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    license_number = StringField(max_length=20)

class PaymentTransaction(Document):
    ride_request_id = IntField()
    payer_id = IntField()
    payee_id = IntField()
    amount = DecimalField(precision=2)
    payment_method = StringField(max_length=20)
    transaction_time = DateTimeField()

class Review(Document):
    ride_request_id = IntField()
    reviewer_id = IntField()
    rating = IntField()
    comment = StringField()
    review_time = DateTimeField()
