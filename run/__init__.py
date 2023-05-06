
"""
The part of data post-proccessing and runing Ultranest.
"""
def main(my_data):
    if my_data["GBM_data"] == None:
        print()
        print("You need to provide GBM data and the Flux at at least one reference date.")
        print()
        return my_data
    elif my_data["Reference"] == None:
        print()
        print("You need to provide the Flux at at least one reference date.")
        print()
        return my_data

    import run.defaults as defaults
    post_data = defaults.post_data(my_data)

    if my_data["Luminosity_proxy"] == "BAT":
        post_data["INTENS"] = my_data["BAT_data"]["rate"]
        post_data["INTENS_ERR"] = my_data["BAT_data"]["rate_err"]
        post_data["INTENS_DATE"] = my_data["BAT_data"]["dates"]
        
    if my_data["Distance"] != "Unknown":
        post_data["DISTANCE"] = my_data["Distance"]
    else:
        post_data["DISTANCE"] = None

    import run.scale_intensity as scale
    post_data = scale.scale(my_data, post_data)
    
    if my_data["Gaps"] != None:
        post_data["GAP_SPOTS"] = my_data["Gaps"]["spots"]
        post_data["GAP_DATES"] = my_data["Gaps"]["dates"]

    import modules.messages as msg
    while True:
        choice = msg.select_tm()
        if choice == "1" or "":
            print()
            break
        elif choice == "2":
            print()
            post_data["TORQUE_MODEL"] = "W95"
            break
        elif choice == "3":
            print()
            post_data["TORQUE_MODEL"] = "H14"
            break
        elif choice == "4":
            print()
            post_data["TORQUE_MODEL"] = "B20"
            break
        else:
            print("Please input a valid choice.")

    import modules.helpers as hlp
    post_data["OUTPUT_DIR"] = hlp.ultranest_saves()

    import run.makescript as mk
    mk.init(post_data)
