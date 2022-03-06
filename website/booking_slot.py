
from .models import Available_Day, Booking, Order    

def removeSlot(booking, Time_From, totalSlotTime, totalSlotTime2):
    time_list = booking.time_list
    if totalSlotTime2 != 0:
        numberdec = (totalSlotTime2 / 0.5) - 1
    else: 
        numberdec = 0
    remove_slot = Time_From + totalSlotTime + numberdec
    for v in range(Time_From, remove_slot + 1):
        time_list.remove(v)
        

    

    
            
        


