import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from models import Location
from models import WeatherItem


class NoSuchLocation(Exception):
    def __init__(self, location_name):
        super().__init__("No such location: {}".format(location_name))


class NoData(Exception):
    def __init__(self, location_name, date):
        super().__init__("No data for {} at {}".format(location_name, date))


def get_temp_for_location(location_name, date):
    engine = create_engine(
        f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@ec2-108-128-104-50.eu-west-1.compute.amazonaws.com:5432/dbk3qt8k0c5sig"
    )
    Session = sessionmaker()
    Session.configure(bind=engine)

    with Session() as session:
        try:
            location = session.query(Location).filter_by(name=location_name).first()
            if not location:
                raise NoSuchLocation(location_name)

            history_item = (
                session.query(WeatherItem)
                .filter_by(date=datetime.datetime.fromisoformat(date))
                .first()
            )
            if not history_item:
                raise NoData(location_name, date)

            return history_item.temperature
        finally:
            session.commit()
