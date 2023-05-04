"""
Module containing all the GBM relevant methods.
"""
from modules.defaults import my_data
default_data = my_data()

def read(my_data):
    import modules.helpers as hlp

    if my_data["GBM_data"] != None:
        while True:
            print()
            print("Be careful! You have already stored GBM data! Would you like to start over?")
            print("(all the existing GBM data will be lost)")
            print()
            response = input("Are you certain you want to continue[y/N]? ").strip()
            if response == "" or response in hlp.negatives:
                print("Continuing with stored data!")
                return my_data
            elif response in hlp.positives:
                print("Deleting GBM data now!")
                my_data["GBM_data"] = None
                break
            else:
                print("Please enter a valid choice!")
            print()
    
    from astropy.io import fits
    import pulsar_mod as pm
    while True:
        filename = input("Give the GBM fits file location: ").strip()
        try:
            """
            Reading the data from the fits file:
            """
            fits_raw = fits.open(filename)
            data = fits_raw[2].data
            date = data.field(3)[data.field(4) > 0]
            freq_raw = data.field(8)[data.field(4) > 0]
            freq_raw_err = data.field(9)[data.field(4) > 0]
            amp = data.field(17)[data.field(4) > 0]
            amp_err = data.field(18)[data.field(4) > 0]
            source = pm.pulsar(filename)
            source.binary_beta(time = None)
            freq = freq_raw * ( 1 - source.vel )
            freq_err = freq_raw_err
            print()
            print("Success!")
            print()
            break
        except:
            print("OOPS! An error occured! Please provide a valid GBM fits file!")
    my_data["GBM_data"] = {
            "dates" : date.tolist(),
            "freq" : freq.tolist(),
            "frew_err" : freq_err.tolist(),
            "amp" : amp.tolist(),
            "amp_err": amp_err.tolist()
            }

    return my_data
