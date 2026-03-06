from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db' #address of the database

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) #actual connection & allows multiple parts of your app to use the same connection

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine) #a class that CREATES sessions whenever you call SessionLocal()

Base = declarative_base() #parent class that all your database MODELS will inherit from.

