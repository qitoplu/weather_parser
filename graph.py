import json
import matplotlib.pyplot as plt

with open("5.json", "r", encoding="utf-8") as file:
    cities_data = json.load(file)


def is_monotonic(temperatures):
    return all(
        temperatures[i] <= temperatures[i + 1] for i in range(len(temperatures) - 1)
    ) or all(
        temperatures[i] >= temperatures[i + 1] for i in range(len(temperatures) - 1)
    )


monotonic_cities = []
for city_data in cities_data:
    for city_name, weather_data in city_data.items():
        temperatures = []
        for temperature in weather_data.values():
            try:
                temperatures.append(int(temperature))
            except ValueError:
                print(f"Неверное значение температуры '{temperature}' для города {city_name}")
                break
        else:
            if is_monotonic(temperatures):
                monotonic_cities.append(city_name)
print("Cities with monotonically changing temperature throughout the week:")
for city in monotonic_cities:
    print(city)
cities_for_plotting = monotonic_cities[5:7]
for city_data in cities_data:
    for city_name, weather_data in city_data.items():
        if city_name in cities_for_plotting:
            dates = sorted(weather_data.keys())
            temperatures = []
            for date in dates:
                temperature = weather_data[date]
                try:
                    temperatures.append(int(temperature))
                except ValueError:
                    print(
                        f"Неверное значение температуры '{temperature}' для города {city_name}"
                    )
                    break

            plt.plot(dates, temperatures, label=city_name)

plt.xlabel("Дата")
plt.ylabel("Температура")
plt.title("Изменение температуры")
plt.xticks(rotation=45)
plt.legend()
plt.show()
