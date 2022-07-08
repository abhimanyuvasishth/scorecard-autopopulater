import logging

import requests

from scorecard_autopopulater.schema.match import Match


class MatchGenerator:
    def __init__(self, limit=10):
        self.limit = limit

    @staticmethod
    def scrape_matches() -> list[(int, int)]:
        base_api_url = 'https://hs-consumer-api.espncricinfo.com/v1/pages'
        url = f'{base_api_url}/matches/current?lang=en&latest=true'

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.exception(e)
            return

        content = response.json()
        matches = content['matches']
        for match in matches:
            yield match['objectId'], match['series']['objectId'], match['startTime']

    def generate_matches(self) -> list[Match]:
        for i, (match_id, series_id, start_time) in enumerate(self.scrape_matches()):
            if i == self.limit:
                break

            yield Match(match_id, series_id, start_time)
