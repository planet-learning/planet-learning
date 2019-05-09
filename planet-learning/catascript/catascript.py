import csv
import logging
import os
import pickle
from os.path import join

import numpy as np
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from .base import Base, Session, engine
from .confirmed import process_confirmed
from .models import Catalog

"""
catascript is a module that builds a SQL Alchemy database with specified database fields, with a primary key being the TESS id (TIC). 
These TICs have the particularity of all having at least one corresponding light curve.
"""

#Loading functions
def get_catalog_files():
    """
    Get all catalog filenames present in the data/catalog folder

    :returns: the list of filenames
    :rtype: list
    """
    #Get path and all file names
    data_root = os.getenv("DATA_ROOT")
    catalog_path = data_root + "/catalog/"
    file_names = os.listdir(catalog_path)

    #Extract the csv files
    catalog_files = []
    for file_name in file_names:
        if file_name.endswith(".csv"):
            catalog_files.append(catalog_path + file_name)
    
    #Results
    return catalog_files

def load_TICS_dict():
    """
    This function loads the dictionnary of extracted TICS that have a ligth curve (it was extracted and stored by the extrattic module)

    :returns: a dictionnary containing the (TIC, list of name_of_ligthcurve_file) pairs.
    :rtype: dict
    """

    path_to_load = join(os.getenv("DATA_ROOT"), os.getenv("PROCESSED_DIR"), os.getenv("EXTRACTED_TICS_FILE"))
    with open(path_to_load, 'rb') as pickle_dict:
        dict_TICS = pickle.load(pickle_dict)
    return dict_TICS

#Preprocessing function
def preprocess_catalog_line(catalog_line):
    """
    Preprocess the given catalog line into a dict with (name of field in the database, value for this line) entries.

    :param catalog_line:
    :type catalog_line: list

    :returns: the processed line
    :returns: dict
    """
    #Getting fields (in order)
    list_of_fields = (os.getenv("LIST_DB_FIELDS")).split(',')

    #Creating dict 
    catalog_line_dict = {}

    #Adding values, taking into account missing ones
    for (index, field) in enumerate(list_of_fields):
        if catalog_line[index] != '':
            catalog_line_dict[field] = catalog_line[index]
        else:
            catalog_line_dict[field] = None

    #results
    return catalog_line_dict

#Checking functions
def check_in_TICS_dict(TIC_in_catalog, TICS_dict):
    """
    This function checks for the existence of a specified TIC in the dictionnary of TICS of which we have a ligth curve 
    and returns the corresponding boolean.

    :param TIC_in_catalog: the TIC we want to check
    :type TIC_in_catalog: str
    :param TICS_dict: the dict of extracted TICS given by load_TICS_dict
    :type TICS_dict: {int: list} dict. The list is for taking into account repetitions of a TIC visualisation.

    :returns: (boolean indicating existence, value of the dict entry if existing)
    :rtype: (bool, (str, {str dict} list)) tuple
    """
    TIC_in_catalog = int(TIC_in_catalog)

    if TIC_in_catalog in TICS_dict.keys():
        return( (True, TICS_dict[TIC_in_catalog]))

    else:
        return ( (False, ("", []))) #we return False and default values

def check_exists_other_ID(catalog_line):
    """
    Checks if the given line has another ID than a TIC

    :param catalog_line: line of catalog currently being examined
    :type catalog_line: dict

    :returns: boolean indicating at least one other ID found, (name of mission ID, ID) dictionnary of found IDs
    :rtype: (bool, dict) tuple
    """
    #Getting the fields corresponding to ids
    list_of_ids = (os.getenv("OTHER_MISSIONS_IDS")).split(',')

    #Dictionnary of found other ids
    found_ids = {}
    flag = False

    #Checks for the existence of other ids
    for id_mission_name in list_of_ids:
        if catalog_line[id_mission_name] != None:
            flag = flag or True
            found_ids[id_mission_name] = catalog_line[id_mission_name]
    
    #Results
    return((flag, found_ids))

#Database relation functions
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
    try:
        new_entry = Catalog(value_fields_dict)
        session.add(new_entry)
        session.commit()
    except (IntegrityError, UniqueViolation):
        #There is already an entry in the database
        pass
    session.close

#Main function
def catascript():
    """
    Builds a database containing the TESS ID (TIC), IDs for other missions, ra and dec value.
    It then fills it with the catalog entries that have a light curve (found in a previously extracted dictionnary) and other mission ID.
    """
    logging.info("Launching : catascript")

    #get catalog files
    catalog_files_list = get_catalog_files()

    #extract TICS_dict
    logging.info("Loading : TICS dict ... ")
    TICS_dict = load_TICS_dict()
    logging.info("Done.")

    #inialize database
    logging.info("Initializing : database ... ")
    initialize_database()
    logging.info("Done.")

    #get re_launch boolean
    need_re_launch = int(os.getenv("RE_LAUNCH"))

    #check if a recompute is being asked
    if need_re_launch:
        #loop over catalog lines in catalog
        for catalog_file in catalog_files_list:
            with open(catalog_file, newline='') as catalog_csv:
                catalog_reader = csv.reader(catalog_csv, delimiter=',', quotechar='|')
                logging.info("Processing : catalog {} ... ".format(catalog_file))
                
                #Iteration on each line of the csv file
                for catalog_line in catalog_reader:
                    #preprocess that line to put in a good format
                    catalog_line_values = preprocess_catalog_line(catalog_line)
                    TIC_in_catalog = catalog_line_values["ID"]

                    #check if match with a TIC with known light curve
                    (TIC_in_dict, dict_values) = check_in_TICS_dict(TIC_in_catalog, TICS_dict)
                    if TIC_in_dict:

                        #check for existence of other missions IDs
                        (exists_other_ids, corresponding_ids) = check_exists_other_ID(catalog_line_values)
                        if exists_other_ids:

                            # add values extracted from the tic stored dictionnary in the catalog line to be stored in the database
                            catalog_line_values['SECTOR'] = dict_values[0]['SECTOR']
                            catalog_line_values['path'] = dict_values[0]['path']

                            # add entry to database
                            add_entry_to_database(catalog_line_values)

                logging.info("Processing {} : Done".format(catalog_file))

        #Processing confirmed catalog
        process_confirmed()

        logging.info("Done : catascript - recomputed entries")
    
    else:
        logging.info("Done : catascript - no new computing performed")

if __name__ == "__main__":
    catascript()
