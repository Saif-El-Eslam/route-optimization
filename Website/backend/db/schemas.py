from mongoengine import (
    Document,
    StringField,
    IntField,
    DateTimeField,
    ListField,
    DecimalField,
    ListField,
    BooleanField,
    ObjectIdField,
    DictField,
    ReferenceField

)


class Bus(Document):
    bus_id = StringField(required=True, max_length=20)  # license plate
    capacity = IntField()  # number of seats
    current_location = ListField(DecimalField(precision=6))  # [long, lat]
    locations = ListField(DictField(
        trip_id=ObjectIdField(required=True), action=StringField(choices=["pickup", "dropoff"], required=True),
        coordinates=ListField(DecimalField(precision=6))))  # list of trip ids, pick/drop and coordinates [(id, "pickup", [long, lat]), (id, "dropoff", [long, lat])]
    route = ListField(IntField())  # list of location ids 1->2->3->4->5->1
    time_windows = ListField(ListField(IntField()))  # list of time windows
    assigned_trips = ListField(ObjectIdField())  # list of trip ids
    status = StringField(max_length=20)  # "Active" or "Inactive"
    depot = ListField(DecimalField(precision=6))  # [long, lat]


# class Trip(Document):
#     bus_id = StringField(max_length=50)  # license plate
#     rider_id = StringField(max_length=50)  # rider id
#     request_time = DateTimeField()  # time of request
#     pickup_time = DateTimeField()  # time of pickup
#     arrival_time = DateTimeField()  # time of arrival
#     pickup_location = ListField(DecimalField(precision=6))  # [long, lat]
#     dropoff_location = ListField(DecimalField(precision=6))  # [long, lat]
#     status = StringField(max_length=20)  # "Pending", "Active", "Completed"


class User(Document):
    first_name = StringField(max_length=50, required=True)
    last_name = StringField(max_length=50, required=True)
    email = StringField(max_length=100, required=True)
    # phone_number = StringField(max_length=15)
    password = StringField(max_length=100, required=True)
    # 0: rider, 1: driver, 2: admin
    role = IntField(max_length=2, required=True)
    bus_id = StringField(max_length=20)
    license_number = StringField(max_length=20, required=(role == 1))
    verified = BooleanField()
    token = StringField(max_length=200)

    ride_id = StringField(max_length=50)


# class Rider(Document):
#     username = StringField(max_length=50)
#     email = StringField(max_length=100)
#     phone_number = StringField(max_length=15)

# class Driver(Document):
#     first_name = StringField(max_length=50)
#     last_name = StringField(max_length=50)
#     license_number = StringField(max_length=20)


class Ride(Document):
    rider = ReferenceField(User)
    bus = ReferenceField(Bus)
    request_time = DateTimeField()
    pickup_time = DateTimeField()
    dropoff_time = DateTimeField()
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
