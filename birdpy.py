#!/usr/bin/env python

# PROGRAM: birdpy.py
#-----------------------------------------------------------------------
# Version 0.1
# 18 January, 2020
# patternizer AT gmail DOT com
# https://patternizer.github.io
#-----------------------------------------------------------------------

import os, sys, time, math
import numpy as np
from numpy import *
import scipy
import scipy.linalg as linalg
from scipy.linalg import toeplitz, eigh 
import scipy.signal as sig
from scipy.stats import chi2
from scipy.optimize import fmin_powell
from scipy import interpolate
from scipy import pi
from scipy.fftpack import fft
from scipy import signal
from scipy.signal import lfilter
import statsmodels.api as sm
import seaborn as sns; sns.set(style="darkgrid")
import matplotlib.pyplot as plt; plt.close("all")
import moviepy

#-------------------------------------------------------------------------------


################################################################################
# MAIN
################################################################################

if __name__ == '__main__':

    '''
    birdpy main:
    ---------------
    # Written by Michael Taylor, version date 2020-01-18.
    # Please send comments to https://patternizer.github.io
    '''

    #
    # Load video clip: 
    #

    # x = loadtxt(filestr, delimiter=',')

print('** END')

