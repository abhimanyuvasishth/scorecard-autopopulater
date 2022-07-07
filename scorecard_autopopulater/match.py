from scorecard_autopopulater.dismissal import Dismissal
from scorecard_autopopulater.reader.data_row_reader import DataRowReader
from scorecard_autopopulater.scraper.scorecard_scraper import ScorecardScraper
from scorecard_autopopulater.stat_items import StatItems, batting_row, bowling_row
from scorecard_autopopulater.team import Team
from scorecard_autopopulater.utils import extract_name


class Match:
    def __init__(self, scraper: ScorecardScraper, squad_reader: DataRowReader, team_games=None):
        self.scraper = scraper
        self.squad_reader = squad_reader
        self.team_names = scraper.generate_team_names()
        self.team_games = team_games or {}
        self.teams = self.generate_teams()

    def generate_teams(self):
        teams = []
        for innings, team_name in enumerate(self.team_names):
            team_game = self.team_games.get(team_name)
            teams.append(Team(team_name, innings, self.squad_reader, team_game))
        return teams

    def update_statistics(self):
        for innings, row in self.scraper.generate_batting_rows():
            try:
                player = self.teams[innings].players[extract_name(row[0])]
                stats = {item: value for item, value in zip(batting_row, row[1:])}
                player.update_statistics(stats)
            except (IndexError, TypeError, KeyError):
                continue

        for innings, row in self.scraper.generate_bowling_rows():
            try:
                player = self.teams[not innings].players[extract_name(row[0])]
                stats = {item: value for item, value in zip(bowling_row, row[1:])}
                player.update_statistics(stats)
            except (IndexError, TypeError, KeyError):
                continue

        # update fielding statistics
        for team in self.teams:
            for name, player in team.active_players.items():
                dismissal = Dismissal(player.statistics[StatItems.DISMISSAL.name].value)
                fielding = StatItems.FIELDING.name

                try:
                    team = self.teams[not player.innings]
                    fielder = team.find_player(dismissal.fielder, dismissal.is_sub)
                    fielder.update_statistics({fielding: fielder.statistics[fielding].value + 1})
                except (AttributeError, KeyError):
                    continue

        # update potm statistics
        potm_name = self.scraper.potm_name
        try:
            potm = self.teams[0].find_player(potm_name) or self.teams[1].find_player(potm_name)
            potm.update_statistics({StatItems.POTM.name: True})
        except AttributeError:
            pass
