import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Obtener datos de conexión desde variables de entorno
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

DATABASE_URL = f"mysql+pymysql://admin:alberto05@bazar.c36mijirazht.us-east-1.rds.amazonaws.com/inventory"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

DATABASE_URL_USER = f"mysql+pymysql://admin:alberto05@bazar.c36mijirazht.us-east-1.rds.amazonaws.com/user"
engine_user = create_engine(DATABASE_URL_USER)
SessionLocalUser = sessionmaker(autocommit=False, autoflush=False, bind=engine_user)
BaseUser = declarative_base()
