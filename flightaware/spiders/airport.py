import warnings
import scrapy

from bs4 import BeautifulSoup
from scrapy.http import Response
from ..items import FlightawareItem, WeatherItem


class KjfkSpider(scrapy.Spider):
    name = 'airport'
    airport = None
    allowed_domains = ['zh.flightaware.com', 'flightaware.com']

    def __init__(self, airport='KJFK', *args, **kwargs):
        super(KjfkSpider, self).__init__(*args, **kwargs)
        self.airport = airport
        self.start_urls = [
            f'https://zh.flightaware.com/resources/airport/{airport}/weather']  # 首先爬取机场天气信息
        self.arrive_url = f'https://zh.flightaware.com/live/airport/{airport}/arrivals?;offset=0;order=actualarrivaltime;sort=DESC'
        self.departure_url = f'https://zh.flightaware.com/live/airport/{airport}/departures?;offset=0;order=actualdeparturetime;sort=DESC'
        self.enroute_url = f'https://zh.flightaware.com/live/airport/{airport}/enroute?;offset=0;order=estimatedarrivaltime;sort=ASC'
        self.scheduled_url = f'https://zh.flightaware.com/live/airport/{airport}/scheduled?;offset=0;order=filed_departuretime;sort=ASC'

    def parse(self, response: Response):
        try:
            # 使用beautifulsoup解析
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find(
                class_='prettyTable fullWidth tablesaw tablesaw-stack')  # 定位到表格
            weather = WeatherItem()
            for child in table.contents[2:]:
                weather['data_type'] = 'weather'
                weather['date'] = child.contents[0].text
                weather['time'] = child.contents[1].text
                weather['flight_rules'] = child.contents[2].text
                weather['wind_dir'] = child.contents[3].text
                weather['wind_speed'] = child.contents[4].text
                weather['type'] = child.contents[5].text
                weather['high_agl'] = child.contents[6].text
                weather['visibility'] = child.contents[7].text
                weather['remarks'] = child.contents[8].text
                yield weather
        except:
            self.logger.error('Parse error called on %s', response.url)
        finally:
            # 到达航班
            yield scrapy.Request(url=self.arrive_url, callback=self.arrive)
            # 出发航班
            yield scrapy.Request(url=self.departure_url, callback=self.departure)
            # 计划前往航班
            yield scrapy.Request(url=self.enroute_url, callback=self.enroute)
            # 计划出发航班
            yield scrapy.Request(url=self.scheduled_url, callback=self.scheduled)

    def arrive(self, response: Response):
        soup = BeautifulSoup(response.text, 'html.parser')  # 使用beautifulsoup解析
        try:
            table = soup.find(class_='prettyTable fullWidth')  # 定位到表格
            for child in table.contents[1:]:  # 循环添加航班
                flight = FlightawareItem()
                flight['data_type'] = 'arrive'
                if child.contents[0].span != None:
                    flight['airline'] = child.contents[0].span['title']
                flight['ident'] = child.contents[0].span.a.text
                if child.contents[1].span != None:
                    flight['type'] = child.contents[1].span['title']
                if child.contents[2].span != None:
                    flight['origin'] = child.contents[2].span['title']
                flight['departure_time'] = child.contents[3].text.replace(
                    '\xa0', ',')
                flight['arrive_time'] = child.contents[4].text.replace(
                    '\xa0', ',')
                yield flight
        except:
            self.logger.error('Parse error called on %s',
                              response.url)  # 出现错错误则使用日志提示
        finally:
            next_page = soup.find(text='后20条')
            if next_page != None:  # 如果有下一页则继续爬取
                next_url = next_page.parent['href']
                yield scrapy.Request(url=next_url, callback=self.arrive)

    def departure(self, response: Response):
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            table = soup.find(class_='prettyTable fullWidth')
            for child in table.contents[1:]:
                flight = FlightawareItem()
                flight['data_type'] = 'departure'
                if child.contents[0].span != None:
                    flight['airline'] = child.contents[0].span['title']
                flight['ident'] = child.contents[0].span.a.text
                if child.contents[1].span != None:
                    flight['type'] = child.contents[1].span['title']
                if child.contents[2].span != None:
                    flight['destination'] = child.contents[2].span['title']
                flight['departure_time'] = child.contents[3].text.replace(
                    '\xa0', ',')
                flight['arrive_time'] = child.contents[4].text.replace(
                    '\xa0', ',')
                yield flight
        except:
            self.logger.error('Parse error called on %s', response.url)
        finally:
            next_page = soup.find(text='后20条')
            if next_page != None:
                next_url = next_page.parent['href']
                yield scrapy.Request(url=next_url, callback=self.departure)

    def enroute(self, response: Response):
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            table = soup.find(class_='prettyTable fullWidth')
            for child in table.contents[1:]:
                flight = FlightawareItem()
                flight['data_type'] = 'enroute'
                if child.contents[0].span != None:
                    flight['airline'] = child.contents[0].span['title']
                flight['ident'] = child.contents[0].span.a.text
                if child.contents[1].span != None:
                    flight['type'] = child.contents[1].span['title']
                if child.contents[2].span != None:
                    flight['origin'] = child.contents[2].span['title']
                flight['departure_time'] = child.contents[3].text.replace(
                    '\xa0', ',')
                flight['arrive_time'] = child.contents[4].text.replace(
                    '\xa0', ',')
                yield flight
        except:
            self.logger.error('Parse error called on %s', response.url)
        finally:
            next_page = soup.find(text='后20条')
            if next_page != None:
                next_url = next_page.parent['href']
                yield scrapy.Request(url=next_url, callback=self.enroute)

    def scheduled(self, response: Response):
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            table = soup.find(class_='prettyTable fullWidth')
            for child in table.contents[1:]:
                flight = FlightawareItem()
                flight['data_type'] = 'scheduled'
                if child.contents[0].span != None:
                    flight['airline'] = child.contents[0].span['title']
                flight['ident'] = child.contents[0].span.a.text
                if child.contents[1].span != None:
                    flight['type'] = child.contents[1].span['title']
                if child.contents[2].span != None:
                    flight['destination'] = child.contents[2].span['title']
                flight['departure_time'] = child.contents[3].text.replace(
                    '\xa0', ',')
                flight['arrive_time'] = child.contents[4].text.replace(
                    '\xa0', ',')
                yield flight
        except:
            self.logger.error('Parse error called on %s', response.url)
        finally:
            next_page = soup.find(text='后20条')
            if next_page != None:
                next_url = next_page.parent['href']
                yield scrapy.Request(url=next_url, callback=self.scheduled)
