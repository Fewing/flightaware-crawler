import scrapy

from bs4 import BeautifulSoup
from scrapy.http import Response
from ..items import FlightawareItem


class KjfkSpider(scrapy.Spider):
    name = 'kjfk'
    allowed_domains = ['zh.flightaware.com','flightaware.com']
    start_urls = [
        'https://zh.flightaware.com/live/airport/KJFK/arrivals?;offset=0;order=actualarrivaltime;sort=DESC']
    
    arrive_url = 'https://zh.flightaware.com/live/airport/KJFK/arrivals?;offset=0;order=actualarrivaltime;sort=DESC'
    departure_url = 'https://zh.flightaware.com/live/airport/KJFK/departures?;offset=0;order=actualdeparturetime;sort=DESC'
    enroute_url = 'https://zh.flightaware.com/live/airport/KJFK/enroute?;offset=0;order=estimatedarrivaltime;sort=ASC'
    scheduled_url = 'https://zh.flightaware.com/live/airport/KJFK/scheduled?;offset=0;order=filed_departuretime;sort=ASC'

    def parse(self, response: Response):
            yield scrapy.Request(url=self.arrive_url, callback=self.arrive) #到达航班
            yield scrapy.Request(url=self.departure_url, callback=self.departure) #出发航班
            yield scrapy.Request(url=self.enroute_url, callback=self.enroute) #计划前往航班
            yield scrapy.Request(url=self.scheduled_url, callback=self.scheduled) #计划出发航班

    def arrive(self, response: Response):
        soup = BeautifulSoup(response.text, 'html.parser')  # 使用beautifulsoup解析
        table = soup.find(
            id='slideOutPanel').contents[1].contents[3].contents[1].contents[1].contents[2]  # 定位到表格
        for child in table.contents[1:]:
            flight = FlightawareItem()
            flight['data_type'] = 'arrive'
            flight['airline'] = child.contents[0].span['title']
            flight['ident'] = child.contents[0].span.a.text
            flight['type'] = child.contents[1].span['title']
            flight['origin'] = child.contents[2].span['title']
            flight['departure_time'] = child.contents[3].text.replace('\xa0', ',')
            flight['arrive_time'] = child.contents[4].text.replace('\xa0', ',')
            yield flight
        next_page = soup.find(text='后20条')
        if next_page != None:                      #如果有下一页则继续爬取
            next_url = next_page.parent['href']
            #yield scrapy.Request(url=next_url, callback=self.arrive) 
    
    def departure(self, response: Response):
        soup = BeautifulSoup(response.text, 'html.parser')  # 使用beautifulsoup解析
        table = soup.find(
            id='slideOutPanel').contents[1].contents[3].contents[1].contents[1].contents[2]  # 定位到表格
        for child in table.contents[1:]:
            flight = FlightawareItem()
            flight['data_type'] = 'departure'
            flight['airline'] = child.contents[0].span['title']
            flight['ident'] = child.contents[0].span.a.text
            flight['type'] = child.contents[1].span['title']
            flight['destination'] = child.contents[2].span['title']
            flight['departure_time'] = child.contents[3].text.replace('\xa0', ',')
            flight['arrive_time'] = child.contents[4].text.replace('\xa0', ',')
            yield flight
        next_page = soup.find(text='后20条')
        if next_page != None:
            next_url = next_page.parent['href']
            #yield scrapy.Request(url=next_url, callback=self.departure)

    def enroute(self, response: Response):
        soup = BeautifulSoup(response.text, 'html.parser')  # 使用beautifulsoup解析
        table = soup.find(
            id='slideOutPanel').contents[1].contents[3].contents[1].contents[1].contents[2]  # 定位到表格
        for child in table.contents[1:]:
            flight = FlightawareItem()
            flight['data_type'] = 'enroute'
            flight['airline'] = child.contents[0].span['title']
            flight['ident'] = child.contents[0].span.a.text
            flight['type'] = child.contents[1].span['title']
            flight['origin'] = child.contents[2].span['title']
            flight['departure_time'] = child.contents[3].text.replace('\xa0', ',')
            flight['arrive_time'] = child.contents[4].text.replace('\xa0', ',')
            yield flight
        next_page = soup.find(text='后20条')
        if next_page != None:
            next_url = next_page.parent['href']
            #yield scrapy.Request(url=next_url, callback=self.enroute)

    def scheduled(self, response: Response):
        soup = BeautifulSoup(response.text, 'html.parser')  # 使用beautifulsoup解析
        table = soup.find(
            id='slideOutPanel').contents[1].contents[3].contents[1].contents[1].contents[2]  # 定位到表格
        for child in table.contents[1:]:
            flight = FlightawareItem()
            flight['data_type'] = 'scheduled'
            flight['airline'] = child.contents[0].span['title']
            flight['ident'] = child.contents[0].span.a.text
            flight['type'] = child.contents[1].span['title']
            flight['destination'] = child.contents[2].span['title']
            flight['departure_time'] = child.contents[3].text.replace('\xa0', ',')
            flight['arrive_time'] = child.contents[4].text.replace('\xa0', ',')
            yield flight
        next_page = soup.find(text='后20条')
        if next_page != None:
            next_url = next_page.parent['href']
            #yield scrapy.Request(url=next_url, callback=self.scheduled)