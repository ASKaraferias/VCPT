def init(my_data):
    gbm_available = False
    bat_available = False
    if not my_data["GBM_data"] == None:
        print()
        print("Available GBM fields: DATE, FREQ, AMP")
        gbm_available = True
    if not my_data["BAT_data"] == None:
        print()
        print("Available BAT fields: DATE, RATE")
        bat_available = True
    if gbm_available == False and bat_available == False:
        print()
        print("You have to provide some data first!")
        print()
        return my_data

    while True:
        response = input(">>").strip()
        if response == "0": break
    
    return my_data
