import scrapy
import logging

# logging.basicConfig(filename='/Users/ratibor/vscode/python/Programs/firstP/log_file.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(
    filename="log_file.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class MySpider(scrapy.Spider):
    name = "weatherParser"
    allowed_domains = ["weather.rambler.ru"]
    start_urls = ["https://weather.rambler.ru/world/rossiya"]

    def parse(self, response):
        try:
            next_pages = response.xpath(
                "//div[contains(@class, 'tRxV')]//div[contains(@class, 'AyDi')]/a/@href"
            ).getall()
            for next_page in next_pages:
                yield response.follow(next_page, callback=self.parse_city1)
        except Exception as e:
            logging.error(f"Произошла ошибка при парсинге: {str(e)}")

    def parse_city1(self, response):
        try:
            next_pages = response.xpath(
                "//div[contains(@class, 'yeW5')]//div[contains(@class, 'rui-Hint-icon buRY')]/a/@href"
            ).getall()
            for next_page in next_pages:
                yield response.follow(next_page, callback=self.parse_city)
        except Exception as e:
            logging.error(f"Произошла ошибка при парсинге страницы города 1: {str(e)}")

    def parse_city(self, response):
        try:
            city = (
                response.xpath("//div[contains(@class, 'rICO')]/h1/text()")
                .get()
                .strip()
            )
            day_nodes = response.xpath(
                "//div[contains(@class, 'Munt nFyo')]//span[@class='PADa']"
            )
            temperature_nodes = response.xpath(
                "//div[contains(@class, 'Munt gWee')]//span[@class='AY6t']"
            )
            if day_nodes and temperature_nodes:
                city_weather_data = {}
                for day_node, temperature_node in zip(day_nodes, temperature_nodes):
                    day = day_node.xpath(".//text()").get().strip()
                    temperature = temperature_node.xpath(".//text()").get().strip()
                    city_weather_data[day] = temperature
                yield {city: city_weather_data}
                logging.info(f'Парсинг страницы города "{city}" завершен успешно')
        except Exception as e:
            logging.error(f"Произошла ошибка при парсинге страницы города: {str(e)}")
