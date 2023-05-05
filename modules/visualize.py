def gbmplot(data):
    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(data["GBM_data"]["dates"], data["GBM_data"]["freq"], "k.", markersize = 2)
    plt.xlabel("DATE [MJD]")
    plt.ylabel("FREQ [Hz]")
    plt.title("GBM Frequency timeseries.")
    plt.show(block = False)

def restrict(data, new_start, new_stop):
    """
    Calls helpers.restrict_by_date() for all available data,
    to limit everything between the new start and stop dates.
    """
    import modules.helpers as hlp
    data["GBM_data"] = hlp.restrict_by_date(data["GBM_data"], new_start, new_stop)
    if data["BAT_data"] != None:
        data["BAT_data"] = hlp.restrict_by_date(data["BAT_data"], new_start, new_stop)

    return data

def new_limit(old_start, old_stop):
    while True:
        try:
            answer = float(input("Give the new date: ").strip())
            too_early = answer <= old_start
            too_late = answer >= old_stop
            if too_early or too_late:
                print("The new date should be between the old start date and the old end date.") 
            else:
                new_date = answer
                break
        except:
            print("The date should be a number!")

    return new_date

def redefine_range(data):
    import modules.messages as msg
    old_startdate = data["GBM_data"]["dates"][0] 
    old_stopdate = data["GBM_data"]["dates"][-1]
    new_startdate = old_startdate
    new_stopdate = old_stopdate
    print("Your current data start at MJD: ", old_startdate)
    print("and end at MJD:                 ", old_stopdate)
    print()
    while True:
        choice = msg.visualize_range_menu()
        if choice in ("q", "Q"):
            break
        elif choice == "1":
            new_startdate = new_limit(old_startdate, old_stopdate)
            data = restrict(data, new_startdate, new_stopdate)
            break

        elif choice == "2":
            new_stopdate = new_limit(old_startdate, old_stopdate)
            data = restrict(data, new_startdate, new_stopdate)
            break
        else:
            print("Please enter a valid option.")
            print()

    return data

def gaps(data):
    print("Coming soon!")
    print()
    return data

def init(my_data):
    import modules.messages as msg
    if my_data["GBM_data"] == None:
        print("Please provide GBM data first!")
        print()
        return(my_data)
    while True:
        gbmplot(my_data)
        choice = msg.visualize_menu()
        if choice in ("q", "Q"):
            break
        elif choice == "1":
            my_data = redefine_range(my_data)
        elif choice == "2":
            import modules.gaps as gaps
            my_data = gaps.init(my_data)

        else:
            print("Please enter a valid choice.")
            print()

    return my_data
