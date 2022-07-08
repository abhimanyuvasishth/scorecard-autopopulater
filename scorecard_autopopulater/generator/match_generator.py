from scorecard_autopopulater.constants import Format, Stages
from scorecard_autopopulater.schema.match import Match
from scorecard_autopopulater.utils import get_json_from_url


class MatchGenerator:
    @staticmethod
    def generate_matches(limit=10) -> list[Match]:
        base_api_url = 'https://hs-consumer-api.espncricinfo.com/v1/pages'
        url = f'{base_api_url}/matches/current?lang=en&latest=true'

        for raw_match in get_json_from_url(url)['matches'][:limit]:
            yield Match(
                raw_match['objectId'],
                raw_match['series']['objectId'],
                raw_match['startTime'],
                Stages[raw_match['stage']],
                Format[raw_match['format']]
            )
