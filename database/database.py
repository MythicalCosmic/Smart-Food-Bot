from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DECIMAL
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


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_name = Column(String)
    product_img = Column(String, nullable=True)
    product_price = Column(DECIMAL(20,2))


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    total_price = Column(DECIMAL(20,2))
    type = Column(String)


