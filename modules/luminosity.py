
def select_proxy(my_data):
    import modules.messages as msg
    while True:
        choice = msg.lumi_menu()
        if choice == "1":
            print("GBM amplitude set as the preferred Luminosity proxy.")
            if my_data["GBM_data"] == None:
                print("Make sure to also provide GBM data!")
                print()
            my_data["Luminosity_proxy"] = "GBM"
            break
        elif choice == "2":
            if my_data["BAT_data"] == None:
                print("BAT data unavailable. Please provide BAT data first!")
                print()
            else:
                my_data["Luminosity_proxy"] = "BAT"
                print("BAT count rates set as the preferred Luminosity proxy.")
                break
        else:
            msg.menu_err()   
    return my_data
