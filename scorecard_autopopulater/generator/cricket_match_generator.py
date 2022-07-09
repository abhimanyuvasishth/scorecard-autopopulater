from scorecard_autopopulater.constants import Format, Stages
from scorecard_autopopulater.match.cricket_match import CricketMatch
from scorecard_autopopulater.utils import get_json_from_url


class MatchGenerator:
    @staticmethod
    def generate_matches(limit=10) -> list[CricketMatch]:
        base_api_url = 'https://hs-consumer-api.espncricinfo.com/v1/pages'
        url = f'{base_api_url}/matches/current?lang=en&latest=true'

        for raw_match in get_json_from_url(url)['matches'][:limit]:
            yield CricketMatch(
                id=raw_match['objectId'],
                tournament_id=raw_match['series']['objectId'],
                start_time=raw_match['startTime'],
                stage=Stages[raw_match['stage']],
                format=Format[raw_match['format']]
            )
