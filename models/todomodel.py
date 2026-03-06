from database.db import Base
from sqlalchemy import Column, Integer,String, Boolean

class Todos(Base):
    __tablename__ = 'todos' #name of the table
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    Complete = Column(Boolean, default=False)