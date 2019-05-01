# Catascript

A module that builds a SQL Alchemy database with specified database fields, with a primary key being the TESS id (TIC). 
These TICs have the particularity of all having at least one corresponding light curve, as given by extracttic

## Getting started

### Setup
In order to setup the module, you need to create an actual `.env` file. To do so, run in your terminal, from the `catascript` folder :

```sh
cp .env.template .env
```

Then open the new `.env` file, and file out the right value for your setup.

#### Launch boolean environment variable

The `.env` file, you can set the boolean **RE_LAUNCH** to either `1` to entail a complete recompute of `catascript`, or to `0`, in order to only re-initialize the database. This is true whatever way of launching is chosen.

### Data root environment variable

in order to be able to launch catascript as part of a processed launched by `docker-compose`, as described in the `README` of the project's main folder, the **DATA_ROOT** specified in `.env` must indicate the location of the data folder comparatively to the code volume.

This means, if taking into consideration the structure given in `docker-compose.yml`, we need to have : 

```
DATA_ROOT = ./../data
PATH_TO_EXTRACTED_TICS = ./../data/processed/dict_TIC.pickle
```

### Prerequisites
In order to be able to execute *catascript*, you need to have the results of the extrattic script stored at the location given by the **PATH_TO_EXTRACTED_TICS** environment variable. If not available, the program will fail.

## Structure

The structure of the module is as follows : 

```sh
├── base.py
├── catascript.py
├── __init__.py
├── models.py
└── README.md
```

Please note that :
* `base.py` contains the tools for SqlAlchemy database
* `models.py` defines the structure of the database
* `catascript.py` is the actual script performing on the catalog