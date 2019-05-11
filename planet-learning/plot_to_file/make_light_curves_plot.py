from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import logging
import os

from os.path import isdir, join

from ..catascript.base import Base, Session
from ..catascript.models import Catalog

def create_dir(directory):
    # Create the directory to store the plots on first run
    if not isdir(directory):
         os.mkdir(directory)

def get_TICS_with_confirmed():
    """
    This functions queries the database and returns the TIC IDs that have a confirmed planet.

    Returns
    -------
        - dict_TIC_IDs : dict
            The dictionnary containing the (TIC ID, path to light curve) pairs.
    """
    #Query
    session = Session()

    query = session.query(Catalog).filter(Catalog.already_confirmed == True).all()

    session.close()

    #Creating the dict of data
    dict_TIC_IDs = {}

    for entry in query:
        dict_TIC_IDs[entry.ID] = entry.path
    
    #Returning
    return dict_TIC_IDs


def make_and_save_light_curve(TIC, lc_path, processed_dir_path):
    """
    This function plots the light curve using matplotlib and saves the output to a svg file

    Parameters
    ----------
        - TIC : int
            The value of the TIC ID corresponding to the light curve we want to plot
        - lc_path : string
            The path to the ligth curve storage on the nfs
        - processed_dir_path : str
            Path to the folder of processed data in the nfs
    """
    # Getting the file
    logging.info("TIC {} : Tackling {} file".format(TIC, lc_path))
    
    # Opening the data
    with fits.open(lc_path, mode="readonly") as hdulist:
        tess_bjds = hdulist[1].data['TIME']
        sap_fluxes = hdulist[1].data['SAP_FLUX']
        pdcsap_fluxes = hdulist[1].data['PDCSAP_FLUX']
    
    # Plotting
    fig, ax = plt.subplots()
    ax.plot(tess_bjds, pdcsap_fluxes, 'ko') 

    #Saving the file to svg
    plt.savefig('{}/plots_to_file/{}_light_curve.svg'.format(processed_dir_path,TIC))
    plt.close(fig)

def make_light_curves_plot(processed_dir_path):
    """
    This function builds the plot of all light curves and save them to jpg, in a nfs subfolder

    Parameters:
    -----------
        - processed_dir_path : str
            Path to the folder of processed data in the nfs
    """
    #Get plotting boolean
    need_to_plot = int(os.getenv("PLOT_TO_FILE"))

    #Create directory
    create_dir('plots_to_file')

    if need_to_plot:
        logging.info("Processing : plotting to file light curves of TICS with confirmed planets")

        #Create a dir if not existent
        dict_TIC_IDs = get_TICS_with_confirmed()

        #Plot to file all light curves
        for (TIC, lc_path) in dict_TIC_IDs.items():
            make_and_save_light_curve(TIC, lc_path)

        #Display message
        logging.info("Done")
    
    else:
        logging.info("Not plotting to file light curves of TICS with confirmed planets")

