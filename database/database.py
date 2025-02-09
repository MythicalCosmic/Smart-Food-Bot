from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker



engine = create_engine("sqlite:///database.db", echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True) 
    step = Column(String)
    latitude = Column(Float, nullable=True)  
    longitude = Column(Float, nullable=True) 


Base.metadata.create_all(engine)

