import datetime
from website.models import Service, Booking
def check_availability(Service, Time_From, Time_To):
    avail_list = []
    Bookings = Booking.object.filter(service=Service)
    for booking in Bookings:
        if booking.Time_From > Time_To or booking.Time_To < Time_From:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)