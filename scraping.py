import requests

from bs4 import BeautifulSoup
from time import sleep

HEADERS = ['Data statystyki', 'Zatrzymani nietrzeźwi kierujący', 'Wypadki drogowe', 'Zabici w wypadkach',
           'Ranni w wypadkach']


class ScrapeData:
    """Scrape web data class
    ----------------------
    Attributes:
        last_date - the date of last record
    _______________________
    Methods:
        """

    def __init__(self, last_date='2020-12-31'):
        self._www = 'https://policja.pl/pol/form/1,Informacja-dzienna.html'
        self._table_class = 'table-listing table-striped margin_b20'
        self.last_date = last_date

    def connection(self, page=0) -> requests.models.Response:
        """Create connection to specific webpage"""
        www = self._www + f'?page={page}'
        res = requests.get(www)
        return res

    @staticmethod
    def get_soup(res: requests.models.Response) -> BeautifulSoup:
        """Create BS4 soup with lxml parsing"""
        soup = BeautifulSoup(res.text, 'lxml')
        return soup

    def get_data(self, soup: BeautifulSoup) -> list:
        """Get the proper data and divide it to list of days"""
        data = soup.find("table", {"class": self._table_class}).find_all('td', {'data-label': HEADERS})
        data = [item.text for item in data]
        data = [data[i:i + 5] for i in range(0, len(data), 5)]
        return data

    def collect_data(self) -> list:
        """Collect daily reports from the last date to the newest available date"""
        collected_data = []
        page = 0
        while True:
            res = self.connection(page)
            data = self.get_data(self.get_soup(res))
            days = [row[0] for row in data]
            print(f'Subpage {page + 1} opened, data loaded')
            if self.last_date in days:
                collected_data.extend(data[:days.index(self.last_date)])
                print('End of loading data process.')
                break
            page += 1
            sleep(0.5)
            collected_data.extend(data)
        collected_data.reverse()
        return collected_data
