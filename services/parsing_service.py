import re
from bs4 import BeautifulSoup
import requests


class ParsingService:
    @staticmethod
    async def parseUrl(url, ignore_row=None):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', attrs={'class': 'table'})
        rows = table.find_all('tr')

        sum = 0
        data = []

        for row in rows:
            cols = row.find_all('td')

            if not cols:
                continue

            cols = [element.text.strip() for element in cols]

            country = cols[0]
            aac = cols[3]

            aac = to_number(aac)
            country = re.findall(r'[A-Za-z ]+', country)[0].strip()

            if aac == '' or country.startswith('US'):
                continue

            if ignore_row and country.startswith(ignore_row):
                continue

            sum += aac

            data.append({
                'country': country,
                'aac': aac
            })

        new_data = []
        other_sum = 0

        print(f'sum is {sum}')

        for i in range(len(data)):
            print(f'{data[i]['country']} - {data[i]['aac'] / sum}')

            if data[i]['aac'] / sum < 0.03:
                other_sum += data[i]['aac']
            else:
                new_data.append(data[i])

        new_data.append({'country': 'other', 'aac': other_sum})

        data = sorted(new_data, key=lambda k: k['aac'])

        return data


def to_number(s):
    try:
        s = s.replace(',', '')
        return float(s)
    except ValueError:
        return ''
