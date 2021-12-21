import datetime
from website.models import Service, Booking
def check_availability(Service, bookin, bookout):
    avail_list = []
    Bookings = Booking.object.filter(service=Service)
    for booking in Bookings:
        if booking.booktime > bookout or booking.bookout < bookin:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)