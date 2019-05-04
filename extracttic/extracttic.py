import logging
import os
import pickle
from os.path import isdir, isfile, join

import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from dotenv import load_dotenv

load_dotenv()


if not isdir('log'):
        os.mkdir('log')

logging.basicConfig(
    filename='log/extracttic.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


DATA_ROOT = os.getenv('DATA_ROOT')
LIGHT_CURVES_DIR = os.getenv('LIGHT_CURVES_DIR')
PROCESSED_DIR = os.getenv('PROCESSED_DIR')
light_curves_path = join(DATA_ROOT, LIGHT_CURVES_DIR)
processed_dir_path = join(DATA_ROOT, PROCESSED_DIR)


def save_to_pickle(data):
    # Create the "processed" directory if it is missing
    if not isdir(processed_dir_path):
        os.mkdir(processed_dir_path)
    
    # Write the data into a pickle file
    logging.info("Saving data")
    save_path = join(processed_dir_path, "dict_TIC.pickle")
    with open(save_path, 'wb') as p:
        pickle.dump(data, p)
    logging.info("Data saved in {}".format(save_path))


def get_light_curve_metadata(light_curve_path):
    """
    Retrieve metadata from a light curve '.fits' file
    A description the content of the light curves files can be found here :
        https://archive.stsci.edu/files/live/sites/mast/files/home/missions-and-data/active-missions/tess/_documents/EXP-TESS-ARC-ICD-TM-0014.pdf
    The collected fields are the following :
        - SECTOR
        - TICVER
    The data is returned as :
        - an integer 'TICID' representing the TIC ID of the observed object
        - a dictionnary 'metadata' with the name of the collected fields as keys
    """
    metadata = {}
    try :
        with fits.open(light_curve_path, mode="readonly") as hdulist:
            TICID = hdulist[0].header['TICID']
            metadata['SECTOR'] = hdulist[0].header['SECTOR']
            metadata['TICVER'] = hdulist[0].header['TICVER']
    # This exception is raised when reading a corrupted file
    except (OSError, Exception) as e:
        logging.warning("Unreadable file : {}".format(light_curve_path))
        logging.warning("Unreadable file : {}".format(e))
        TICID = None

    return TICID, metadata


def get_light_curves(light_curves_path, verbose=True):
    sector_dirs = sorted([d for d in os.listdir(light_curves_path) if isdir(join(light_curves_path, d))])
    light_curves = {}
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

            TICID, metadata = get_light_curve_metadata(light_curve_path)
            metadata['path'] = light_curve_path

            if TICID in light_curves:
                light_curves[TICID] += [metadata]
            else:
                light_curves[TICID] = [metadata]
            
            if 'SECTOR' in metadata:
                n += 1
            else:
                e += 1
        
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
    light_curves = get_light_curves(light_curves_path)
    # logging.info(light_curves)

    save_to_pickle(light_curves)
