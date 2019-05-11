import csv
import logging
import os
import pickle
from os.path import join

import numpy as np

from .base import Base, Session, engine
from .models import Catalog


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
            logging.info(" ")
            logging.info("HIP : \n Modifying entry for : {}".format(processed_catalog_line))
            search_for_HIP[0].already_confirmed = True
             
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
            logging.info(" ")
            logging.info("Dec/Ra : \n Modifying entry for : {}".format(processed_catalog_line))
            search_for_Dec_and_Ra[0].already_confirmed = True
             
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
    nb_rows_header = os.getenv("NB_ROWS_HEADER")

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

if __name__ == "__main__":
    process_confirmed()
