from collections import Counter

import requests

from scorecard_autopopulater.schema.player import Player
from scorecard_autopopulater.schema.team import Team


class CricketScraper:
    def __init__(self, match_id=None, series_id=None):
        self.match_id = match_id
        self.series_id = series_id

        self.base_url = 'https://www.espncricinfo.com'
        self.api_base_url = 'https://hs-consumer-api.espncricinfo.com/v1/pages'

        self.api_match_url = f'{self.api_base_url}/match/details?lang=en'
        self.content_url = f'{self.api_match_url}&seriesId={self.series_id}&matchId={self.match_id}'

        self.api_schedule_url = f'{self.api_base_url}/series/schedule?lang=en'
        self.schedule_url = f'{self.api_schedule_url}&seriesId={self.series_id}&fixtures=false'

    @property
    def content(self):
        return requests.get(self.content_url).json()

    def add_match_numbers(self, teams):
        team_lookup = {team.id: team for team in teams}
        data = requests.get(self.schedule_url).json()
        teams_played = []

        for match in sorted(data['content']['matches'], key=lambda game: game['startTime']):
            for team_played in match['teams']:
                teams_played.append(team_played['team']['objectId'])

            if match['objectId'] == self.match_id:
                break

        counter = Counter(teams_played)
        for team_id, team in team_lookup.items():
            team.match_number = counter[team_id]

    def generate_teams(self):
        for index, team in enumerate(self.content['match']['teams']):
            yield Team(
                team['team']['objectId'],
                team['team']['name'],
                team['team']['longName'],
                team['team']['abbreviation']
            )

    @staticmethod
    def create_player(player):
        return Player(
            player['player']['objectId'],
            player['player']['name'],
            player['player']['longName'],
            player['player']['fieldingName']
        )

    def add_players(self, teams):
        for index, team in enumerate(teams):
            try:
                for player in self.content['matchPlayers']['teamPlayers'][index]['players']:
                    team.add_player(self.create_player(player))
            except TypeError:
                pass

    def add_statistics(self, teams, team_lookup):
        for i, scorecard in enumerate(self.content['scorecard']['innings']):
            batting_team = team_lookup[scorecard['team']['objectId']]
            fielding_team = teams[not teams.index(batting_team)]
            innings = i // 2

            for batter in scorecard['inningBatsmen']:
                if batter['battedType'] in {'DNB', 'sub'}:
                    continue

                player = batting_team.get_player(batter['player']['objectId'])
                player.statistics[innings].dismissal = batter['dismissalText']['long'].strip()
                player.statistics[innings].runs_scored = batter['runs']
                player.statistics[innings].balls_faced = batter['balls']
                player.statistics[innings].minutes = batter['minutes']
                player.statistics[innings].fours_scored = batter['fours']
                player.statistics[innings].sixes_scored = batter['sixes']
                player.statistics[innings].strike_rate = batter['strikerate']
                player.statistics[innings].not_out = not batter['isOut']

            for bowler in scorecard['inningBowlers']:
                if bowler['bowledType'] != 'yes':
                    continue

                player = fielding_team.get_player(bowler['player']['objectId'])
                player.statistics[innings].overs = bowler['overs']
                player.statistics[innings].maidens = bowler['maidens']
                player.statistics[innings].runs_conceded = bowler['conceded']
                player.statistics[innings].wickets = bowler['wickets']
                player.statistics[innings].fours_conceded = bowler['fours']
                player.statistics[innings].sixes_conceded = bowler['sixes']
                player.statistics[innings].wides = bowler['wides']
                player.statistics[innings].no_balls = bowler['noballs']
                player.statistics[innings].economy_rate = bowler['economy']

            for wicket in scorecard['inningWickets']:
                for fielder_number, fielder in enumerate(wicket['dismissalFielders']):
                    try:
                        player = fielding_team.get_player(fielder['player']['objectId'])
                    except TypeError:
                        continue
                    except KeyError:
                        player = self.create_player(fielder)
                        fielding_team.add_player(player)

                    if fielder_number == 0:
                        player.statistics[innings].fielding_primary += 1
                    else:
                        player.statistics[innings].fielding_secondary += 1

    def add_potm_statistics(self):
        try:
            for potm in self.content['supportInfo']['playersOfTheMatch']:
                yield potm['team']['objectId'], potm['player']['objectId']
        except (KeyError, TypeError):
            pass
