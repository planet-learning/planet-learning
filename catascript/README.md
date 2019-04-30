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

### Prerequisites
In order to execute *catascript*, you need to have the results of the extrattic script stored in `./data/processed.dict_TIC.pickle`.

You also need to have a running `postgresql` database as defined by the Dockerfile in `../docker/database/Dockerfile` and `../docker-compose.yml`

## Launching catascript

### Allowing launch boolean

As defined in `.env` file, you can set the boolean **RE_LAUNCH** to either `1` to entail a complete recompute of `catascript`, or to `0`, in order to only re-initialize the database. This is true whatever way of launching is chosen.

### As standalone
It is a good idea to setup a `virtualenv` before running the script for the first time. To do so, run in the main folder :

```sh
mkdir env
virtualenv env/
source ./env/bin/activate
pip install -r requirements.txt
```

Then to run it, activate your virtualenv and run the script as a module : 

```sh
source ./env/bin/activate
python -m catascript.catascript
```

### With docker-compose

If not already the case, build the dockers by running the following in the main project folder `catascript` : 

```sh
docker-compose build
```

Then run them with : 

```sh
docker-compose up
```
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