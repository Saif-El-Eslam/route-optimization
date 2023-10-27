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


def get_bus(bus_id):
    return Bus.objects(bus_id=bus_id).first()


def get_all_buses():
    return Bus.objects()


def update_bus(bus_id, data):
    bus = get_bus(bus_id)
    if bus:
        for key, value in data.items():
            setattr(bus, key, value)
        bus.save()
    return bus


def delete_bus(bus_id):
    bus = get_bus(bus_id)
    if bus:
        bus.delete()


# Trip Services
def create_trip(data):
    trip = Trip(**data)
    trip.save()
    return trip


def get_trip(trip_id):
    return Trip.objects(id=trip_id).first()


def update_trip(trip_id, data):
    trip = get_trip(trip_id)
    if trip:
        for key, value in data.items():
            setattr(trip, key, value)
        trip.save()
    return trip


def delete_trip(trip_id):
    trip = get_trip(trip_id)
    if trip:
        trip.delete()


# Rider Services
def create_rider(data):
    rider = Rider(**data)
    rider.save()
    return rider


def get_rider(rider_id):
    return Rider.objects(id=rider_id).first()


def update_rider(rider_id, data):
    rider = get_rider(rider_id)
    if rider:
        for key, value in data.items():
            setattr(rider, key, value)
        rider.save()
    return rider


def delete_rider(rider_id):
    rider = get_rider(rider_id)
    if rider:
        rider.delete()


# Ride Request Services
def create_ride_request(data):
    ride_request = RideRequest(**data)
    ride_request.save()
    return ride_request


def get_ride_request(ride_request_id):
    return RideRequest.objects(id=ride_request_id).first()


def get_ride_requests_by_rider_id(rider_id):
    return RideRequest.objects(rider_id=rider_id)


def get_ride_requests_by_status(status):
    return RideRequest.objects(status=status)


def get_all_ride_requests():
    return RideRequest.objects()


def update_ride_request(ride_request_id, data):
    ride_request = get_ride_request(ride_request_id)
    if ride_request:
        for key, value in data.items():
            setattr(ride_request, key, value)
        ride_request.save()
    return ride_request


def delete_ride_request(ride_request_id):
    ride_request = get_ride_request(ride_request_id)
    if ride_request:
        ride_request.delete()


# Driver Services
def create_driver(data):
    driver = Driver(**data)
    driver.save()
    return driver


def get_driver(driver_id):
    return Driver.objects(id=driver_id).first()


def update_driver(driver_id, data):
    driver = get_driver(driver_id)
    if driver:
        for key, value in data.items():
            setattr(driver, key, value)
        driver.save()
    return driver


def delete_driver(driver_id):
    driver = get_driver(driver_id)
    if driver:
        driver.delete()


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
