from sqlalchemy import Column, String, Integer, Numeric, DateTime, Boolean, ForeignKey, BigInteger, VARCHAR
from sqlalchemy.orm import relationship

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
    """
    __tablename__="catalog"
    self.ID = Column(BigInteger, primary_key = True)
    self.version = Column("version", VARCHAR(8))
    self.HIP = Column("HIP", Integer)
    self.TYC = Column("TYC", VARCHAR(12))
    self.UCAC = Column("UCAC", VARCHAR(10))
    self.TWOMASS = Column("TWOMASS", VARCHAR(20))
    self.SDSS = Column("SDSS", BigInteger)
    self.ALLWISE = Column("ALLWISE", VARCHAR(20))
    self.GAIA = Column("GAIA", VARCHAR(20))
    self.APASS = Column("APASS", VARCHAR(30))
    self.KIC = Column("KIC", Intege)
    self.objType = Column("objType", VARCHAR(10))
    self.typeSrc = Column("typeSrc", VARCHAR(10))
    self.ra = Column("ra", Numeric)
    self.dec = Column("dec", Numeric)

    def __init__(self, value_fields_dict):
        """
        Creates another entry in the database
        """
        for (key, value) in value_fields_dict.items():
            self.key = value
            # setattr(self, key, value)