# import schemas from location: route-optimization\Website\backend\db\schemas.py
from schemas import *


# User Services
def create_user(data):
    user = User(**data)
    user.save()
    return user


def get_user_by_id(user_id):
    return User.objects(id=user_id).first()


def get_user_by_email(email):
    return User.objects(email=email).first()


def get_users_by_role(role):
    return User.objects(role=role)


def get_user_by_token(token):
    return User.objects(token=token).first()



def update_user(user_id, data):
    user = get_user_by_id(user_id)
    if user:
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
    return user


def delete_user(user_id):
    user = get_user(user_id)
    if user:
        user.delete()


# Bus Services
def create_bus(data):
    bus = Bus(**data)
    bus.save()
    return bus



def get_bus_by_id(bus_id):
    return Bus.objects(bus_id=bus_id).first()


def get_all_buses():
    return Bus.objects()


def update_bus(bus_id, data):
    bus = get_bus_by_id(bus_id)
    if bus:
        for key, value in data.items():
            setattr(bus, key, value)
        bus.save()
    return bus


def delete_bus(bus_id):
    bus = get_bus(bus_id)
    if bus:
        bus.delete()


# Ride  Services
def create_ride(data):
    ride = Ride(**data)
    ride.save()
    return ride


def get_ride_by_id(ride_id):
    return Ride.objects(id=ride_id).first()


def get_rides_by_rider_id(rider_id):
    return Ride.objects(rider_id=rider_id)


def get_rides_by_status(status):
    return Ride.objects(status=status)


def get_all_rides():
    return Ride.objects()


def update_ride(ride_id, data):
    ride = get_ride_by_id(ride_id)
    if ride:
        for key, value in data.items():
            setattr(ride, key, value)
        ride.save()
    return ride


def delete_ride(ride_id):
    ride = get_ride_by_id(ride_id)
    if ride:
        ride.delete()



# Payment Transaction Services
def create_payment_transaction(data):
    payment_transaction = PaymentTransaction(**data)
    payment_transaction.save()
    return payment_transaction


def get_payment_transaction(payment_transaction_id):
    return PaymentTransaction.objects(id=payment_transaction_id).first()


def update_payment_transaction(payment_transaction_id, data):
    payment_transaction = get_payment_transaction(payment_transaction_id)
    if payment_transaction:
        for key, value in data.items():
            setattr(payment_transaction, key, value)
        payment_transaction.save()
    return payment_transaction


def delete_payment_transaction(payment_transaction_id):
    payment_transaction = get_payment_transaction(payment_transaction_id)
    if payment_transaction:
        payment_transaction.delete()


# Review Services
def create_review(data):
    review = Review(**data)
    review.save()
    return review


def get_review(review_id):
    return Review.objects(id=review_id).first()


def update_review(review_id, data):
    review = get_review(review_id)
    if review:
        for key, value in data.items():
            setattr(review, key, value)
        review.save()
    return review


def delete_review(review_id):
    review = get_review(review_id)
    if review:
        review.delete()
