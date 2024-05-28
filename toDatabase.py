import json
import logging
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

logging.basicConfig(
    filename="log_file.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

Base = declarative_base()


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    weather = relationship("Weather", back_populates="city")

    def __repr__(self):
        return f"<City(id={self.id}, name={self.name})>"


class Weather(Base):
    __tablename__ = "weather"

    city_id = Column(Integer, ForeignKey("city.id"), primary_key=True)
    date = Column(String, primary_key=True)
    temperature = Column(String)

    city = relationship("City", back_populates="weather")

    def __repr__(self):
        return f"<Weather(city_id={self.city_id}, date={self.date}, temperature={self.temperature})>"


engine = create_engine("sqlite:///weather.db")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

logging.info("Загрузка данных из файла JSON...")

with open("4.json", "r") as file:
    data = json.load(file)

logging.info("Обработка данных и добавление в базу данных...")

for item in data:
    for city_name, weather_data in item.items():
        city = session.query(City).filter_by(name=city_name).first()
        if city is None:
            city = City(name=city_name)
            session.add(city)
            session.commit()

        for date_str, temperature_str in weather_data.items():
            date = date_str
            temperature = temperature_str
            existing_weather = (
                session.query(Weather).filter_by(city_id=city.id, date=date).first()
            )
            if existing_weather is None:
                weather = Weather(city_id=city.id, date=date, temperature=temperature)
                session.add(weather)
session.commit()

logging.info("Добавление данных в базу данных завершено.")

session.close()
