import datetime
import csv
from collections import defaultdict

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

Base = declarative_base()


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


if __name__ == "__main__":
    engine = create_engine(
        f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@ec2-108-128-104-50.eu-west-1.compute.amazonaws.com:5432/dbk3qt8k0c5sig"
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    cache = defaultdict(set)

    try:
        locations = {
            "Moscow": "mskmay.csv",
            "Murmansk": "murmansmay.csv",
            "Nizniy Novgorod": "nizhniynovgorodmay.csv",
            "Samara": "samaramay.csv",
            "Saint Petersburg": "spbmay.csv",
        }

        for location_name, filename in locations.items():
            location_entity = (
                session.query(Location).filter_by(name=location_name).first()
            )
            if location_entity is None:
                res = session.add(Location(name=location_name))

            location_entity = (
                session.query(Location).filter_by(name=location_name).first()
            )

            with open("data\\{}".format(filename), newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter=";", quotechar="|")
                data = list(reader)[7:]
                for row in data:
                    date = datetime.datetime.strptime(row[0], "%d.%m.%Y %H:%M").date()
                    if not date in cache[location_name]:
                        cache[location_name].add(date)
                        session.add(
                            WeatherItem(
                                location=location_entity.id,
                                date=date,
                                temperature=float(row[1].replace(",", ".")),
                            )
                        )
    finally:
        session.commit()
        session.close()
