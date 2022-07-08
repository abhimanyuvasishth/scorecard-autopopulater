from collections import Counter

import requests

from scorecard_autopopulater.schema.player import Player
from scorecard_autopopulater.schema.team import Team


class CricketScraper:
    def __init__(self, match_id):
        self.match_id = match_id

        self.base_url = 'https://www.espncricinfo.com'
        self.api_base_url = 'https://hs-consumer-api.espncricinfo.com/v1/pages'

        self.match_url = f'{self.base_url}/matches/engine/match/{self.match_id}.json'
        self.series_id = int(requests.get(self.match_url).json()['series'][0]['object_id'])

        self.api_match_url = f'{self.api_base_url}/match/details?lang=en'
        self.api_schedule_url = f'{self.api_base_url}/series/schedule?lang=en'

    @property
    def content(self):
        content_url = f'{self.api_match_url}&seriesId={self.series_id}&matchId={self.match_id}'
        return requests.get(content_url).json()

    def add_match_numbers(self, teams):
        team_lookup = {team.id: team for team in teams}
        schedule_url = f'{self.api_schedule_url}&seriesId={self.series_id}&fixtures=false'
        data = requests.get(schedule_url).json()
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
                team['team']['abbreviation'],
                team['inningNumbers']
            )

    @staticmethod
    def create_player(player):
        return Player(
            player['player']['objectId'],
            player['player']['name'],
            player['player']['longName'],
            player['player']['fieldingName']
        )

    def add_players(self, team, index):
        for player in self.content['matchPlayers']['teamPlayers'][index]['players']:
            team.add_player(self.create_player(player))

    def add_statistics(self, teams):
        for innings, scorecard in enumerate(self.content['scorecard']['innings']):
            for batter in scorecard['inningBatsmen']:
                if batter['battedType'] == 'DNB':
                    continue

                player = teams[innings].get_player(batter['player']['objectId'])
                player.statistics.dismissal = batter['dismissalText']['long'].strip()
                player.statistics.runs_scored = batter['runs']
                player.statistics.balls_faced = batter['balls']
                player.statistics.minutes = batter['minutes']
                player.statistics.fours_scored = batter['fours']
                player.statistics.sixes_scored = batter['sixes']
                player.statistics.strike_rate = batter['strikerate']
                player.statistics.not_out = not batter['isOut']

            for bowler in scorecard['inningBowlers']:
                if bowler['bowledType'] != 'yes':
                    continue

                player = teams[not innings].get_player(bowler['player']['objectId'])
                player.statistics.overs = bowler['overs']
                player.statistics.maidens = bowler['maidens']
                player.statistics.runs_conceded = bowler['conceded']
                player.statistics.wickets = bowler['wickets']
                player.statistics.fours_conceded = bowler['fours']
                player.statistics.sixes_conceded = bowler['sixes']
                player.statistics.wides = bowler['wides']
                player.statistics.no_balls = bowler['noballs']
                player.statistics.economy_rate = bowler['economy']

            for wicket in scorecard['inningWickets']:
                for i, fielder in enumerate(wicket['dismissalFielders']):
                    try:
                        player = teams[not innings].get_player(fielder['player']['objectId'])
                    except TypeError:
                        continue
                    except KeyError:
                        player = self.create_player(fielder)
                        teams[not innings].add_player(player)

                    if i == 0:
                        player.statistics.fielding_primary += 1
                    else:
                        player.statistics.fielding_secondary += 1

    def add_potm_statistics(self):
        try:
            for potm in self.content['supportInfo']['playersOfTheMatch']:
                yield potm['team']['objectId'], potm['player']['objectId']
        except (KeyError, TypeError):
            pass
