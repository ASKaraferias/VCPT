def init(data):
    import numpy as np
    import modules.models as models
    I = models.I
    G = models.G
    M = models.M
    parsec = models.parsec
    R = models.R
    c = models.c
    eff = models.eff
    DATE = np.array(data["DATE"])
    FREQ = np.array(data["FREQ"])
    FREQ_ERR = np.array(data["FREQ_ERR"])
    INTENS = np.array(data["INTENS"])
    INTENS_ERR = np.array(data["INTENS_ERR"])
    INTENS_DATE = np.array(data["INTENS_DATE"])
    DISTANCE = data["DISTANCE"]
    GAP_SPOTS = np.array(data["GAP_SPOTS"])
    GAP_DATES = np.array(data["GAP_DATES"])
    TORQUE_MODEL = np.array(data["TORQUE_MODEL"])
    OUTPUT_DIR = np.array(data["OUTPUT_DIR"])
    TMPFILE = np.array(data["TIMPFILE"])

    MM = 1000
    DINT = np.linspace(DATE[0], DATE[-1], MM)
    LX_FACTOR = np.interp(DINT, INTENS_DATE, INTENS * 4 * np.pi() * parsec**2)
    
    GAP_SPOTS_INT = np.zeros(len(GAP_SPOTS))
    while k < len(DINT):
        if j < len(GAP_DATES):
            if (DINT[k] > GAP_DATES[j]) and (DINT[k-1] < GAP_DATES[j]):
                GAP_SPOTS_INT[j] = k
                j += 1
        k += 1
    GAP_SPOTS_INT = GAP_SPOTS_INT.astype(int)
