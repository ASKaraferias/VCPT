from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
#
#Release 220509: Corrected T_pi/2 epoch in binary_beta
#
class pulsar:
# initialize class
    def __init__(self, filename):
        hdulist = fits.open(filename)
        orb_elem = hdulist[1].data
        self.name = orb_elem.field("NAME")[0]
        self.ra = orb_elem.field("RA")[0]
        self.dec = orb_elem.field("DEC")[0]
        self.binary = orb_elem.field("BINARY") 
        self.pbinary = orb_elem.field("PBINARY")[0] 
        self.pbdot = orb_elem.field("PBDOT")[0]
        self.epoch_type = orb_elem.field("EPOCH_TYPE")[0]
        self.binaryepoch = orb_elem.field("BINARYEPOCH")[0]
        self.axsini = orb_elem.field("AXSINI")[0]
        self.periapse = orb_elem.field("PERIAPSE")[0]
        self.apsidalrate = orb_elem.field("APSIDALRATE")[0]
        self.eccentricity = orb_elem.field("ECCENTRICITY")[0]
        self.egress = orb_elem.field("EGRESS")[0]
        self.ingress = orb_elem.field("INGRESS")[0]
        hist = hdulist[2].data
        self.tstart = hist.field("TSTART")[hist.field("DETECTED") == 1]
        self.tstop = hist.field("TSTOP")[hist.field("DETECTED") == 1]
        self.psrtime = hist.field("PSRTIME")[hist.field("DETECTED") == 1] 
        self.barytime = hist.field("BARYTIME")[hist.field("DETECTED") == 1]
        self.fpeak = hist.field("FREQUENCY")[hist.field("DETECTED") == 1]
        self.fsig = hist.field("FREQUENCY_ERR")[hist.field("DETECTED") == 1]
        self.amplitude = hist.field("AMPLITUDE")[hist.field("DETECTED") == 1]
        self.ampsig = hist.field("AMPSIG")[hist.field("DETECTED") == 1]
        self.nharm = len(hist.field("SEARCH_HRM")[0])
  #      self.yn = hist.field("YN")[hist.field("DETECTED") == 1]
        self.hrmcoef = hist.field("HRMCOEF")[hist.field("DETECTED") == 1]
        self.hrmcoefsig = hist.field("HRMCOEFSIG")[hist.field("DETECTED") == 1]
