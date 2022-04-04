import csv
import logging
from urllib.request import urlopen

from bs4 import BeautifulSoup

from constants import BatCols, BowlCols, FieldCols, abbrev_lookup, safe_modes
from utils import extract_fielder_name, extract_name, safe_float, safe_int


class Match:

    def __init__(self, series_id, match_id):
        self.base_url = 'https://www.espncricinfo.com/series'
        self.series_id = series_id
        self.match_id = match_id
        self.match_url = f'{self.base_url}/{series_id}/scorecard/{match_id}'
        self.soup = self.get_soup()
        self.content = self.get_content()
        self.players = {}
        self.innings = 0
        if self.content:
            self.teams = self.get_teams()
            self.squads = self.get_squads()
            if self.teams:
                self.scrape_page()
                assert len(self.players.keys()) >= 11
        else:
            logging.info(f'{self.series_id}, {self.match_id}: no content')

    def get_soup(self):
        page = urlopen(self.match_url)
        return BeautifulSoup(page, 'html.parser')

    def get_content(self):
        class_name = 'ReactCollapse--collapse'
        return self.soup.find_all(class_=class_name, recursive=True)

    def save_html(self):
        with open(f'data/{self.match_id}.html', 'w') as file:
            file.write(str(self.soup))

    def get_teams(self):
        teams = []
        text = 'ds-text-tight-s ds-font-bold ds-uppercase'
        containers = self.soup.find_all('span', class_=text)
        if not containers:
            return teams
        for container in containers:
            if not container:
                continue
            team_text = container.text.split('INNINGS')[0].strip().title()
            teams.append(team_text)
        return teams

    def get_squads(self):
        squads = [[], []]
        with open('squads.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['team'] == self.teams[0]:
                    squads[0].append(row['name'])
                elif row['team'] == self.teams[1]:
                    squads[1].append(row['name'])
                else:
                    continue
        return squads

    def scrape_page(self):
        self.extract_batting_stats()
        self.extract_bowling_stats()
        self.extract_fielding_stats()
        self.extract_player_of_the_match()

    def extract_batting_stats(self):
        for i in range(2):
            self.innings = i
            text = 'ds-w-full ds-table ds-table-xs ds-table-fixed ci-scorecard-table'
            table = self.content[i].find(class_=text)
            if not table:
                continue
            rows = table.find_all('tr')
            for row in rows:
                try:
                    cols = row.find_all('td')
                    cols = [x.text.strip() for x in cols]
                    name = extract_name(cols[0])
                    if name.startswith('Did not bat') or name.startswith('Yet to bat'):
                        self.extract_did_not_bat(name)

                    bat_dict = {
                        BatCols.DISMISSAL.get_name(): cols[1],
                        BatCols.RUNS_SCORED.get_name(): safe_int(cols[2]),
                        BatCols.BALLS_FACED.get_name(): safe_int(cols[3]),
                        BatCols.FOURS_SCORED.get_name(): safe_int(cols[5]),
                        BatCols.SIXES_SCORED.get_name(): safe_int(cols[6]),
                        BatCols.STRIKE_RATE.get_name(): safe_float(cols[7]),
                        BatCols.NOT_OUT.get_name(): (cols[1].lower() in safe_modes) * 1
                    }

                    if not self.players.get(name):
                        self.players[name] = {
                            'name': name,
                            'team': self.teams[i],
                            'abbrev': abbrev_lookup[self.teams[i]]
                        }

                    self.players[name].update(bat_dict)
                except IndexError:
                    continue

    def extract_bowling_stats(self):
        for i in range(2):
            self.innings = i
            text = 'ds-w-full ds-table ds-table-xs ds-table-fixed'
            table = self.content[i].find(class_=text)
            if not table:
                continue
            rows = table.find_all('tr')

            for row in rows:
                try:
                    cols = row.find_all('td')
                    cols = [x.text.strip() for x in cols]
                    name = extract_name(cols[0])

                    bowl_dict = {
                        BowlCols.OVERS.get_name(): safe_float(cols[1]),
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
                        self.players[name] = {
                            'name': name,
                            'team': self.teams[not i],
                            'abbrev': abbrev_lookup[self.teams[not i]],
                        }

                    self.players[name].update(bowl_dict)

                except IndexError:
                    continue

    def extract_did_not_bat(self, dnb_string):
        players = [p.strip() for p in dnb_string.split(':')[1].split(',')]
        for name in players:
            self.players[name] = {
                'name': name,
                'team': self.teams[self.innings],
                'abbrev': abbrev_lookup[self.teams[self.innings]]
            }

    def name_to_player(self, fielder):
        for name in self.squads[not self.innings]:
            if fielder == name:
                return name
            else:
                parts = fielder.split(' ')
                name_parts = name.split(' ')
                num_parts = len(parts)
                if num_parts == 1:
                    if fielder in name_parts:
                        return name
                elif num_parts == 2:
                    if parts[1] in name_parts:
                        if name[0] == fielder[0] or fielder[0] == fielder[0].lower():
                            return name
                        if parts[0] in name_parts:
                            return name
                elif num_parts == 3:
                    if parts[2] in name_parts:
                        if name[0] == fielder[0] or fielder[0] == fielder[0].lower():
                            return name
        return None

    def update_fielding(self, fielder_name):
        player_name = self.name_to_player(fielder_name)
        try:
            player = self.players[player_name]
        except KeyError:
            if player_name not in self.squads[not self.innings]:
                logging.error(f'Fielder does not exist: {fielder_name}')
                return
            else:
                player = {
                    'name': player_name,
                    'team': self.teams[not self.innings],
                    'abbrev': abbrev_lookup[self.teams[not self.innings]]
                }
                self.players[player_name] = player
                logging.info(f'Sub/Live fielder added {player_name}')
        if not player.get('fielding'):
            player['fielding'] = 1
        else:
            player['fielding'] += 1

    @staticmethod
    def extract_caught_or_stumped(dismissal):
        raw_fielder, raw_bowler = dismissal.split(' b ')
        if raw_fielder.startswith('c'):
            dismissal_type = 'c '
        elif raw_fielder.startswith('st '):
            dismissal_type = 'st '
        else:
            return None
        fielder = raw_fielder.split(dismissal_type)[1]
        if fielder == '&':
            return extract_name(raw_bowler)
        else:
            return extract_fielder_name(fielder)

    @staticmethod
    def extract_run_out(dismissal):
        if dismissal.startswith('run out'):
            fielders = extract_fielder_name(dismissal.split('run out')[1])
            return fielders.split('/')[0]

    def extract_fielding_stats(self):
        player_items = list(self.players.items()).copy()
        for name, player_info in player_items:
            self.innings = self.teams.index(player_info['team'])
            fielder_name = ''
            dismissal = player_info.get(BatCols.DISMISSAL.get_name())
            try:
                _, _ = dismissal.split(' b ')
                fielder_name = self.extract_caught_or_stumped(dismissal)
            except IndexError:
                fielder_name = self.extract_caught_or_stumped(dismissal)
            except ValueError:
                fielder_name = self.extract_run_out(dismissal)
            except AttributeError:
                continue
            finally:
                if fielder_name:
                    self.update_fielding(fielder_name)

    def extract_player_of_the_match(self):
        try:
            class_name = 'ci-match-player-award-carousel'
            potm_container = self.soup.find(class_=class_name, recursive=True)
            potm = potm_container.find_all('span')[0].text.split(',')[0].strip()
            self.players[potm]['potm'] = 1
            logging.info(f'Player of the match: {potm}')
        except AttributeError:
            logging.info('No potm found')
        except KeyError:
            logging.error(f'Potm does not exist: {potm}')

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
        general_cols = ['name', 'team', 'abbrev']
        bat_cols = [col.get_name() for col in BatCols]
        bowl_cols = [col.get_name() for col in BowlCols]
        field_cols = [col.get_name() for col in FieldCols]
        header = general_cols + bat_cols + bowl_cols + field_cols
        with open(f'data/{self.match_id}.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            for i in self.players:
                writer.writerow(self.players[i])
