from scorecard_autopopulater.scraper.scorecard_scraper import ScorecardScraper


class CricinfoScorecardScraper(ScorecardScraper):
    @property
    def content(self):
        class_name = 'ReactCollapse--collapse'
        return self.soup.find_all(class_=class_name, recursive=True)

    @property
    def potm_name(self):
        try:
            class_name = 'ci-match-player-award-carousel'
            potm_container = self.soup.find(class_=class_name, recursive=True)
            return potm_container.find_all('span')[0].text.split(',')[0].strip()
        except AttributeError:
            pass

    def generate_team_names(self):
        class_name = 'ds-text-tight-s ds-font-bold ds-uppercase'
        containers = self.soup.find_all('span', class_=class_name)

        div = 'ds-text-tight-s ds-font-bold ds-uppercase ds-p-4 ds-pb-2 ds-border-b ds-border-line'
        if len(containers) == 1:
            containers += self.soup.find_all(class_=div)

        for container in containers:
            if not container:
                continue

            team_text = container.text.split('INNINGS')[0].split('Team')[0].strip().title()
            yield team_text

    def generate_batting_rows(self):
        for order, content in enumerate(self.content):
            div_id = 'ds-w-full ds-table ds-table-xs ds-table-fixed ci-scorecard-table'
            table = content.find(class_=div_id)

            if not table:
                continue

            for row in table.find_all('tr'):
                yield order, [x.text.strip() for x in row.find_all('td')]

    def generate_bowling_rows(self):
        for order, content in enumerate(self.content):
            div_id = 'ds-w-full ds-table ds-table-xs ds-table-fixed'

            table = content.find(class_=div_id)

            if not table:
                continue

            for row in table.find_all('tr'):
                yield order, [x.text.strip() for x in row.find_all('td')]
