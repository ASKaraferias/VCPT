def post_data(data):
    default_dict = {
            "FREQ" : data["GBM_data"]["freq"],          
            "FREQ_ERR" : data["GBM_data"]["freq_err"],
            "DATES" : data["GBM_data"]["dates"],
            "INTENS" : data["GBM_data"]["amp"],
            "INTENS_ERR" : data["GBM_data"]["amp_err"],
            "INTENS_DATE" : data["GBM_data"]["dates"],
            "DISTANCE" : None,
            "GAPS" : None,
            "TORQUE_MODEL" : "GL79"
            }
    return default_dict
