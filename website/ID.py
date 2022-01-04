import random 
def OrderID():
    existing_IDs = []
    new = False
    while new == False:
        random_number = random.randint(1000, 1000000)
        if random_number in existing_IDs:
            new = False
        else:
            new = True
    existing_IDs.append(random_number)
    
    
    return random_number
    