import os
from os.path import isdir, isfile, join

from dotenv import load_dotenv

from .extracttic.extracttic import extracttic, save_to_pickle
from .catascript.catascript import catascript

load_dotenv()


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
    catascript()
    light_curves = extracttic(light_curves_path)
    save_to_pickle(light_curves, save_path)


