"""
Here we set the distance to the source.
Default value: Unknown distance.
"""
def init(my_data):
    while True:
        print()
        dist = input("Give the distance to the source in kpc (set it to 0 for unknown distance): ").strip()
        try:
            dist_asfloat = float(dist)
            if dist_asfloat == 0:
                print("The distance will be a free parameter.")
            else:
                print("The distance is now set to ", dist, "kpc.")
            print()
            break
        except:
            print("Prease provide a valid distance!")
            print()
    if dist_asfloat == 0:
        my_data["Distance"] = "Unknown"
    else:
        my_data["Distance"] = dist_asfloat

    return my_data
