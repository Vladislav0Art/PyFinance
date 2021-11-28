from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# important to import models to make Base.metadata.create_all(ENGINE) work
import models
from config import config


# Create engine based on the db specified in our config
ENGINE = create_engine(config.DATABASE, echo=False, connect_args={"check_same_thread": False})

# Create all tables if they don't exist
config.Base.metadata.create_all(ENGINE)

# Define session object which we'll instantiate in other modules
Session = sessionmaker(ENGINE)