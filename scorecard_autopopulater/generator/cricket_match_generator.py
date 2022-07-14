from scorecard_autopopulater.generator.match_generator import MatchGenerator
from scorecard_autopopulater.match.cricket_match import (CricketMatch, CricketMatchFormat,
                                                         CricketMatchStages)
from scorecard_autopopulater.utils import get_json_from_url


class CricketMatchGenerator(MatchGenerator):
    def generate_matches(self, limit=10) -> list[CricketMatch]:
        base_api_url = 'https://hs-consumer-api.espncricinfo.com/v1/pages'
        url = f'{base_api_url}/matches/current?lang=en&latest=true'

        for raw_match in get_json_from_url(url)['matches'][:limit]:
            yield CricketMatch(
                id=raw_match['objectId'],
                tournament_id=raw_match['series']['objectId'],
                stage=CricketMatchStages[raw_match['stage']],
                format=CricketMatchFormat[raw_match['format']]
            )
