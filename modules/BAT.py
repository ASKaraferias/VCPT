"""
Module containing all the BAT relevant methods.
"""
from modules.defaults import my_data
default_data = my_data()

def read(my_data):
    import modules.helpers as hlp

    if my_data["BAT_data"] != None:
        while True:
            print()
            print("Be careful! You have already stored BAT data! Would you like to start over?")
            print("(all the existing BAT data will be lost)")
            print()
            response = input("Are you certain you want to continue[y/N]? ").strip()
            if response == "" or response in hlp.negatives:
                print("Continuing with stored data!")
                return my_data
            elif response in hlp.positives:
                print("Deleting BAT data now!")
                my_data["BAT_data"] = None
                break
            else:
                print("Please enter a valid choice!")
            print()
    
    from astropy.io import fits
    from scipy.signal import savgol_filter
    while True:
        filename = input("Give the BAT fits file location: ").strip()
        try:
            """
            Reading the data from the fits file:
            """
            fits_raw = fits.open(filename)
            data = fits_raw[1].data
            date = data.field(0)[data.field(1)>0]
            rate = data.field(1)[data.field(1)>0]
            rate_sm = savgol_filter(rate, 21, 3) #Smooth them out a bit.
            rate = rate_sm
            rate_err = data.field(2)[data.field(1)>0]
            print()
            print("Success!")
            print()
            break
        except:
            print("OOPS! An error occured! Please provide a valid BAT fits file!")

    my_data["BAT_data"] = {
            "dates" : date,
            "rate" : rate,
            "rate_err" : rate_err
            }

    return my_data
