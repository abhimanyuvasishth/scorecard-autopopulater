from itertools import chain

from scorecard_autopopulater.match.cricket_match import (CricketMatch, CricketMatchFormat,
                                                         CricketMatchStages)
from scorecard_autopopulater.utils import get_json_from_url

URL = 'https://hs-consumer-api.espncricinfo.com/v1/pages'
LIVE_URL = f'{URL}/matches/current?lang=en&latest=true'


def generate_live_matches() -> list[CricketMatch]:
    for raw_match in get_json_from_url(LIVE_URL)['matches']:
        yield CricketMatch(
            id=raw_match['objectId'],
            tournament_id=raw_match['series']['objectId'],
            stage=CricketMatchStages[raw_match['stage']],
            format=CricketMatchFormat[raw_match['format']],
            start_time=raw_match['startTime']
        )


def generate_matches_by_tournament(tournament_id: str) -> list[CricketMatch]:
    schedule_url = f'{URL}/series/schedule?lang=en&seriesId={tournament_id}'
    fixtures = get_json_from_url(schedule_url, params={'fixtures': True})
    results = get_json_from_url(schedule_url, params={'fixtures': False})

    all_matches = {}
    for raw_match in chain(fixtures['content']['matches'], results['content']['matches']):
        match = CricketMatch(
            id=raw_match['objectId'],
            tournament_id=raw_match['series']['objectId'],
            stage=CricketMatchStages[raw_match['stage']],
            format=CricketMatchFormat[raw_match['format']],
            start_time=raw_match['startTime']
        )
        all_matches[match.id] = match

    for match in sorted(all_matches.values(), key=lambda game: game.start_time):
        yield match
