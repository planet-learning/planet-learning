"""Module to extract metadata from TESS `.fits` light curves files headers

This module reads the headers of light curves files from TESS and exports them into a dictionary, saved in a `.pickle` file.
The extracted fields are the following :
    - TICID
    - TICVER
    - SECTOR
The path to the `.fits` file is also provided in each entry.
Find more information about the TESS `.fits` files here : https://archive.stsci.edu/files/live/sites/mast/files/home/missions-and-data/active-missions/tess/_documents/EXP-TESS-ARC-ICD-TM-0014.pdf

"""
import logging
import os
import pickle
import sys
from os.path import isdir, isfile, join

import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits


def load_pickle(path):
    """Load data from a `.pickle` file.

    The `.pickle` file is read in binary format.

    Parameters
    ----------
    path: path-like object
        path to the file to read

    Raises
    ------
    EnvironmentError
        if the requested file does not exist

    Returns
    -------
    type of object saved in the `.pickle`
        Python object stored in the `.pickle`
    
    """
    if isfile(path):
        logging.info("Loading existing extracted file : {}".format(path))
        with open(path, 'rb') as p:
            data = pickle.load(p)
    else:
        logging.info("No existing extracted file found")
        raise EnvironmentError

    return data


def save_to_pickle(data, path):
    """Save a python object into a `.pickle` file.
    
    Data is saved in binary format.

    Parameters
    ----------
    data: any python object
        object to save
    path: path-like object
        path to the file to write

    """
    # Write the data into a pickle file
    logging.info("Saving data")
    with open(path, 'wb') as p:
        pickle.dump(data, p)
    logging.info("Data saved in {}".format(path))


def get_light_curve_metadata(light_curve_path):
    """Retrieve metadata from a light curve `.fits` file.

    A description the content of the light curves files can be found here :
        https://archive.stsci.edu/files/live/sites/mast/files/home/missions-and-data/active-missions/tess/_documents/EXP-TESS-ARC-ICD-TM-0014.pdf
    The collected fields are the following :
        - TICID
        - TICVER
        - SECTOR
    The extracted data is returned as an int representing the TICID and a dict with the following structure :
        {'SECTOR': int, 'TICVER': int}
    In the case where the file could not be read an bare error is raised.
    The error message is outputed in the log file.

    Parameters
    ----------
    light_curve_path: path-like object
        path to the light curve `.fits` file

    Raises
    ------
    RuntimeError
        if the light curve file cannot be read

    Returns
    -------
    (int, dict)
        The extracted metadata

    """
    metadata = {}
    try :
        with fits.open(light_curve_path, mode="readonly") as hdulist:
            TICID = hdulist[0].header['TICID']
            metadata['SECTOR'] = hdulist[0].header['SECTOR']
            metadata['TICVER'] = hdulist[0].header['TICVER']
    # This exception is raised when reading a corrupted file
    except OSError as e:
        logging.warning("OSError : {}".format(e))
        logging.warning("Unreadable file : {}".format(light_curve_path))
        raise RuntimeError
    except:
        logging.warning("Unexpected error: {}".format(sys.exc_info()[0]))
        logging.warning("Unreadable file : {}".format(light_curve_path))
        raise RuntimeError

    return TICID, metadata


def extracttic(light_curves_path, pickle_path, force_extract=False):
    """Retrieve some fields in the headers of TESS `.fits` light curve files and exports them in a dictionary.

    Metadata of all files under `light_curve_path` are extracted into a dictionary.
    The keys of the dictionary are the TICID of the observed objects. The values of
    the entries are lists containing one or more dictionaries. One for each observation.
    The structure of an entry is :
        {int: [{'TICVER': int, 'SECTOR': int, 'path': str},]}
    If an exception is raised while readind the file, the `'TICVER'` and `'SECTOR'` fields are not present in the entry.

    Parameters
    ----------
    light_curve_path: path-like object
        path to the folder containing the light curves
    pickle_path: path-like object
        path to the `.pickle` file used to store the extracted data
    force_extract: bool
        True to force TIC extraction even if up-to-date data is found on storage

    """
    sector_dirs = sorted([d for d in os.listdir(light_curves_path) if isdir(join(light_curves_path, d))])
    # get sector numbers
    sectors = set([int(s.split("_")[1]) for s in sector_dirs])
    # dict to store the light curves' metadata
    light_curves = {}

    logging.info("#############################################")
    logging.info("#### Extract TIC from light curves files ####")
    logging.info("#############################################")
    logging.info("The following observation sectors are available on storage: {}".format((sectors)))

    # Load previously extracted data
    try:
        existing_data = load_pickle(pickle_path)
        existing_sectors = set()

        # Get the sectors present in the extracted data
        for tic, existing_lcs in existing_data.items():
            for lc in existing_lcs:
                if tic != None:
                    existing_sectors.add(lc['SECTOR'])
        logging.info("Found sectors {} in extracted data".format((existing_sectors)))

        if existing_sectors == sectors:
            if force_extract:
                logging.info("No new data available, extracting TIC again anyway")
                logging.info("--------------------------------------------------")
            else:
                logging.info("No new data available, skipping TIC extraction")
                logging.info("----------------------------------------------")
                return
        else:
            new_sectors = sectors.difference(existing_sectors)
            logging.info("New sectors available : {}".format(new_sectors))
            new_sector_dirs = []

            for s in new_sectors:
                s_dir = [d for d in sector_dirs if str(s) in d][0]
                new_sector_dirs.append(s_dir)
            
            sector_dirs = new_sector_dirs
            logging.info("Starting extraction for new sectors")
            logging.info("-----------------------------------")

    # Exception raised by load_pickle() if the requested file is not found on storage
    except EnvironmentError:
        logging.info("Starting TIC extraction")
        logging.info("-----------------------")

    for sector in sector_dirs:
        n = 0
        e = 0
        sector_dir_path = join(light_curves_path, sector)
        light_curve_files = [f for f in os.listdir(sector_dir_path) if isfile(join(sector_dir_path, f))]
        lc_in_sector = len(light_curve_files)

        logging.info("Starting {}".format(sector))
        logging.info("Number of light curve files found : {}".format(lc_in_sector))
        
        for light_curve in light_curve_files:
            light_curve_path = join(sector_dir_path, light_curve)

            try:
                TICID, metadata = get_light_curve_metadata(light_curve_path)
                n += 1
            # If the file cannot be read
            except RuntimeError:
                # Paths of corrupted files is stored under the None key
                TICID = None
                metadata = {}
                e += 1

            metadata['path'] = light_curve_path

            if TICID in light_curves:
                light_curves[TICID] += [metadata]
            else:
                light_curves[TICID] = [metadata]

        logging.info("Number of light curves added : {}".format(n))
        logging.info("Number of light curves not added : {}".format(e))
    
    # Add the loaded data to the newly extracted data
    light_curves.update(existing_data)
    
    # The number of observed objects is the number of entries in the light_curves dictionary minus one because the key "None" holds the paths to corrupted files
    object_number = len(light_curves) - 1
    # Count the nomber of light curves
    lc_number = 0
    for tic, data in light_curves.items():
        if tic != None:
            for lc in data:
                lc_number += 1

    logging.info("Finished extracting data")
    logging.info("------------------------")
    logging.info("Total number of light curve files processed : {}".format(lc_number))
    logging.info("Total number of objects observed : {}".format(object_number))

    save_to_pickle(light_curves, pickle_path)
