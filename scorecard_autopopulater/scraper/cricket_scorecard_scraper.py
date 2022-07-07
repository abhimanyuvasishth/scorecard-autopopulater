from scorecard_autopopulater.scraper.scorecard_scraper import ScorecardScraper


class CricketScorecardScraper(ScorecardScraper):
    @property
    def content(self):
        class_name = 'ReactCollapse--collapse'
        return self.soup.find_all(class_=class_name, recursive=True)

    @property
    def potm_name(self):
        try:
            classes = [
                'ds-flex ds-justify-between ds-items-center',
                'ds-px-4 ds-py-2 ds-self-stretch ds-w-full ds-border-line ds-border-none',
            ]
            potm_container = self.soup.find_all(True, {'class': classes})[0]
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

            text = container.text.replace(' 1st', '').replace(' 2nd', '')
            team_text = text.split('INNINGS')[0].split('Team')[0].strip().title()
            yield team_text

    def generate_rows(self, div_id):
        innings = 0
        for order, content in enumerate(self.content):
            table = content.find(class_=div_id)
            innings += 1

            if not table:
                continue

            for row in table.find_all('tr'):
                yield innings - 1, [x.text.strip() for x in row.find_all('td')]

    def generate_batting_rows(self):
        div_id = 'ds-w-full ds-table ds-table-xs ds-table-fixed ci-scorecard-table'
        for row in self.generate_rows(div_id):
            yield row

    def generate_bowling_rows(self):
        div_id = 'ds-w-full ds-table ds-table-xs ds-table-fixed'
        for row in self.generate_rows(div_id):
            yield row
