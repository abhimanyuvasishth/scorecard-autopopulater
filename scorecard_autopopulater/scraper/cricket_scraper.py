from collections import Counter

import requests

from scorecard_autopopulater.schema.player import Player
from scorecard_autopopulater.schema.team import Team
from scorecard_autopopulater.utils import tracing


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

        self.content = self.get_json(self.content_url)

    @tracing(requests.exceptions.HTTPError, message='get_json failed')
    def get_json(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def add_match_numbers(self, teams):
        team_lookup = {team.id: team for team in teams}
        fixtures = self.get_json(self.schedule_url)
        teams_played = []

        for match in sorted(fixtures['content']['matches'], key=lambda game: game['startTime']):
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

    @tracing(errors=TypeError, message='no players to add')
    def add_players(self, teams):
        for index, team in enumerate(teams):
            for player in self.content['matchPlayers']['teamPlayers'][index]['players']:
                team.add_player(self.create_player(player))

    @tracing(errors=TypeError, message='no scorecard')
    def get_innings_scorecard(self):
        return self.content['scorecard']['innings']

    @staticmethod
    @tracing(errors=KeyError, message='Creating Sub Fielder', raises=True)
    def get_fielder(fielding_team, fielder_id):
        return fielding_team.get_player(fielder_id)

    def add_statistics(self, teams, team_lookup):
        for i, scorecard in enumerate(self.get_innings_scorecard() or []):
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
                        fielder_id = fielder['player']['objectId']
                        player = self.get_fielder(fielding_team, fielder_id)
                    except TypeError:
                        continue
                    except KeyError:
                        player = self.create_player(fielder)
                        fielding_team.add_player(player)

                    if fielder_number == 0:
                        player.statistics[innings].fielding_primary += 1
                    else:
                        player.statistics[innings].fielding_secondary += 1

    @tracing(errors=TypeError, message='No POTM')
    def add_potm_statistics(self, team_lookup):
        for potm in self.content['supportInfo'].get('playersOfTheMatch', []):
            team_id, player_id = potm['team']['objectId'], potm['player']['objectId']
            team_lookup[team_id].get_player(player_id).statistics[0].potm = 1
