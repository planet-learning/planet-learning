import csv
import os
import numpy as np

from catascript.base import Base, Session, engine
from catascript.models import Catalog
"""
catascript is a module that builds a SQL Alchemy database with specified database fields, with a primary key being the TESS id (TIC). 
These TICs have the particularity of all having at least one corresponding light curve.


TODO : 
    - preprocess_list_of_db_fields(list_of_db_fields) : takes as given by .env file, and builds a list of the fields
    - preprocess_catalog_line(catalog_line) : takes in input a catalog_line as read from a catalog.csv, and outputs its content in a dict
    - make_dict_value_fields_from_catalog_line (catalog_line, list_of_db_fields) : makes dict of value_fields for this catalog line
"""

def load_TICS_dict(path):
    """
    This function loads the dictionnary of extracted TICS that have a ligth curve (it was extracted and stored by the extrattic module)

    :param path: path to the saved dictionnary. It is specified in .env file.
    :type path: str

    :returns: a dictionnary containing the (TIC, list of name_of_ligthcurve_file) pairs.
    :rtype: dict
    """
    pass

def check_in_TICS_dict(TIC_in_catalog, TICS_dict):
    """
    This function checks for the existence of a specified TIC in the dictionnary of TICS of which we have a ligth curve 
    and returns the corresponding boolean.

    :param TIC_in_catalog: the TIC we want to check
    :type TIC_in_catalog: str
    :param TICS_dict: the dict of extracted TICS given by load_TICS_dict
    :type TICS_dict: dict

    :returns: (boolean indicating existence, value of the dict entry if existing)
    :rtype: (bool, (str, str list)) tuple
    """
    pass

def check_exists_other_ID(catalog_line):
    """
    Checks if the given line has another ID than a TIC

    :param catalog_line: line of catalog currently being examined
    :type catalog_line: list ?

    :returns: boolean indicating at least one other ID found, (name of mission ID, ID) dictionnary of found IDs
    :rtype: (bool, dict) tuple

    TODO : 
        - define the type of catalog_line
    """
    pass

def initialize_database():
    """
    This function initializes a database with SQL Alchemy ; its model is located in catascript.base.Catalog
    """
    #instantiates database
    Base.metadata.create_all(engine)

def add_entry_to_database(value_fields_dict):
    """
    This function adds a new value to the database. 
    It matches the list of all possible fields given with the keys of the value of fields dictionnary, 
    filling with None if there is not such value for that TIC.

    :param value_fields_dict: dictionary containing the value for each of the needed fields for that TIC entry.
    :type value_fields_dict: dict
    """
    session = Session()
    Catalog(value_fields_dict)
    session.commit()
    session.close

def catascript():
    """
    Builds a database containing the TESS ID (TIC), IDs for other missions, ra and dec value.

    It loads from the .env file :
        - the path to the saved dictionnary of TIC IDs
        - the list of fields to include in the database
        - the engine url for the database

    """
    #load engine_url
    #extract TICS_dict
    #process list_of_db_fields (if needed)
    #inialize database
    #loop over catalog lines in catalog
        #preprocess that line to put in a good format
        #check if match with a TIC with known light curve
            #check for existence of other missions IDs
                # make dict of value_fields for this catalog line
                # add entry to database
    
    #close database editing if such thing is necessary
    pass