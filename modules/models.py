#Here we define some constants we will use throughout the code
I = 1.3 * pow(10.,45) #g * cm^2    NS Moment of Inertia
G = 6.674 * pow(10., -8) #dyne * cm^2 /g^2  Gravitational Constant
M = 1.4 * 1.988435 * pow(10., 33) #g NS Mass
parsec = 3.086e21 #cm
R = 1.2e6 #cm NS Radius
c = 3e10 #cm/s   Speed of Light  
eff = G*M/(R*c**2) #accretion column radiative efficiency

# Magnetospheric radius/pow(M_dot, -2/7) =>  r_magnetospheric = r_m_factor(mu, xi) * pow(M_dot, -2/7)
def r_m_factor(mu, xi0):
    return xi0 * np.power(np.power(mu, 4)/(2 * G * M), 1/7)


# Corrotation RaOdius
def r_co(omega):
    return np.power(G * M/(omega**2), 1/3) #x is omega


# Torque Models
def GL79(y, r_m, omega):
    r_co = (G*M/omega**2)**(1/3)
    omega_fast = (r_m/r_co)**(3/2)
    n = 1.39 * (1 - omega_fast * (4.03 * np.abs(1-omega_fast)**0.173 - 0.878))/(1-omega_fast)
    Nacc = y * (G*M*r_m)**(1/2)
    N_tot = Nacc * n
    return (1/(2 * math.pi * I)) * N_tot

def W95(y, r_m, omega):
    r_co = (G*M/omega**2)**(1/3)
    omega_fast = (r_m/r_co)**(3/2)
    n = (7/6 - (4/3) * omega_fast + (1/9) * omega_fast**2)/(1-omega_fast)
    Nacc = y * (G*M*r_m)**(1/2)
    N_tot = Nacc * n
    return (1/(2 * math.pi * I)) * N_tot


def H14(y, r_m, omega):
    N_tot = y * r_m**2 * (((G*M)**(1/2)) * (r_m**(-3/2))) * (1 - omega / (((G*M)**(1/2)) * (r_m**(-3/2))))
    return (1/(2 * math.pi * I)) * (N_tot)


def B20(y, r_m, omega): #O. Benli Feb 2020
    r_A = xi * r_m
    omega_fast = (r_m/r_co(omega))**(3/2)
    N_SU = y * ((G * M * r_m)**(1/2))
    N_SD = (1/2) * y * ((G * M * r_A)**(1/2)) * (1 - omega_fast**2)
    N_tot = N_SU + N_SD
    return (1/(2 * math.pi * I)) * N_tot

# Radial Velocity
def RADVEL(DATE0, e, Period, Periapse, axsini, epoch, time):
    #For a binary source compute the velocity/c away from the observer for an
    #       array of times time.
    # time is in MJD 
    # The times must be barycentered.  
    if time is None:
        time = DATE0
    raddeg = np.pi/180.0
    secinday = 86400.00
    omega = Periapse * raddeg
    radical = np.sqrt(1.0-e**2)
    e1 = e*np.cos(omega)
    e2 = e*np.sin(omega)
    n = 2.0 *np.pi/Period/secinday
    #epoch_ref = epoch - 2400000.5
    # calculate mean anomoly
    #M = (time+2400000.5 - self.binaryepoch)/self.pbinary
    M = (time + 2400000.5 - epoch) /Period
    M = np.mod((M+0.25-Periapse/360.0) ,1.0)
    M = 2.0*np.pi*(M+(M<0.0))
    # calculate the eccentric anomoly
    E = np.array([np.pi+(M-np.pi)/(1+e)])
    delta = np.array([2.0])
    while (np.ndarray.max(np.absolute(delta)) > 1.0e-12):
        delta = (M-E+e*np.sin(E))/(1-e*np.cos(E))
        E = E+delta
    U = E-np.pi/2.0 + omega
    cU = np.cos(U)
    sU = np.sin(U)
    temp = n*axsini*(-sU-e1*(-e1*sU+e2*cU)/(1.0 + radical))/(1+e1*sU-e2*cU)
    return temp[0,:]
