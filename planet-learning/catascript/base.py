import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

#Loading environment variables
load_dotenv()
ENGINE = os.getenv("ENGINE_URL")

#Creating engine, session and base class
engine = create_engine(ENGINE)
Session = sessionmaker(bind=engine)
Base = declarative_base()