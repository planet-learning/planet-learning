import csv
import logging
import os
import pickle
from os.path import join

import numpy as np
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from .base import Base, Session, engine
from .models import Catalog, Confirmed


"""
catascript.confirmed updates the already_confirmed attribute of the database build by catascript by looking up to the confirmed exoplanets catalog.
"""

#Preprocessing function
def preprocess_catalog_line(catalog_line):
    """
    Preprocess the given catalog line into a dict with (name of field in the database, value for this line) entries.

    Parameters
    ----------
    catalog_line: list
        the line of the csv to process

    Returns
    -------
    catalog_line_dict: dict
        the dict containing the entries of the catalog line
    """
    #Getting fields (in order)
    list_of_fields = (os.getenv("LIST_CONFIRMED_FIELDS")).split(',')
    #Creating dict 
    catalog_line_dict = {}

    #Adding values, taking into account missing ones
    for (index, field) in enumerate(list_of_fields):
        if catalog_line[index] != '':
            #conversion for numeric fields
            if field == "Controversial flag":
                catalog_line_dict[field] = int(catalog_line[index])                
            else:
                catalog_line_dict[field] = catalog_line[index]
        else:
            catalog_line_dict[field] = None

    #results
    return catalog_line_dict

#Query fucntions
def add_or_update_confirmed(value_fields_dict, catalog_id):
    """
    This function adds a new value to the database (without commiting it)
    It matches the list of all possible fields given with the keys of the value of fields dictionnary, 
    filling with None if there is not such value for that host.

    Parameters
    ----------
    value_fields_dict: dict
        dictionary containing the value for each of the needed fields for that host entry.
    catalog_id : int
    """
    session = Session()
    try:
        #Querying database
        check_exists_db = session.query(Confirmed).filter(Confirmed.catalog_id == catalog_id).limit(1).all()
        if check_exists_db:
            raise IntegrityError

        #Adding new entry
        logging.info(value_fields_dict)
        new_entry = Confirmed(value_fields_dict, catalog_id)
        session.add(new_entry)
        session.commit()

    except (IntegrityError, UniqueViolation):
        #There is already an entry in the database
        host = session.query(Confirmed).filter(Confirmed.catalog_id == catalog_id).limit(1).all()
        host[0].increment_number_planets()
    finally:
        session.close()

#Processing functions
def checks_star_exists_in_database_and_update(processed_catalog_line):
    """
    This function checks if the HIP identifier of the confirmed line is in the database. If it isn't, we check for th ra and dec values.

    Parameters
    ----------
    processed_catalog_line : dict
        the dict containing the processed catalog line

    """
    HIP_identifier = processed_catalog_line["HIP Name"]

    #If there is an HIP identifier    
    if HIP_identifier:
        HIP_identifier = int(HIP_identifier.split(' ')[1])
        session = Session() 
        try:
            search_for_HIP = session.query(Catalog).filter(Catalog.HIP == HIP_identifier).limit(1).all()

            #Modifying Catalog entry
            catalog_entry = search_for_HIP[0]
            catalog_entry.update_already_confirmed()
            catalog_id = catalog_entry.ID 

            #Closing first session
            session.commit()
            session.close()
            

            #Creating or updating a Confirmed entry
            add_or_update_confirmed(processed_catalog_line, catalog_id)

            logging.info("HIP : \n Modifying entry for : {}, with TIC : {}".format(processed_catalog_line["Host name"], catalog_id))

        except (IndexError):
            #Closing the opened session
            session.close() 

    #Else, we search by ra and dec (in degrees in the database)
    else:
        Ra = float(processed_catalog_line["Ra_deg"])
        Dec = float(processed_catalog_line["Dec_deg"])
        accepted_error_margin = 0.000001

        session = Session()
        try:
            #Queries
            search_for_Ra = session.query(Catalog).filter(Catalog.ra > Ra-accepted_error_margin).filter(Catalog.ra < Ra + accepted_error_margin)
            search_for_Dec_and_Ra = search_for_Ra.filter(Catalog.dec > Dec-accepted_error_margin).filter(Catalog.dec < Dec + accepted_error_margin).limit(1).all()

            #Modifying Catalog entry
            catalog_entry = search_for_Dec_and_Ra[0]
            catalog_entry.update_already_confirmed()
            catalog_id = catalog_entry.ID 

            #Closing this first session
            session.commit()
            session.close()
            
            #Creating or updating a Confirmed entry, updating Catalog entry
            add_or_update_confirmed(processed_catalog_line, catalog_id)
            
            logging.info("Dec/Ra : \n Modifying entry for : {}, with TIC : {}".format(processed_catalog_line["Host name"], catalog_id))
        
        except (IndexError):
            #Closing the opened session
            session.close()

def process_confirmed():
    """
    This function processes the confirmed exoplanets catalog

    """
    logging.info("Processing : catascript, confirmed catalog")
    #get the file
    catalog_file = join(os.getenv("DATA_ROOT"), os.getenv("CONFIRMED_DIR"), os.getenv("CONFIRMED_CATALOG_FILE"))
    #get the number of rows in header (skipped in the processing)
    nb_rows_header = int(os.getenv("NB_ROWS_HEADER"))

    #open the file
    with open(catalog_file, newline='') as catalog_csv:
        catalog_reader = csv.reader(catalog_csv, delimiter=',', quotechar='|')

        #Skipping header rows
        for i in range(nb_rows_header):
            next(catalog_reader)

        #Iteration on each line of the csv file
        for catalog_line in catalog_reader:
            processed_catalog_line = preprocess_catalog_line(catalog_line)
            checks_star_exists_in_database_and_update(processed_catalog_line)
        
    #logging.info number of confirmed systems are in database

    logging.info("Done : catascript, confirmed catalog")