#        self.hrmchisqnu = hist.field("HRMCHISQNU")[hist.field("DETECTED") == 1]
        hdulist.close()
        # tmin and tmax set the plotting bounds in MJD
        self.tmin = np.ndarray.min(self.psrtime) - 20.
        self.tmax = np.ndarray.max(self.psrtime) + 20.
        self.fmin = (np.ndarray.min(self.fpeak) - np.ndarray.max(self.fsig)) * 1000.0
        self.fmax = (np.ndarray.max(self.fpeak) + np.ndarray.max(self.fsig)) * 1000.0
        self.amin = np.ndarray.min(self.amplitude) - np.ndarray.max(self.ampsig)
        self.amax = np.ndarray.max(self.amplitude) + np.ndarray.max(self.ampsig)
        #
        self.shift_zero = 'no'
        self.plot_prof = 'no'
        self.phase_sig = 0.0
        self.phase = 0.0
        self.lc_sig = 0.0
        self.lc_sig_error = 0.0
        self.lc = 0.0
    def circular_el(self,g,h):
        
        theta = np.degrees(np.arctan2(g,h))
        self.periapse = theta
        eccen = g/np.sin(np.radians(theta))
        self.eccentricity = eccen
        print(eccen)()
        print(theta)
    def printinfo(self):
        if self.binary == 'Y' :
            print('Source name {} ra={} dec={}'.format(self.name, self.ra, self.dec))
            print('The following ephemeris is used to determine pulsar emission frequencies')
            print('Binary orbital period is {} days'.format(self.pbinary))
            if np.abs(self.pbdot) > 0:
                print('Binary orbital period derivative is {} days/day'.format(self.pbdot))
            if self.epoch_type =='T':
                print('Pi/2 Epoch is {} JED'.format(self.binaryepoch))
            else:
                print('Periastron Epoch is {} JED'.format(self.binaryepoch))
            print('AXSIN(i) is {} light-sec'.format(self.axsini) )
            print('Long. of periastron is {} deg'.format(self.periapse))
            print('Eccentricity is {}'.format(self.eccentricity))
            if self.egress > 0:
                print('Source is eclipsing:')
                print('Egress is {}'.format(self.egress))
                print('Ingress is {}'.format(self.ingress))
        else:
            print('Source name {} ra={} dec={}'.format(self.name, self.ra, self.dec))
            print('No ephemeris is used and frequencies are not corrected for the pulsar orbit')
    def setminmax(self,fmin=None,fmax=None,amin=None,amax=None):
        # This method sets the plot ranges for frequency(fmin, fmax) and pulsed amplitude(amin, amax)
        # Use user defined vertical plot ranges
        if fmin is None:
            self.fmin = (np.ndarray.min(self.fpeak[(self.barytime >= self.tmin) * (self.barytime < self.tmax)])- \
                np.ndarray.max(self.fsig[(self.barytime >= self.tmin) * (self.barytime < self.tmax)])) * 1000.0
        else:
            self.fmin = fmin
        if fmax is None:
            self.fmax = (np.ndarray.max(self.fpeak[(self.barytime >= self.tmin) * (self.barytime < self.tmax)])+\
                np.ndarray.max(self.fsig[(self.barytime >= self.tmin) * (self.barytime < self.tmax)])) * 1000.0
        else:
            self.fmax = fmax
        if amin is None:
            self.amin = np.ndarray.min(self.amplitude[(self.barytime >= self.tmin) * (self.barytime < self.tmax)])- \
                np.ndarray.max(self.ampsig[(self.barytime >= self.tmin) * (self.barytime < self.tmax)])
        else:
            self.amin = amin
        if amax is None:
            self.amax = np.ndarray.max(self.amplitude[(self.barytime >= self.tmin) * (self.barytime < self.tmax)])+\
                np.ndarray.max(self.ampsig[(self.barytime >= self.tmin) * (self.barytime < self.tmax)])
        else:
            self.amax = amax
    def plot(self,tmin=None,tmax=None,fmin=None,fmax=None,amin=None,amax=None):
        # This method plots the frequency history and pulsed flux between tmin and tmax
        # Use user supplied tmin tmax [MJD]
        # verticle limits can be preset with fmin, fmax and amin, amax either explicityly for the method call or by setting the values directly
        if tmin is not None:
            self.tmin = tmin
        if tmax is not None:
            self.tmax = tmax
        self.setminmax(fmin = fmin, fmax = fmax, amin = amin, amax = amax)
        plt.figure(1)
        plt.subplot(211)        
        plt.ylabel('fpeak [mHz]')
        plt.axis([self.tmin,self.tmax,self.fmin,self.fmax])
        plt.errorbar(self.barytime, self.fpeak*1000.,self.fsig*1000.,fmt='.')
        plt.subplot(212)
        plt.axis([self.tmin,self.tmax,self.amin,self.amax])
        plt.xlabel('Time [MJD]')
        plt.ylabel('12-25 keV Pulsed Flux')
        plt.errorbar(self.barytime, self.amplitude,self.ampsig,fmt='.')
        plt.show()
    def binary_beta(self,time=None):
        #For a binary source compute the velocity/c away from the observer for an
        #       array of times time.
        # time is in MJD 
        # The times must be barycentered.
        if self.epoch_type =='T':
            tpi2 = self.binaryepoch
            #print('T=',tpi2)
        else:
            tpi2 = self.binaryepoch+(90.0-self.periapse)/360.0 * self.pbinary
            #print('P=',tpi2)
        if time is None:
            time = self.barytime
        raddeg = np.pi/180.0
        secinday = 86400.00
        omega = self.periapse*raddeg
        radical = np.sqrt(1.0-self.eccentricity**2)
        e1 = self.eccentricity*np.cos(omega)
        e2 = self.eccentricity*np.sin(omega)
        n = 2.0 *np.pi/self.pbinary/secinday
        # calculate mean anomoly
        #M = (self.barytime+2400000.5 - self.binaryepoch)/self.pbinary
        M = (time+2400000.5 -tpi2)/self.pbinary
        M = np.mod((M+0.25-self.periapse/360.0) ,1.0)
        M = 2.0*np.pi*(M+(M<0.0))
        # calculate the eccentric anomoly
        E = np.array([np.pi+(M-np.pi)/(1+self.eccentricity)])
        delta = np.array([2.0])
        while (np.ndarray.max(np.absolute(delta)) > 1.0e-12):
            delta = (M-E+self.eccentricity*np.sin(E))/(1-self.eccentricity*np.cos(E))
            E = E+delta
        U = E-np.pi/2.0 + omega
        cU = np.cos(U)
        sU = np.sin(U)
        temp = n*self.axsini*(-sU-e1*(-e1*sU+e2*cU)/(1.0 + radical))/(1+e1*sU-e2*cU)
        self.vel = temp[0,:]
    def profile(self,time,channel,center=None):
        # This method calculates the light curve for a pulse profile for a given channel at a given time (MJD) with an optional parameter to shift
        # the minimum to phase zero
        # the nearest interval >= time will be used
        # this method must be called before plot_profile()
        if center is None:
            center = self.shift_zero
        npoints = 10*(2*self.nharm+1) #number of points in plotted profile
        npe = (2.0*self.nharm+1) # number of error points
        phi2 = (0.5+np.arange(2.0*npe))/npe
        phi = np.arange(2.0*npoints)/npoints
        r2 = np.zeros(2.0*npe)
        re = np.zeros(2.0*npe)
        r = np.zeros(2.0*npoints)
        exact_time = np.amin(self.barytime[self.barytime >= time])
        lc = self.hrmcoef[self.barytime == exact_time,channel,:]
        lce = self.hrmcoefsig[self.barytime == exact_time,channel,:]
        for harm in (np.arange(self.nharm)+1):
         #   print(2*harm-2)
            r = r+lc[0,2*harm-2]*np.cos(2*np.pi*phi*harm)+lc[0,2*harm-1]*np.sin(2*np.pi*(phi*harm))
            r2 = r2+lc[0,2*harm-2]*np.cos(2*np.pi*phi2*harm)+lc[0,2*harm-1]*np.sin(2*np.pi*phi2*harm)
            re = re+np.power(lce[0,harm-2],2)
        re = np.sqrt(re)
        if center =='yes' :
            w = r2[r2 == np.amin(r2)]
            print(np.arange(len(r2))[w[0] == r2])
            shift_r = -10*np.arange(len(r2))[w[0] == r2]
            r2 = np.roll(r2,-np.arange(len(r2))[w[0] == r2])
            re = np.roll(re,-np.arange(len(re))[w[0] == r2])            
            r = np.roll(r,shift_r)
        self.phase_sig = phi2
        self.phase = phi
        self.lc_sig = r2
        self.lc_sig_error = re
        self.lc = r
        return exact_time
    def plot_profile(self,plot_prof=None):
        # This method will actually plot the profile
        if plot_prof == None:
            plot_prof = self.plot_prof
        if plot_prof == 'yes':
            plt.errorbar(self.phase_sig,self.lc_sig,self.lc_sig_error,fmt='.')
            plt.plot(self.phase,self.lc)
        phi2 = self.phase_sig
        phi = self.phase
        r2 = self.lc_sig
        re = self.lc_sig_error
        r = self.lc
        plt.show()
    
