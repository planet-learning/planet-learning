import logging
import os
from os.path import isdir, isfile, join

from dotenv import load_dotenv

from .catascript.catascript import catascript
from .extracttic.extracttic import extracttic, save_to_pickle

load_dotenv()


# Create the directory to store the logs on first run
if not isdir('log'):
        os.mkdir('log')


DATA_ROOT = os.getenv('DATA_ROOT')
LIGHT_CURVES_DIR = os.getenv('LIGHT_CURVES_DIR')
PROCESSED_DIR = os.getenv('PROCESSED_DIR')
light_curves_path = join(DATA_ROOT, LIGHT_CURVES_DIR)

processed_dir_path = join(DATA_ROOT, PROCESSED_DIR)
# Create the "processed" directory if it is missing
if not isdir(processed_dir_path):
    os.mkdir(processed_dir_path)

EXTRACTED_TICS_FILE = os.getenv('EXTRACTED_TICS_FILE')
save_path = join(processed_dir_path, EXTRACTED_TICS_FILE)


if __name__ == '__main__':
    # Configuration of the logging module
    logging.basicConfig(
        filename='log/catascript.log',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    catascript()
    
    # Configuration of the logging module
    logging.basicConfig(
        filename='log/extracttic.log',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    light_curves = extracttic(light_curves_path)
    save_to_pickle(light_curves, save_path)
