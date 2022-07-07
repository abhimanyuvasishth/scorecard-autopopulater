from scorecard_autopopulater.dismissal import Dismissal
from scorecard_autopopulater.match.match import Match
from scorecard_autopopulater.stat_items import StatItems, batting_row, bowling_row
from scorecard_autopopulater.team.cricket_team import CricketTeam
from scorecard_autopopulater.utils import extract_name


class CricketMatch(Match):
    def generate_teams(self):
        teams = []
        for order, team_name in enumerate(self.team_names):
            team_game = self.team_games.get(team_name)
            teams.append(CricketTeam(team_name, order, self.squad_reader, team_game))
        return teams

    def update_statistics(self):
        for order, row in self.scraper.generate_batting_rows():
            try:
                player = self.teams[order].players[extract_name(row[0])]
                stats = {item: value for item, value in zip(batting_row, row[1:])}
                player.update_statistics(stats)
            except (IndexError, TypeError, KeyError):
                continue

        for order, row in self.scraper.generate_bowling_rows():
            try:
                player = self.teams[not order].players[extract_name(row[0])]
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
                    team = self.teams[not player.order]
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
