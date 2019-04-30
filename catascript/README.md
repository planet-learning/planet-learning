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