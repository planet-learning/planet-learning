from sqlalchemy import Column, String, Integer, Numeric, DateTime, Boolean, ForeignKey, BigInteger, VARCHAR
from sqlalchemy.orm import relationship

from .base import Base
"""
Database classes
"""
class Catalog(Base):
    """
    Creates a database with following attributes
	[ID] [bigint] *
	[version] [varchar](8) *
	[HIP] [int] *
	[TYC] [varchar](12) *
	[UCAC] [varchar](10) *
	[TWOMASS] [varchar](20) *
	[SDSS] [bigint] *
	[ALLWISE] [varchar](20) *
	[GAIA] [varchar](20) *
	[APASS] [varchar](30) *
	[KIC] [int] *
	[objType] [varchar](10)
	[typeSrc] [varchar](20)
	[ra] [float] *
	[dec] [float] *
    [SECTOR] [int] *
    [path] [varchar 300]
    [already_confirmed] [boolean]
    """
    __tablename__="catalog"
    ID = Column(BigInteger, primary_key = True)
    version = Column("version", VARCHAR(8))
    HIP = Column("HIP", Integer)
    TYC = Column("TYC", VARCHAR(12))
    UCAC = Column("UCAC", VARCHAR(10))
    TWOMASS = Column("TWOMASS", VARCHAR(20))
    SDSS = Column("SDSS", BigInteger)
    ALLWISE = Column("ALLWISE", VARCHAR(20))
    GAIA = Column("GAIA", VARCHAR(20))
    APASS = Column("APASS", VARCHAR(30))
    KIC = Column("KIC", Integer)
    objType = Column("objType", VARCHAR(10))
    typeSrc = Column("typeSrc", VARCHAR(20))
    ra = Column("ra", Numeric)
    dec = Column("dec", Numeric)
    SECTOR = Column("SECTOR", Integer)
    path = Column("path", VARCHAR(300))
    already_confirmed = Column("already_confirmed", Boolean)

    #One to one relationship with Confirmed
    planets_information = relationship("Confirmed", uselist=False, back_populates="related_catalog_entry")

    def __init__(self, value_fields_dict):
        """
        Creates another entry in the database

        Parameters
        ----------
        value_fields_dict: dict
            Dict containing the fields and values of the entry to create
        """
        #Setting the attributes
        for (key, value) in value_fields_dict.items():
            setattr(self, key, value)
        
        #Initializes already_confirmed attribute to false for latter processing
        self.already_confirmed = False

        #Idem for planets_information
        self.planets_information = None

class Confirmed(Base):
    """
    Creates a database with following attributes

    Host_name [Varchar(40)]
    Discovery_Method [Varchar(50)]
    Controversial_flag [integer]
    Number_planets_in_system [integer]
    Orbital_Period [float]
    Ra_sex [float]
    Ra_deg [float]
    Dec_sex [float]
    Dec_deg [float]
    HIP_Name [varchar(25)]
    Proper_Motion_ra [float]
    Proper_Motion_dec [float]
    """
    __tablename__ = "confirmed"
    ID = Column(BigInteger, primary_key=True)
    Host_name = Column("Host_name", VARCHAR(40))
    Discovery_Method = Column("Discovery_method", VARCHAR(50))
    Controversial_flag = Column("Controversial_flag", Integer)
    Number_planets_in_system = Column("Number_planets_in_system", Integer)
    Orbital_Period = Column("Orbital period", Numeric)
    Ra_sex = Column("Ra_sex", Numeric)
    Ra_deg = Column("Ra_deg", Numeric)
    Dec_sex = Column("Dec_sex", Numeric)
    Dec_deg = Column("Dec_deg", Numeric)
    HIP_Name = Column("HIP Name", VARCHAR(25))
    Proper_Motion_ra = Column("Proper_Motion_ra", Numeric)
    Proper_Motion_dec = Column("Proper_Motion_dec", Numeric)

    #One to one relationship with Confirmed
    related_catalog_entry = relationship("Catalog", uselist=False, back_populates="planets_information")

    def __init__(self, value_fields_dict, related_catalog_entry):
        """
        Creates another entry in the database

        Parameters
        ----------
        value_fields_dict: dict
            Dict containing the fields and values of the entry to create
        related_catalog_entry: Catalog entry
            The corresponding catalog entry
        """
        #Setting the attributes
        for (key, value) in value_fields_dict.items():
            setattr(self, key, value)

        #Initializing number of planets
        self.Number_planets_in_system = 1

        #Linking to the corresponding catalog entry
        self.related_catalog_entry = related_catalog_entry

    def increment_number_planets():
        """
        Increments by one the number of planets of an entry
        """
        self.Number_planets_in_system = self.Number_planets_in_system + 1
        