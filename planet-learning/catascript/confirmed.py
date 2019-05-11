import csv
import logging
import os
import pickle
from os.path import join

import numpy as np

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
            catalog_line_dict[field] = catalog_line[index]
        else:
            catalog_line_dict[field] = None

    #results
    return catalog_line_dict

#Query fucntions
def add_or_update_confirmed(value_fields_dict, catalog_entry):
    """
    This function adds a new value to the database (without commiting it)
    It matches the list of all possible fields given with the keys of the value of fields dictionnary, 
    filling with None if there is not such value for that host.

    Parameters
    ----------
    value_fields_dict: dict
        dictionary containing the value for each of the needed fields for that host entry.
    """
    try:
        new_entry = Confirmed(value_fields_dict, catalog_entry)
        session.add(new_entry)
    except (IntegrityError, UniqueViolation):
        #There is already an entry in the database
        host = session.query(Confirmed).filter(Confirmed.TIC == value_fields_dict["TIC"]).limit(1).all()
        host[0].increment_number_planets()

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
    session = Session() 

    #If there is an HIP identifier    
    if HIP_identifier:
        HIP_identifier = int(HIP_identifier.split(' ')[1])
        search_for_HIP = session.query(Catalog).filter(Catalog.HIP == HIP_identifier).limit(1).all()

        #Database modifications
        if search_for_HIP:
            #Modifying Catalog entry
            search_for_HIP[0].already_confirmed = True

            #Updating processed_catalog_line
            processed_catalog_line["TIC"] = search_for_HIP[0].ID 

            #Creating or updating a Confirmed entry
            add_or_update_confirmed(processed_catalog_line, search_for_HIP[0])

            logging.info("HIP : \n Modifying entry for : {}, with TIC : {}".format(processed_catalog_line["Host name"], processed_catalog_line["TIC"]))
             
    #Else, we search by ra and dec (in degrees in the database)
    else:
        Ra = float(processed_catalog_line["Ra_deg"])
        Dec = float(processed_catalog_line["Dec_deg"])
        #Queries
        accepted_error_margin = 0.000001
        search_for_Ra = session.query(Catalog).filter(Catalog.ra > Ra-accepted_error_margin).filter(Catalog.ra < Ra + accepted_error_margin)
        search_for_Dec_and_Ra = search_for_Ra.filter(Catalog.dec > Dec-accepted_error_margin).filter(Catalog.dec < Dec + accepted_error_margin).limit(1).all()

        #Database modifications
        if (search_for_Dec_and_Ra):
            #Modifying Catalog entry
            search_for_Dec_and_Ra[0].already_confirmed = True

            #Updating processed_catalog_line
            processed_catalog_line["TIC"] = search_for_Dec_and_Ra[0].ID 

            #Creating or updating a Confirmed entry
            add_or_update_confirmed(processed_catalog_line, search_for_Dec_and_Ra[0])
            
            logging.info("Dec/Ra : \n Modifying entry for : {}, with TIC : {}".format(processed_catalog_line["Host name"], processed_catalog_line["TIC"]))
    
    session.commit()
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
