from collections import Counter

from scorecard_autopopulater.match.cricket_match import CricketMatch
from scorecard_autopopulater.stat_items import bowling_row
from scorecard_autopopulater.team.cricket_team import CricketTeam
from scorecard_autopopulater.utils import extract_name


class CricketTestMatch(CricketMatch):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.innings_mapper = {1: 0, 0: 1, 2: 3, 3: 2}

    def add_follow_on_team(self):
        if len(self.teams) % 2 and len(self.teams) > 2:
            team_counter = Counter(self.teams)
            team = min(team_counter, key=team_counter.get)
            new_team = CricketTeam(team.name, len(self.teams), self.squad_reader, team.game_number)
            for player_name in team.active_players:
                new_team.players[player_name].active = True
            self.teams.append(new_team)

    def update_bowling_statistics(self):
        for order, row in self.scraper.generate_bowling_rows():
            try:
                team = self.teams[self.innings_mapper[order]]
            except IndexError:
                self.add_follow_on_team()
                team = self.teams[self.innings_mapper[order]]

            try:
                player = team.players[extract_name(row[0])]
                stats = {item: value for item, value in zip(bowling_row, row[1:])}
                player.update_statistics(stats)
            except (IndexError, TypeError, KeyError):
                continue
