from scorecard_autopopulater.match.cricket_match import (CricketMatch, CricketMatchFormat,
                                                         CricketMatchStages)
from scorecard_autopopulater.utils import get_json_from_url

LIVE_URL = 'https://hs-consumer-api.espncricinfo.com/v1/pages/matches/current?lang=en&latest=true'


def generate_matches() -> list[CricketMatch]:
    for raw_match in get_json_from_url(LIVE_URL)['matches']:
        yield CricketMatch(
            id=raw_match['objectId'],
            tournament_id=raw_match['series']['objectId'],
            stage=CricketMatchStages[raw_match['stage']],
            format=CricketMatchFormat[raw_match['format']]
        )
