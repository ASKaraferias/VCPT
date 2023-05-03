def read(my_data):
    import modules.helpers as hlp
    if my_data["GBM_data"] == None:
        print()
        print("Please provide GBM data first!")
        print()
        return my_data
    if my_data["Reference"] != None:
        print()
        print("Existing reference data will be deleted!")
        print()
        my_data["Reference"] = None

    print("In order to scale our luminosity proxy, \
we need to know the Flux of the source on at least one date. \
Said reference date should be in the range of your data.")
    while True:
        print()
        print("Provide a reference DATE [MJD] and the FLUX [erg/s/cm^2] on that date.")
        while True:
            try:
                date = float(input("DATE [MJD]: ").strip())
                if not (my_data["GBM_data"]["dates"][0] <= date <= my_data["GBM_data"]["dates"][-1]):
                    print("The date should be in the range of your data!")
                else:
                    break
            except:
                print("The date should be a number!")

        while True:
            try:
                flux = float(input("FLUX [erg/s/cm^2]: ").strip())
                break
            except:
                print("The flux should be a number!")
        
        if my_data["Reference"] == None:
            my_data["Reference"] = {
                    "dates" : [ date ],
                    "flux" : [ flux ]
                    }
        else:
            my_data["Reference"]["dates"].append(date)
            my_data["Reference"]["flux"].append(flux)
        
        while True:
            more = False
            response = input("Do you want to provide reference data in more dates[y/N]? ").strip()
            if (response in hlp.negatives) or (response == ""):
                break
            elif response in hlp.positives:
                print()
                print("You will now be prompted to provide additional reference data.")
                more = True
                break
            else:
                print()
                print("Please provide a valid response!")
                print()
        if more != True: break

    return my_data
