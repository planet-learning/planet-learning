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
from dotenv import load_dotenv

load_dotenv()


# Create the directory to store the logs on first run
if not isdir('log'):
        os.mkdir('log')
# Configuration of the logging module
logging.basicConfig(
    filename='log/extracttic.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def save_to_pickle(data, path):
    """Save a python object into a `.pickle` file.
    
    Data is saved in binary format.


    :param data: object to save
    :type data: any python object
    :param path: path to the file to write
    :type path: path-like object

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


    :param light_curve_path: path to the light curve `.fits` file
    :type light_curve_path: path-like object
    :raises RuntimeError if the light curve file cannot be read
    :returns: The extracted metadata
    :rtype: int, dict

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


def extracttic(light_curves_path):
    """Retrieve some fields in the headers of TESS `.fits` light curve files and exports them in a dictionary.

    Metadata of all files under `light_curve_path` are extracted into a dictionary.
    The keys of the dictionary are the TICID of the observed objects. The values of
    the entries are lists containing one or more dictionaries. One for each observation.
    The structure of an entry is :
        {int: [{'TICVER': int, 'SECTOR': int, 'path': str},]}
    If an exception is raised while readind the file, the `'TICVER'` and `'SECTOR'` fields are not present in the entry.


    :param light_curves_path: path to the folder containing the light curves
    :type light_curve_path: path-like object
    :returns light_curves: dictionary holding the extracted metadata
    :rtype: dict

    """
    sector_dirs = sorted([d for d in os.listdir(light_curves_path) if isdir(join(light_curves_path, d))])
    # dict to store the light curves' metadata
    light_curves = {}
    # Keep track of the number of file processed
    lc_number = 0

    logging.info("#############################################")
    logging.info("#### Extract TIC from light curves files ####")
    logging.info("#############################################")
    logging.info("The following observation sectors are available : {}".format(" | ".join(sector_dirs)))

    for sector in sector_dirs:
        n = 0
        e = 0
        sector_dir_path = join(light_curves_path, sector)
        light_curve_files = [f for f in os.listdir(sector_dir_path) if isfile(join(sector_dir_path, f))]
        lc_in_sector = len(light_curve_files)

        logging.info("Starting {}".format(sector))
        logging.info("Number of light curves file found : {}".format(lc_in_sector))
        
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
        
        lc_number += n

        logging.info("Number of light curves added : {}".format(n))
        logging.info("Number of light curves not added : {}".format(e))
    
    # The number of observed objects is the number of entries in the light_curves dictionary minus one because the key "None" holds the paths to corrupted files
    object_number = len(light_curves) - 1

    logging.info("Finished extracting data")
    logging.info("Light curve files processed : {}".format(lc_number))
    logging.info("Number of objects observed : {}".format(object_number))

    return light_curves


if __name__ == '__main__':
    light_curves = extracttic(light_curves_path)
    save_to_pickle(light_curves, save_path)
