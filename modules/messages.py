def banner():
    """
    Print a welcome message:
    """
    import time
    
    text = "\
     █████   █████   █████████  ███████████  ███████████\n\
    ░░███   ░░███   ███░░░░░███░░███░░░░░███░█░░░███░░░█\n\
     ░███    ░███  ███     ░░░  ░███    ░███░   ░███  ░ \n\
     ░███    ░███ ░███          ░██████████     ░███    \n\
     ░░███   ███  ░███          ░███░░░░░░      ░███    \n\
      ░░░█████░   ░░███     ███ ░███            ░███    \n\
        ░░███      ░░█████████  █████           █████   \n\
         ░░░        ░░░░░░░░░  ░░░░░           ░░░░░    \
            "
    
    bannertab = text.split("\n")
    
    print()
    i = 0
    while i < len(bannertab):
        print(bannertab[i])
        print(bannertab[i+1])
        time.sleep(0.2)
        i += 2
    
    print()
    print("Welcome to the Very Cool Pulsar Tool!")
    print()


def mainmenu():
    print()
    print("Enter an option and press RETURN:")
    print()
    print("[1] Import GBM '.fits' data. (Start here)")
    print("[2] Import BAT '.fits' data. (Optional)")
    print("[3] Visualize your data.")
    print("[4] Select a luminosity proxy. (Optional. Defaults to GBM Amplitude.)")
    print("[5] Set the distance to the source. (Optional. Defaults to Unknkown distance.)")
    print("[6] Provide reference Flux(es).")
    print("[7] Run!")
    print()
    print("[I] Import a saved json file.")
    print("[E] Export your current data to json file.")
    print()
    print("[q] Exit")
    print()
    choice = input("Your choice: ").strip()
    return choice

def menu_err():
    print()
    print("OOPS! An error occured!")
    print("Please enter a valid choice!")
    print()
    return True

def lumi_menu():
    print("Select a proxy for the luminosity.")
    print("Available values:")
    print()
    print("[1] GBM amplitude")
    print("[2] BAT count rates")
    print()
    choice = input("Your choice: ").strip()
    return choice

def visualize_menu():
    print("Options:")
    print()
    print("[1] Change date range.")
    print("[2] Check account for gaps.")
    print()
    print("[q] Exit submenu.")
    print()
    choice = input("Your choice: ").strip()
    return choice
