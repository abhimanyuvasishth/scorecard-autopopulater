import csv
import json
import os
import time
from collections import defaultdict
from http.client import IncompleteRead
from urllib.error import HTTPError
from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup
from dateutil import parser

from scorecard_autopopulater.constants import full_name_lookup, pure_date


class Impact:

    def __init__(self):
        self.players = defaultdict(dict)
        self.all_dates = []

    def generate_impact_table(self):
        path = 'data/raw/past_match_impacts'
        for i, file_name in enumerate(sorted(os.listdir(path))):
            if i % 50 == 0 and i > 0:
                print(i)
            if file_name.endswith('html'):
                with open(f'{path}/{file_name}', 'r') as html_file:
                    page = html_file.read()

                soup = BeautifulSoup(page, 'html.parser')
                date = self.find_date(soup)
                self.all_dates.append(date)
                content = self.get_content(soup)
                self.append_player_impact(content, date)

        for date in self.all_dates:
            for player in self.players:
                if not self.players[player].get(date):
                    self.players[player][date] = 0.0

        df = pd.DataFrame.from_dict(self.players).T
        unsorted_date_columns = df.loc[:, ((df.columns != 'country') & (df.columns != 'image_url'))]
        date_columns = sorted(unsorted_date_columns.columns.values)
        path = 'data/raw/output'
        df[sorted(df.columns)].to_csv(f'{path}/raw_table.csv')
        df.loc[:, date_columns] = df.loc[:, date_columns].cumsum(axis=1)
        df[sorted(df.columns)].to_csv(f'{path}/cumulative_table.csv')

    @staticmethod
    def save_all_impact_reports():
        path = 'data/raw/past_schedules'
        for file_name in sorted(os.listdir(path)):
            if file_name.endswith('csv'):
                year = file_name.split('_')[1].split('.')[0]
                print(year)
                with open(f'{path}/{file_name}', 'r') as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        name = f'data/raw/past_match_impacts/{year}_{row["match_num"]}.html'
                        if os.path.exists(name):
                            continue
                        soup = Impact.get_soup(row['url'])
                        if soup:
                            Impact.save_html(soup, name)
                        time.sleep(1)

    @staticmethod
    def get_soup(url):
        try:
            page = urlopen(url)
            return BeautifulSoup(page, 'html.parser')
        except (HTTPError, IncompleteRead) as e:
            print(url, e)
            return None

    @staticmethod
    def get_content(soup):
        class_name = 'ds-border-b ds-border-line'
        return soup.find_all('tr', class_=class_name)

    @staticmethod
    def save_html(soup, file_name):
        with open(file_name, 'w') as file:
            file.write(str(soup))

    @staticmethod
    def find_date(soup):
        class_name = 'ds-px-4 ds-py-3 ds-border-b ds-border-line'
        match_date = ''.join(soup.find(class_=class_name).text.split(',')[2:4]).strip()
        if match_date == 'May 27 - 28 2014':
            match_date = 'May 27 2014'

        parsed_date = parser.parse(match_date)

        if parsed_date.year > 2022:
            breakpoint()

        return parsed_date.strftime(pure_date)

    @staticmethod
    def get_or_create_player(url):
        file_name = url.split('/')[2]
        file_path = f'data/raw/players/{file_name}.html'
        if os.path.exists(file_path):
            with open(file_path, 'r') as html_file:
                return BeautifulSoup(html_file.read(), 'html.parser')

        full_url = f'https://www.espncricinfo.com/{url}'
        soup = Impact.get_soup(full_url)
        Impact.save_html(soup, file_path)
        return soup

    @staticmethod
    def get_player_data(player_url):
        soup = Impact.get_or_create_player(player_url)
        try:
            script = json.loads(soup.find('script', id="__NEXT_DATA__").text)
            player = script['props']['appPageProps']['data']['player']
            image_path = player.get('headshotImage') or player.get('image')
            image_url = f"https://www.espncricinfo.com{image_path['url']}"
        except (KeyError, TypeError):
            image_url = ''
        return {
            'country': soup.find(class_='ds-bg-raw-black/85').find('span').text,
            'image_url': image_url,
        }

    def append_player_impact(self, content, date):
        for row in content:
            try:
                data = row.find_all('td')
                name = data[0].text
                player_url = data[0].find('a')['href']

                team = data[1].text
                _ = full_name_lookup[team]

                impact = float(data[2].text.replace(' ', ''))

                if not self.players[name].get('country'):
                    player_data = self.get_player_data(player_url)
                    self.players[name]['country'] = player_data['country']
                    self.players[name]['image_url'] = player_data['image_url']

                self.players[name][date] = impact
            except (IndexError, KeyError, TypeError, ValueError):
                continue


if __name__ == '__main__':
    # Impact().save_all_impact_reports()
    Impact().generate_impact_table()
