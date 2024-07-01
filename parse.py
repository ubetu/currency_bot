import requests
from typing import List
from bs4 import BeautifulSoup
from datetime import date



class Parse:
    """Всё, что нужно для парсинга ЦБ"""


    __url = 'https://www.cbr.ru/currency_base/daily/'
    __headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }


    @classmethod
    def __get_html_of_CB(cls) -> None:
        """Получение и сохранение html страницы ЦБ"""

        req = requests.get(cls.__url, headers=cls.__headers)
        srs = req.text

        with open(f'/home/a0999441/domains/parcingcbscript.ru/public_html/data/sites/{date.today()}.html', 'w') as f:
            f.write(srs)

    @classmethod
    def get_currency_table(cls) -> List[List]:
        """Создание python таблицы с названием валют и их курсом, """
        cls.__get_html_of_CB()
        with open(f'/home/a0999441/domains/parcingcbscript.ru/public_html/data/sites/{date.today()}.html') as f:
            src = f.read()
        soup = BeautifulSoup(src, 'lxml')

        table_soup = soup.find( class_="table-wrapper").find(class_="table").find('tbody').find_all('tr')
        table_python = []

        for line in table_soup[1:]:
            elements = line.find_all('td')

            currency_name: str = elements[3].text
            currency_quantity = int(elements[2].text)
            currency_cost = float(elements[4].text.replace(',', '.'))

            table_python.append([currency_name, currency_cost/currency_quantity])

        return table_python
