from fastapi import FastAPI
from database.db import engine, Base
from models import todomodel

app = FastAPI()

Base.metadata.create_all(bind=engine)