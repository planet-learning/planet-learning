import os
import pickle
from os.path import isdir, isfile, join
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from dotenv import load_dotenv

load_dotenv()


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
    with open(processed_dir_path + "/dict_TIC.pickle", 'wb') as p:
        pickle.dump(data, p)


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
    except OSError :
        TICID = None

    return TICID, metadata


def get_light_curves(light_curves_path, verbose=True):
    sector_dirs = sorted([d for d in os.listdir(light_curves_path) if isdir(join(light_curves_path, d))])
    light_curves = {}

    if verbose:
        print("")
        print("#############################################")
        print("#### Extract TIC from light curves files ####")
        print("#############################################")
        print("")
        print("The following observation sectors are available :")
        print((" - {}\n"*len(sector_dirs)).format(*sector_dirs))
        print("")

    for sector in sector_dirs:
        sector_dir_path = join(light_curves_path, sector)
        light_curve_files = [f for f in os.listdir(sector_dir_path) if isfile(join(sector_dir_path, f))]

        if verbose:
            print("")
            print("Starting {}".format(sector))
            print("Number of light curves found : {}".format(len(light_curve_files)))
            print("")
        
        for light_curve in light_curve_files:
            light_curve_path = join(sector_dir_path, light_curve)

            TICID, metadata = get_light_curve_metadata(light_curve_path)
            metadata['path'] = light_curve_path

            if TICID in light_curves:
                light_curves[TICID] += [metadata]
            else:
                light_curves[TICID] = [metadata]
            
            if verbose:
                if not 'SECTOR' in metadata:
                    print("error : {}".format(light_curve_path))

    return light_curves


if __name__ == '__main__':
    light_curves = get_light_curves(light_curves_path)
    # print(light_curves)

    save_to_pickle(light_curves)
