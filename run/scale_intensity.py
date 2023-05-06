"""
Scaling the intensity proxy based on the given intensity reference(s).
"""
def linear(x, a):
    return a * x

def linear2(x, a, b):
    return a * x + b * x**2

def first_degree_scale(post_data, intens_on_ref_dates, reference_fluxes):

    import numpy as np
    from scipy.optimize import curve_fit
    p0 = [np.mean(intens_on_ref_dates/reference_fluxes)]
    popt, pcov = curve_fit(linear, intens_on_ref_dates, reference_fluxes, p0 = p0)
    perr = np.sqrt(np.diag(pcov))
    post_data_copy = post_data.copy()
    intens_err = np.array(post_data["INTENS_ERR"])
    intens = np.array(post_data["INTENS"])
    post_data_copy["INTENS"] = linear(intens, *popt).tolist()
    post_data_copy["INTENS_ERR"] = np.sqrt((popt[0] * intens_err)**2 + (intens * perr[0])**2).tolist()
    
    return post_data_copy 

def second_degree_scale(post_data, intens_on_ref_dates, reference_fluxes):

    import numpy as np
    from scipy.optimize import curve_fit
    p0 = [np.mean(intens_on_ref_dates/reference_fluxes), 0]
    popt, pcov = curve_fit(linear2, intens_on_ref_dates, reference_fluxes, p0 = p0)
    perr = np.sqrt(np.diag(pcov))
    post_data_copy = post_data.copy()
    intens_err = np.array(post_data["INTENS_ERR"])
    intens = np.array(post_data["INTENS"])
    post_data_copy["INTENS"] = linear2(intens, *popt)
    post_data_copy["INTENS_ERR"] = np.sqrt(((popt[0] + 2 * popt[0] * intens) * intens_err)**2 + (intens**2 * perr[1])**2 )

    return post_data_copy

def scale(my_data, post_data):
    import modules.messages as msg
    import numpy as np
    reference_dates = np.array(my_data["Reference"]["dates"])
    reference_fluxes = np.array(my_data["Reference"]["flux"])
    intens_dates = np.array(post_data["INTENS_DATE"])
    intens = np.array(post_data["INTENS"])

    intens_on_ref_dates = np.interp(reference_dates, intens_dates, intens)

    if len(my_data["Reference"]["dates"]) > 1:
        while True:
            choice = msg.scale_intensity_menu()
            if choice == "1":
                print("Scaling intensity...")
                data = first_degree_scale(post_data, intens_on_ref_dates, reference_fluxes)
                break
            elif choice == "2":
                print("Scaling intensity...")
                data = second_degree_scale(post_data, intens_on_ref_dates, reference_fluxes)
                break
            else:
                print("Please input a valid choice.")
    else:
       print("Scaling intensity...")
       data = first_degree_scale(post_data, intens_on_ref_dates, reference_fluxes) 
    print("Success!")
    return data
