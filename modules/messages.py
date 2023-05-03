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
    print("Choose an option (enter the correct \
number and press RETURN):")
    print()
    print("[1] Import GBM '.fits' data.")
    print("[2] Import BAT '.fits' data.")
    print("[3] Visualize your data.")
    print("[4] Select an luminosity proxy. (Optional, Default: GBM Amplitude)")
    print("[5] Set the distance to the source. (Optional)")
    print("[6] Provide reference Flux(es).")
    print("[0] Exit")
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
