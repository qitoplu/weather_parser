import logging
import json

logging.basicConfig(
    filename="log_file.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def modify_cities(input_filename, output_filename):
    try:
        with open(input_filename, "r", encoding="utf-8") as file:
            cities = json.load(file)

        modified_cities = []
        for city in cities:
            key = next(iter(city))
            n_key = key[8:]
            city[n_key] = city.pop(key)
            modified_cities.append(city)

        with open(output_filename, "w", encoding="utf-8") as file:
            json.dump(modified_cities, file, ensure_ascii=False, indent=4)

        logging.info(
            f"Модификация данных о городах в файле {input_filename} завершена успешно."
        )

    except Exception as e:
        logging.error(
            f"Произошла ошибка во время модификации данных о городах: {str(e)}"
        )


def process_weather_data(input_filename, output_filename):
    try:
        with open(input_filename, "r", encoding="utf-8") as file:
            cities_data = json.load(file)

        modified_cities_data = []
        for city_data in cities_data:
            modified_city_data = {}
            for city_name, weather_data in city_data.items():
                modified_weather_data = {}
                for time, temperature in weather_data.items():
                    date_string = f"2024-05-{int(time):02d}"
                    modified_weather_data[date_string] = temperature
                modified_city_data[city_name[:-1]] = modified_weather_data
            modified_cities_data.append(modified_city_data)

        with open(output_filename, "w", encoding="utf-8") as file:
            json.dump(modified_cities_data, file, ensure_ascii=False, indent=4)

        logging.info(
            f"Обработка данных о погоде в файле {input_filename} завершена успешно."
        )

    except Exception as e:
        logging.error(f"Произошла ошибка во время обработки данных о погоде: {str(e)}")


modify_cities("2.json", "3.json")
process_weather_data("3.json", "5.json")
