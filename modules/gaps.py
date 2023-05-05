def All_gaps(data):
    """
    Calculate all the gaps
    """
    dates = data["GBM_data"]["dates"]
    all_gaps = []

    i = 1
    while i < len(dates):
        all_gaps.append(dates[i] - dates[i-1])
        i += 1

    largest_gap = max(all_gaps)
    return all_gaps

def gap_plot(data):
    import matplotlib.pyplot as plt
    dates = data["GBM_data"]["dates"]
    freq = data["GBM_data"]["freq"]
    gaps = data["Gaps"]["dates"]
    plt.figure()
    plt.plot(dates, freq, 'r.', markersize = 2, label = "GBM data")
    plt.vlines(gaps, min(freq), max(freq), label = "gaps taken to account")
    plt.legend()
    plt.show(block = False)

def Gap_assassin(data, min_gap):
    """
    Remove single data points between two large gaps and
    tag gap indices.
    """
    print()
    print("Locating the relevant gaps...")
    import numpy as np
    import modules.helpers as hlp
    all_gaps = np.array(All_gaps(data))
    gap_spots = np.where(all_gaps >= min_gap)[0]
    remove_spots = []
    i = 1
    remove_gaps = []
    while i < len(gap_spots):
        if gap_spots[i] == 1 + gap_spots[i-1]:
            remove_spots.append(gap_spots[i])
            remove_gaps.append(i)
            k = i + 1
            while k < len(gap_spots):
                gap_spots[k] -= 1
                k += 1
        i += 1
    print("Removing single points between gaps...")
    gap_spots = np.delete(gap_spots, remove_gaps)
    gap_spots += 1
    print("Writing the results...")
    data["GBM_data"], data_removed = hlp.data_point_remover(data["GBM_data"], remove_spots)
    if not data_removed: data_removed = None
    if data["Gaps"] == None:
        data["Gaps"] = {
                "min_gap" : min_gap,
                "dates" : np.array(data["GBM_data"]["dates"])[gap_spots].tolist(),
                "spots" : gap_spots.tolist(),
                "removed_points" : data_removed,
                }
    else:
        data["min_gap"] = min_gap,
        data["Gaps"]["dates"] = np.array(data["GBM_data"]["dates"])[gap_spots].tolist()
        data["Gaps"]["spots"] = gap_spots.tolist()
        for key in data["Gaps"]["removed_points"].keys():
            data["Gaps"]["removed_points"][key] += data_removed[key]
    print("Done!")
    print()
    gap_plot(data)
    return data

def Forget_gaps(data):
    import modules.helpers as hlp
    if data["Gaps"] == None:
        print("There is nothing to do.")
        print()
        return data
    if not data["Gaps"]["removed_points"]:
        data["Gaps"] = None
        return data
    
    data["GBM_data"] = hlp.add_data(data["GBM_data"], data["Gaps"]["removed_points"])
    data["Gaps"] = None
    return data

def init(data):
    all_gaps = All_gaps(data)
    large_gap_threshold = 7
    if max(all_gaps) < large_gap_threshold:
        print()
        print("There are no large gaps in your data set.")
        print()
    else:
        print()
        print("There are some large gaps in your data set.")
        print("The largest gap is ", max(all_gaps), " days long.")
        print()
        while True:
            while True:
                try:
                    min_gap = float(input(f"How large (in days) should a gap be to take it into \
account (should be >= {large_gap_threshold}, or 0 to restore to defaults)? ").strip())
                    break
                except:
                    print()
                    print("Please give a number!")
                    print()
            if min_gap > max(all_gaps):
                print("Good, no gaps in your dataset are that large.")
                break
            elif min_gap < large_gap_threshold and min_gap != 0:
                print(f"The gaps should be larger than {large_gap_threshold} to take into account")
                print()
            elif min_gap == 0:
                data = Forget_gaps(data)
                break
            else:
                data = Gap_assassin(data, min_gap)
                break
                print() 

    return data
