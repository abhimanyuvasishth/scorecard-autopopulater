import requests

from scorecard_autopopulater.constants import MatchFormats
from scorecard_autopopulater.schema.match import Match
from scorecard_autopopulater.scraper.cricket_scraper import CricketScraper


class MatchGenerator:
    def __init__(self, limit=1):
        self.limit = limit

    @staticmethod
    def scrape_matches() -> list[int]:
        base_api_url = 'https://hs-consumer-api.espncricinfo.com/v1/pages'
        url = f'{base_api_url}/matches/current?lang=en&latest=true'
        content = requests.get(url).json()
        for match in content['matches']:
            if MatchFormats[match['format']] != MatchFormats.TEST:
                yield match['objectId']

    def generate_matches(self) -> list[Match]:
        for i, match_id in enumerate(self.scrape_matches()):
            if i == self.limit:
                break

            scraper = CricketScraper(match_id)
            content = scraper.content
            match = Match(content['match']['objectId'], content['match']['startTime'])
            for inning, team in enumerate(scraper.generate_teams()):
                scraper.add_players(team, inning)
                match.add_team(team)

            scraper.add_match_numbers(match.teams)
            scraper.add_statistics(match.teams)

            for potm_team_id, potm_player_id in scraper.add_potm_statistics():
                match.get_team(potm_team_id).get_player(potm_player_id).statistics.potm = 1

            yield match
