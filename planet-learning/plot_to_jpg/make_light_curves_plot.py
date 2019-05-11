from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

from .catascript.base import Base, Session
from .catascript.models import Catalog

def get_TICS_with_confirmed():
    """
    This functions queries the database and returns the TIC IDs that have a confirmed planet.

    Returns
    -------
        - dict_TIC_IDs : dict
            The dictionnary containing the (TIC ID, path to light curve) pairs.
    """
    pass

def make_and_save_light_curve(TIC):
    """
    This function plots the light curve using matplotlib and saves the output to a jpg file

    Parameters
    ----------
        - TIC : int
            The value of the TIC ID corresponding to the light curve we want to plot
    """
    pass

def make_light_curves_plot():
    """
    This function builds the plot of all light curves and save them to jpg
    """
    pass
    #Create a dir if not existent
    #Get the TICS
    #for TIC in TICS
        #make and save light curve
    #Display data
