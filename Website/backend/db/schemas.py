from mongoengine import (
    Document,
    StringField,
    IntField,
    DateTimeField,
    ListField,
    DecimalField,
    ListField,
    BooleanField,
)


class Bus(Document):
    bus_id = StringField(required=True, max_length=20)
    capacity = IntField()
    current_location = ListField(DecimalField(precision=6))
    route = ListField(ListField(StringField(max_length=100)))
    assigned_trips = ListField(StringField(max_length=100))
    status = StringField(max_length=20)
    depot = ListField(DecimalField(precision=6))


class Trip(Document):
    bus_id = StringField(max_length=50)
    rider_id = StringField(max_length=50)
    request_time = DateTimeField()
    pickup_time = DateTimeField()
    arrival_time = DateTimeField()
    pickup_location = ListField(DecimalField(precision=6))
    dropoff_location = ListField(DecimalField(precision=6))
    status = StringField(max_length=20)


class User(Document):
    username = StringField(max_length=50)
    email = StringField(max_length=100)
    phone_number = StringField(max_length=15)
    password = StringField(max_length=20)
    role = IntField(max_length=2)
    # 0: rider, 1: driver, 2: admin
    license_number = StringField(max_length=20)
    verified = BooleanField(default=False)
    token = StringField(max_length=200)


# class Rider(Document):
#     username = StringField(max_length=50)
#     email = StringField(max_length=100)
#     phone_number = StringField(max_length=15)

# class Driver(Document):
#     first_name = StringField(max_length=50)
#     last_name = StringField(max_length=50)
#     license_number = StringField(max_length=20)


class RideRequest(Document):
    rider_id = StringField(max_length=50)
    request_time = DateTimeField()
    start_location = ListField(DecimalField(precision=6))
    end_location = ListField(DecimalField(precision=6))
    status = StringField(max_length=20)


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