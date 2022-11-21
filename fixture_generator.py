import json
from urllib.request import urlopen

from bs4 import BeautifulSoup


if __name__ == '__main__':
    url = 'https://fixtur.es/en/fifa-world-cup-qatar?'
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    div = soup.find_all('div', { "class" : "wedstrijden table round" })[0]
    templates = []
    count = 1
    for match in div.find_all('script'):
        text = json.loads(match.text)
        template = {
            "team_1": text['homeTeam']['name'],
            "team_1_num": 1,
            "team_2": text['awayTeam']['name'],
            "team_2_num": 1,
            "start_timestamp": text['startDate'].split('+')[0] + '.000Z',
            "object_id": count,
            "match_day": 1
        }
        templates.append(template)
        count += 1
    print(json.dumps(templates))
