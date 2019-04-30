from sqlalchemy import Column, String, Integer, Numeric, DateTime, Boolean, ForeignKey, BigInteger, VARCHAR
from sqlalchemy.orm import relationship

from catascript.base import Base
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
	[typeSrc] [varchar](10)
	[ra] [float] *
	[dec] [float] *
    [SECTOR] [int] *
    [path] [varchar 60]
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
    typeSrc = Column("typeSrc", VARCHAR(10))
    ra = Column("ra", Numeric)
    dec = Column("dec", Numeric)
    SECTOR = Column("SECTOR", Integer)
    path = Column("path", VARCHAR(60))

    def __init__(self, value_fields_dict):
        """
        Creates another entry in the database
        """
        for (key, value) in value_fields_dict.items():
            self.key = value
            # setattr(self, key, value)