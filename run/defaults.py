def post_data(data):
    import os
    default_dict = {
            "FREQ" : data["GBM_data"]["freq"],          
            "FREQ_ERR" : data["GBM_data"]["freq_err"],
            "DATE" : data["GBM_data"]["dates"],
            "INTENS" : data["GBM_data"]["amp"],
            "INTENS_ERR" : data["GBM_data"]["amp_err"],
            "INTENS_DATE" : data["GBM_data"]["dates"],
            "DISTANCE" : None,
            "GAP_SPOTS" : None,
            "GAP_DATES" : None,
            "TORQUE_MODEL" : "GL79",
            "OUTPUT_DIR" : None,
            "TMPFILE" : os.path.relpath(__package__)
            }
    print(default_dict["TMPFILE"])
    return default_dict
