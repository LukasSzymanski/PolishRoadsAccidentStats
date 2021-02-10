import requests
import typing

from bs4 import BeautifulSoup


class ScrapeData:
    """Scrape web data class
    ----------------------
    Attributes:
    _______________________
    Methods:
        """

    def __init__(self):
        self._www = 'https://policja.pl/pol/form/1,Informacja-dzienna.html'
        self._table_class = 'table.table-listing:nth-child(2)'

    def connection(self, page=0) -> requests.models.Response:
        """Create connection to specific webpage"""
        www = self._www + f'?page={page}'
        res = requests.get(www)
        return res

    @staticmethod
    def get_soup(res: requests.models.Response) -> BeautifulSoup:
        soup = BeautifulSoup(res.text, 'lxml')
        return soup

    def get_data(self, soup: BeautifulSoup) -> list:
        """Get the proper data and divide it to list of days"""
        data = soup.find("table", {"class": self._table_class}).find_all('td')
        data = [item.text for item in data]
        final = [data[i:i + 8] for i in range(0, len(data), 8)]
        return final
