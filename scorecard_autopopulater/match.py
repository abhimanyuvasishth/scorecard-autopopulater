from urllib.request import urlopen

from bs4 import BeautifulSoup

from scorecard_autopopulater.dismissal import Dismissal
from scorecard_autopopulater.stat_items import StatItems, batting_row, bowling_row
from scorecard_autopopulater.team import Team
from scorecard_autopopulater.utils import extract_name


class Match:
    def __init__(self, url):
        self.url = url
        self.match_id = self.url.split('/')[-2].split('-')[-1]
        self.soup = self._generate_soup()
        self.content = self._generate_content()
        self.teams = self._generate_teams()

    def _generate_soup(self):
        page = urlopen(self.url)
        return BeautifulSoup(page, 'html.parser')

    def _generate_content(self):
        class_name = 'ReactCollapse--collapse'
        return self.soup.find_all(class_=class_name, recursive=True)

    def _generate_teams(self):
        team_names = []
        text = 'ds-text-tight-s ds-font-bold ds-uppercase'
        containers = self.soup.find_all('span', class_=text)

        div = 'ds-text-tight-s ds-font-bold ds-uppercase ds-p-4 ds-pb-2 ds-border-b ds-border-line'
        if len(containers) == 1:
            containers += self.soup.find_all(class_=div)

        if not containers:
            return team_names

        for container in containers:
            if not container:
                continue
            team_text = container.text.split('INNINGS')[0].split('Team')[0].strip().title()
            team_names.append(team_text)

        teams = [Team(team_name, innings) for innings, team_name in enumerate(team_names)]
        return teams

    def save_html(self):
        with open(f'data/{self.match_id}.html', 'w') as file:
            file.write(str(self.soup))

    def generate_stats_values(self):
        for i, content in enumerate(self.content):
            div_ids = [
                'ds-w-full ds-table ds-table-xs ds-table-fixed ci-scorecard-table',
                'ds-w-full ds-table ds-table-xs ds-table-fixed',
            ]
            for div_id, stat_type in zip(div_ids, [batting_row, bowling_row]):
                table = content.find(class_=div_id)

                if not table:
                    continue

                for row in table.find_all('tr'):
                    try:
                        cols = [x.text.strip() for x in row.find_all('td')]
                        team = self.teams[i] if stat_type == batting_row else self.teams[not i]
                        player = team.players[extract_name(cols[0])]
                        stats = {item: value for item, value in zip(stat_type, cols[1:])}
                        yield player, stats
                    except (IndexError, TypeError, KeyError):
                        continue

    def update_statistics(self):
        for player, stats in self.generate_stats_values():
            # update batting and bowling statistics
            player.update_statistics(stats)

        for team in self.teams:
            for name, player in team.active_players.items():
                # update fielding statistics
                dismissal = Dismissal(player.statistics[StatItems.DISMISSAL.name].value)
                fielder = self.extract_fielder(dismissal.fielder, player.innings, dismissal.is_sub)
                if not fielder:
                    continue

                fielding = StatItems.FIELDING.name
                fielder.update_statistics({fielding: fielder.statistics[fielding].value + 1})

        # update potm statistics
        potm = self.extract_player_of_the_match()
        potm.update_statistics({StatItems.POTM.name: True})

    def extract_fielder(self, fielder_name, innings, sub):
        try:
            return self.teams[not innings].find_player(fielder_name, sub)
        except AttributeError:
            return

    def extract_player_of_the_match(self):
        try:
            class_name = 'ci-match-player-award-carousel'
            potm_container = self.soup.find(class_=class_name, recursive=True)
            potm = potm_container.find_all('span')[0].text.split(',')[0].strip()
            # logging.info(f'Player of the match: {potm}')
            if potm in self.teams[0].players:
                return self.teams[0].players[potm]
            else:
                return self.teams[1].players[potm]
        except AttributeError:
            pass
            # logging.info('No potm found')
        except KeyError:
            pass
            # logging.error(f'Potm does not exist')

    def __repr__(self):
        return f'Match Id: {self.match_id}. Teams: {self.teams}'
