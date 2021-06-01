from sqlalchemy import Column, String, Integer, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

import config

Base = declarative_base()

engine = create_engine(
    f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@ec2-108-128-104-50.eu-west-1.compute.amazonaws.com:5432/dbk3qt8k0c5sig"
)
Base.metadata.create_all(engine)


class Location(Base):
    __tablename__ = "locations"

    def __init__(self, name):
        self.name = name

    id = Column(Integer, primary_key=True)
    name = Column(String)


class WeatherItem(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True)
    location = Column(Integer, ForeignKey("locations.id"), nullable=False)
    date = Column(Date)
    temperature = Column(Float)
