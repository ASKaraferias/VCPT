def gbmplot(data):
    import matplotlib.pyplot as plt
    plt.plot(data["GBM_data"]["dates"], data["GBM_data"]["freq"], "k.", markersize = 2)
    plt.xlabel("DATE [MJD]")
    plt.ylabel("FREQ [Hz]")
    plt.title("GBM Frequency timeseries.")
    plt.show()

def redefine_range(data):
    return data

def gaps(data):
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
            my_data = gaps(my_data)
        else:
            print("Please enter a valid choice.")
            print()

    return my_data
