from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import logging
import os

from os.path import isdir, join

from ..catascript.base import Base, Session
from ..catascript.models import Catalog, Confirmed

#Setting properties for matplotlib (width, heigth in inches)
plt.rcParams["figure.figsize"] = (20,3)

def create_dir(directory):
    # Create the directory to store the plots on first run
    if not isdir(directory):
         os.mkdir(directory)

def get_TICS_with_confirmed_and_info():
    """
    This function queries the database and returns the TIC IDs that have a confirmed planet.

    Returns
    -------
    dict_TIC_IDs : dict
        The dictionnary containing the (TIC ID, (path to the ligth curve storage on the nfs, name of star, discovery method)) pairs.
    """
    #Catalog Query
    session = Session()

    TIC_query = session.query(Catalog).filter(Catalog.already_confirmed == True).all()

    #Creating the dict of data
    dict_TIC_IDs = {}

    for catalog_entry in TIC_query:
        #Querying more info
        info_query = session.query(Confirmed).filter(Confirmed.catalog_id == catalog_entry.ID).limit(1)
        confirmed_entry = info_query[0]

        dict_TIC_IDs[catalog_entry.ID] = (catalog_entry.path, confirmed_entry.Host_name, confirmed_entry.Discovery_Method)

    session.close()

    #Returning
    return(dict_TIC_IDs)


def make_and_save_light_curve(TIC, info, processed_dir_path):
    """
    This function plots the light curve using matplotlib and saves the output to a svg file

    Parameters
    ----------
    TIC : int
        The value of the TIC ID corresponding to the light curve we want to plot
    info : tuple
        (path to the ligth curve storage on the nfs, name of star, discovery method)
    processed_dir_path : str
        Path to the folder of processed data in the nfs
    """
    # Unpacking info
    (lc_path, name, method) = info

    # Getting the file
    logging.info("TIC {} : Tackling {} file".format(TIC, lc_path))
    
    # Opening the data
    with fits.open(lc_path, mode="readonly") as hdulist:
        tess_bjds = hdulist[1].data['TIME']
        pdcsap_fluxes = hdulist[1].data['PDCSAP_FLUX']
    
    # Plotting
    fig, ax = plt.subplots()
    ax.plot(tess_bjds, pdcsap_fluxes, 'k.') 

    #Adding a title
    fig.suptitle("{name}, discovered by {method}".format(name=name, method=method))

    #Saving the file to svg
    plt.savefig('{}/plots_to_file/{}_lc.svg'.format(processed_dir_path,TIC))
    plt.close(fig)

def make_light_curves_plot(processed_dir_path):
    """
    This function builds the plot of all light curves and save them to svg, in a nfs subfolder

    Parameters:
    -----------
    processed_dir_path : str
        Path to the folder of processed data in the nfs
    """
    #Get plotting boolean
    need_to_plot = int(os.getenv("PLOT_TO_FILE"))

    #Create directory
    create_dir('{}/plots_to_file'.format(processed_dir_path))

    if need_to_plot:
        logging.info("Processing : plotting to file light curves of TICS with confirmed planets")

        #Create a dir if not existent
        dict_TIC_IDs = get_TICS_with_confirmed_and_info()

        #Plot to file all light curves
        for (TIC, info) in dict_TIC_IDs.items():
            make_and_save_light_curve(TIC, info, processed_dir_path)

        #Display message
        logging.info("Done")
    
    else:
        logging.info("Not plotting to file light curves of TICS with confirmed planets")

