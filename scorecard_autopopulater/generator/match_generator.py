import requests

from scorecard_autopopulater.constants import Format, Stages
from scorecard_autopopulater.schema.match import Match
from scorecard_autopopulater.utils import tracing


class MatchGenerator:
    @tracing(requests.exceptions.HTTPError, message='Scraping live matches failed')
    def generate_matches(self, limit=10) -> list[Match]:
        count = 0
        base_api_url = 'https://hs-consumer-api.espncricinfo.com/v1/pages'
        url = f'{base_api_url}/matches/current?lang=en&latest=true'

        response = requests.get(url)
        response.raise_for_status()
        content = response.json()
        matches = content['matches']

        for raw_match in matches:
            yield Match(
                raw_match['objectId'],
                raw_match['series']['objectId'],
                raw_match['startTime'],
                Stages[raw_match['stage']],
                Format[raw_match['format']]
            )
            count += 1
            if count == limit:
                break
