import json
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np

from constants import BatCols, BowlCols
from utils import safe_int, safe_float

class Match:

    def __init__(self, match_id):
        self.base_url = 'https://www.espncricinfo.com/matches/engine/match'
        self.match_id = match_id
        self.match_url = f'{self.base_url}/{match_id}.html'
        self.soup = self.get_soup()
        self.content = self.get_content()
        self.players = {}

    def get_soup(self):
        page = urlopen(self.match_url)
        return BeautifulSoup(page, 'html.parser')

    def get_content(self):
        class_name = 'Collapsible__contentInner'
        return self.soup.find_all(class_=class_name, recursive=True)

    @staticmethod
    def extract_fielder_name(name):
        new_name = name.replace('sub','').replace(r'\(.*\)','')
        return Match.extract_name(new_name)

    @staticmethod
    def extract_name(name):
        new_name = name.replace(u'\xa0',' ').replace('†', '').replace('(c)', '')
        return new_name.strip()

    def scrape_page(self):
        self.extract_batting_stats()
        self.extract_bowling_stats()
        self.extract_fielding_stats()

    def extract_batting_stats(self):
        for i in range(2):
            table = self.content[i].find(class_='table batsman')
            rows = table.find_all('tr')
            for row in rows:
                try:
                    cols = row.find_all('td')
                    cols = [x.text.strip() for x in cols]
                    name = self.extract_name(cols[0])
                    if name.startswith('Did not bat'):
                        self.extract_did_not_bat(name)

                    bat_dict = {
                        BatCols.DISMISSAL.get_name(): cols[1],
                        BatCols.RUNS_SCORED.get_name(): safe_int(cols[2]),
                        BatCols.BALLS_FACED.get_name(): safe_int(cols[3]),
                        BatCols.FOURS_SCORED.get_name(): safe_int(cols[5]),
                        BatCols.SIXES_SCORED.get_name(): safe_int(cols[6]),
                        BatCols.STRIKE_RATE.get_name(): safe_float(cols[7]),
                        BatCols.NOT_OUT.get_name(): (cols[1] == 'not out') * 1
                    }

                    if not self.players.get(name):
                        self.players[name] = {'name': name}

                    self.players[name].update(bat_dict)
                except IndexError as e:
                    continue

    def extract_bowling_stats(self):
        for i in range(2):
            table = self.content[i].find(class_='table bowler')
            rows = table.find_all('tr')

            for row in rows:
                try:
                    cols = row.find_all('td')
                    cols = [x.text.strip() for x in cols]
                    name = self.extract_name(cols[0])

                    bowl_dict = {
                        BowlCols.OVERS.get_name(): safe_int(cols[1]),
                        BowlCols.MAIDENS.get_name(): safe_int(cols[2]),
                        BowlCols.RUNS_CONCEDED.get_name(): safe_int(cols[3]),
                        BowlCols.WICKETS.get_name(): safe_int(cols[4]),
                        BowlCols.ECONOMY_RATE.get_name(): safe_float(cols[5]),
                        BowlCols.DOTS_BOWLED.get_name(): safe_int(cols[6]),
                        BowlCols.FOURS_CONCEDED.get_name(): safe_int(cols[7]),
                        BowlCols.SIXES_CONCEDED.get_name(): safe_int(cols[8]),
                        BowlCols.WIDES.get_name(): safe_int(cols[9]),
                        BowlCols.NO_BALLS.get_name(): safe_int(cols[10]),
                    }

                    if not self.players.get(name):
                        self.players[name] = {'name': name}

                    self.players[name].update(bowl_dict)

                except IndexError as e:
                    continue

    def extract_did_not_bat(self, dnb_string):
        players = [p.strip() for p in dnb_string.split(':')[1].split(',')]
        for name in players:
            self.players[name] = {'name': name}

    def name_to_player(self, fielder):
        for name in self.players.keys():
            if fielder == name:
                return name
            else:
                parts = fielder.split(' ')
                num_parts = len(parts)
                if num_parts == 1:
                    if fielder in name.split(' '):
                        return name
                elif num_parts == 2:
                    if parts[1] in name.split(' ') and name[0] == fielder[0]:
                        return name
        return None

    def extract_fielding_stats(self):
        for name, player_info in self.players.items():
            dismissal = player_info.get(BatCols.DISMISSAL.get_name())
            try:
                raw_fielder, raw_bowler = dismissal.split(' b ')
                fielder = raw_fielder.split('c ')[1]
                if fielder == '&':
                    fielder = self.extract_name(raw_bowler)
                else:
                    fielder = self.extract_fielder_name(fielder)
                print('catch', name, fielder, self.name_to_player(fielder))
            except IndexError:
                # print('stumping', name, dismissal)
                continue
            except ValueError:
                # print('other dismissal', name, dismissal)
                continue
            except AttributeError:
                # print('no dismissal', name)
                continue

    def get_player_info(self, player_name):
        player = self.players[player_name]
        return [
            player.get('runs_scored', 0),
            player.get('balls_faced', 0),
            player.get('strike_rate', 0.0),
            player.get('not_out', 0),
            player.get('overs', 0),
            player.get('economy_rate', 0),
            player.get('wickets', 0),
            player.get('maidens', 0),
            player.get('hattricks', 0),
            player.get('fielding', 0),
        ]

    def convert_to_csv(self):
        header = ['name'] + [a.get_name() for a in BatCols] + [a.get_name() for a in BowlCols]
        with open(f'data/{self.match_id}.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            for i in self.players:
                writer.writerow(self.players[i])
