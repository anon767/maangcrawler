import requests
from bs4 import BeautifulSoup

from .Crawler import Crawler


class Webcrawler(Crawler):
    def __init__(self, url: str):
        self.website = requests.get(url)
        self.results = BeautifulSoup(self.website.content, 'html.parser')
