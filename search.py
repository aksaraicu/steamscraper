import os
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

search_term = input('Enter game name: ')
url = 'https://store.steampowered.com/search/?term=' + search_term


def get_data(url):
    r = requests.get(url)
    return r.text

# processing data
def parse(data):
    result = []
    soup = BeautifulSoup(data, 'html.parser')
    contents = soup.find('div', attrs={'id': 'search_resultsRows'})
    games = contents.find_all('a')

    for game in games:
        link = game['href']

    # parsing data
        title = game.find('span', {'class': 'title'}).text.strip().split('£')[
            0].replace('\u2013', '-')
        price = game.find('div', {'class': 'search_price'}
                          ).text.strip().split('£')[0]
        released = game.find(
            'div', {'class': 'search_released'}).text.strip().split('£')[0]

        if title == '':
            title = 'Not Found'
        if price == '':
            price = 'Not Found'
        if released == '':
            released = 'Not Found'

        # sorting data
        data_dict = {
            'title': title,
            'price': price,
            'link': link,
            'released': released
        }
        # append
        result.append(data_dict)
    return result
#  proceess cleaned data from parser


def output(datas: list):
    for i in datas:
        print(i)


if __name__ == '__main__':
    data = get_data(url)
    final_data = parse(data)
    output(final_data)

# create folder for output
    directory = 'output/' + search_term
    if not os.path.exists(directory):
        os.mkdir(directory)

# write to json
    with open('output/' + search_term + '/' + search_term + '.json', 'w') as f:
        json.dump(final_data, f, indent=4)

# write to csv
    df = pd.DataFrame(final_data)
    df.to_csv('output/' + search_term + '/' + search_term + '.csv', index=False)
