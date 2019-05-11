# ExtractTIC

A module that reads metadata from TESS `.fits` light curves to extract the following data :
- `TICID`
- `TICVER`
- `SECTOR`

See the [TESS Science Data Products Description Document](https://archive.stsci.edu/files/live/sites/mast/files/home/missions-and-data/active-missions/tess/_documents/EXP-TESS-ARC-ICD-TM-0014.pdf) for more information about these fields.

Data is compiled in a dictionary and save in a `pickle` for later use.

## Getting started

### Setup

This module requires the presence of a `.env` file containing some configuration variables in the root directory. You can copy-paste it from the template provided.

```sh
cp .env.template .env
```

The required files in the `.env` file are the following :

```py
DATA_ROOT = /path/to/data/folder #/planet-learning/data
LIGHT_CURVES_DIR = name_of_the_folder_containing the light_curves #light_curves
PROCESSED_DIR = name_of_the_folder_containing the processed_data #processed
EXTRACTED_TICS_FILE = name_of_the_file_holding_the_extracted_tic_data #dict_TIC.pickle
FORCE_TIC_EXTRACTION=1 or 0
```

`FORCE_TIC_EXTRACTION` should be set to `1` to force re-extracting TICs from all available light curves. Set this to `0` to extract only new sectors that are not yet extracted.

In the example, the data is structured like the following :

```py
.
└── data/
    ├── light_curves/ # put the .fits light curves file here
    │   ├── sector_1/
    │   └── ...
    └── processed/
        └── dict_TIC.pickle
```

>Keep in mind that no space can be present around the "=" sign between the variable name and its value in the `.env` file since it is used by docker and by python

### Requirements

Light curves '.fits' files from TESS must be present in the `LIGHT_CURVES_DIR` directory.

## Folder structure

```py
.
├── extracttic.py
├── __init__.py
└── README.md
```