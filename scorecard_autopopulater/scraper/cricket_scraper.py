from collections import Counter
from itertools import chain

from scorecard_autopopulater.player.player import Player
from scorecard_autopopulater.scraper.scraper import Scraper
from scorecard_autopopulater.team.team import Team
from scorecard_autopopulater.utils import get_json_from_url, tracing

URL = 'https://hs-consumer-api.espncricinfo.com/v1/pages'


class CricketScraper(Scraper):

    def __init__(self, match_id=None, series_id=None):
        self.match_id = match_id
        self.series_id = series_id

        self.api_match_url = f'{URL}/match/details?lang=en'
        self.content_url = f'{self.api_match_url}&seriesId={self.series_id}&matchId={self.match_id}'
        self.content = get_json_from_url(self.content_url)

        self.api_schedule_url = f'{URL}/series/schedule?lang=en&seriesId={self.series_id}'

    def add_match_numbers(self, teams):
        team_lookup = {team.id: team for team in teams}
        fixtures = get_json_from_url(self.api_schedule_url, params={'fixtures': True})
        results = get_json_from_url(self.api_schedule_url, params={'fixtures': False})

        all_matches = {}
        for match in chain(fixtures['content']['matches'], results['content']['matches']):
            all_matches[match['objectId']] = match

        teams_played = []
        for match_id, match in sorted(all_matches.items(), key=lambda game: game[1]['startTime']):
            for team_played in match['teams']:
                teams_played.append(team_played['team']['objectId'])

            if match_id == self.match_id:
                break

        counter = Counter(teams_played)
        for team_id, team in team_lookup.items():
            team.match_number = counter[team_id]

    def generate_teams(self):
        for team in self.content['match']['teams']:
            yield Team(
                id=team['team']['objectId'],
                name=team['team']['name'],
                long_name=team['team']['longName'],
                abbreviation=team['team']['abbreviation']
            )

    @staticmethod
    def create_player(player):
        return Player(
            id=player['player']['objectId'],
            name=player['player']['name'],
            long_name=player['player']['longName'],
            fielding_name=player['player']['fieldingName']
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
                player.player_stats[innings].dismissal = batter['dismissalText']['long'].strip()
                player.player_stats[innings].runs_scored = batter['runs']
                player.player_stats[innings].balls_faced = batter['balls']
                player.player_stats[innings].minutes = batter['minutes']
                player.player_stats[innings].fours_scored = batter['fours']
                player.player_stats[innings].sixes_scored = batter['sixes']
                player.player_stats[innings].strike_rate = batter['strikerate']
                player.player_stats[innings].not_out = not batter['isOut']

            for bowler in scorecard['inningBowlers']:
                if bowler['bowledType'] != 'yes':
                    continue

                player = fielding_team.get_player(bowler['player']['objectId'])
                player.player_stats[innings].overs = bowler['overs']
                player.player_stats[innings].maidens = bowler['maidens']
                player.player_stats[innings].runs_conceded = bowler['conceded']
                player.player_stats[innings].wickets = bowler['wickets']
                player.player_stats[innings].fours_conceded = bowler['fours']
                player.player_stats[innings].sixes_conceded = bowler['sixes']
                player.player_stats[innings].wides = bowler['wides']
                player.player_stats[innings].no_balls = bowler['noballs']
                player.player_stats[innings].economy_rate = bowler['economy']

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
                        player.player_stats[innings].fielding_primary += 1
                    else:
                        player.player_stats[innings].fielding_secondary += 1

    @tracing(errors=TypeError, message='No POTM')
    def add_potm_statistics(self, team_lookup):
        for potm in self.content['supportInfo'].get('playersOfTheMatch', []):
            team_id, player_id = potm['team']['objectId'], potm['player']['objectId']
            team_lookup[team_id].get_player(player_id).player_stats[0].potm = 1
