# -*- coding: utf-8 -*-
"""
Created on Thu Oct 06 08:39:25 2016

@author: shilei

Loader and checker for M3D-C1 RMP output files
"""

import numpy as np
from scipy.io.netcdf import netcdf_file


class RmpLoader(object):
    """Loader for M3D-C1 RMP output files
    
    Initialization
    ****************
    
    __init__()
    Initialize with a filename
    
    Attributes
    ***********
    
    Example
    *******
    """
    
    def __init__(self, filename, mode=r'full'):
        """Initialize the loader
        
        filename should contain the full path to the netcdf file generated by
        M3DC1.
        
        :param string filename: full or relative path to the netcdf file 
                                generated by M3DC1
        :param string mode: loading mode. mode='full' will automatically read
                            all the desired data in the file, and is the 
                            default mode. mode='eq_only' reads only the 
                            equilibrium, no RMP variables. mode='least' only 
                            initialize the object, nothing will be read. 
        """  
        self.filename = filename
        if mode == 'least':            
            return
        else:
            self.load_equilibrium(self.filename)
            if mode == 'full':
                self.load_rmp(self.filename)
    
    def load_equilibrium(self, filename):
        """load the equilibrium data from M3DC1 output netcdf file
        
        :param string filename: full or relative path to the netcdf file 
                                generated by M3DC1
        """
        m3d_raw = netcdf_file(filename, 'r')
        
        # npsi is the number of grid points in psi
        # mpol is the number of grid points in theta
        self.npsi = m3d_raw.dimensions['npsi']
        self.mpol = m3d_raw.dimensions['mpol']
        
        # 1D quantities are function of psi only
        # we have
        
        # poloidal flux, in weber/radian
        self.psi_p = np.copy(m3d_raw.variables['flux_pol'].data)
        # normalized psi, normalized to psi_wall
        self.psi_n = np.copy(m3d_raw.variables['psi'].data)
        # toroidal current enclosed in a flux surface
        self.I = np.copy(m3d_raw.variables['current'].data)
        # R B_phi is also a flux function
        self.F = np.copy(m3d_raw.variables['F'].data)
        # equilibrium electron density
        self.ne = np.copy(m3d_raw.variables['ne'].data)
        # safety factor
        self.q = np.copy(m3d_raw.variables['q'].data)
        # total pressure
        self.p = np.copy(m3d_raw.variables['p'].data)
        # electron pressure
        self.pe = np.copy(m3d_raw.variables['pe'].data)
        
        # 2D quantities will depend on theta
        
        # R in (R, PHI, Z) coordinates
        self.R = np.copy(m3d_raw.variables['rpath'].data)
        # Z in (R, PHI, Z)
        self.Z = np.copy(m3d_raw.variables['zpath'].data)
        # poloidal magnetic field
        self.B_p = np.copy(m3d_raw.variables['Bp'].data)
        
    def load_rmp(self, filename):
        """load the resonant magnetic perturbations
        :param string filename: full or relative path to the netcdf file 
                                generated by M3DC1
        """
        #todo coordinates convention needs to be sorted out
        
        m3d_raw = netcdf_file(filename, 'r')
        
        # In our convention, alpha is a complex number, and the resonant form
        # has cos and sin part on real and imaginary parts respectively
        self.alpha_m = np.copy(m3d_raw.variables['alpha_real'].data) + \
                     1j*np.copy(m3d_raw.variables['alpha_imag'].data)
        
        # Then, the real space alpha can be obtained by FFT. Check Nate's note
        # on the normalization convention, as well as scipy's FFT 
        # documentation.
        self.alpha = np.fft.fft(self.alpha_m)
                     
        
        

            
            
        
