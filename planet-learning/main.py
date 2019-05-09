import logging
import os
from os.path import isdir, join

from dotenv import load_dotenv

from .catascript.catascript import catascript
from .extracttic.extracttic import extracttic, save_to_pickle


def create_dir(directory):
    # Create the directory to store the logs on first run
    if not isdir(directory):
            os.mkdir(directory)


if __name__ == '__main__':
    load_dotenv()


    DATA_ROOT = os.getenv('DATA_ROOT')
    LIGHT_CURVES_DIR = os.getenv('LIGHT_CURVES_DIR')
    PROCESSED_DIR = os.getenv('PROCESSED_DIR')
    EXTRACTED_TICS_FILE = os.getenv('EXTRACTED_TICS_FILE')
    light_curves_path = join(DATA_ROOT, LIGHT_CURVES_DIR)
    processed_dir_path = join(DATA_ROOT, PROCESSED_DIR)
    save_path = join(processed_dir_path, EXTRACTED_TICS_FILE)

    create_dir('log')
    create_dir(processed_dir_path)


    # Configuration of the logging module
    logging.basicConfig(
        filename='log/extracttic.log',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    light_curves = extracttic(light_curves_path)
    save_to_pickle(light_curves, save_path)

    # Configuration of the logging module
    logging.basicConfig(
        filename='log/catascript.log',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    catascript()
