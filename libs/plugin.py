from libs import git
from libs import config
from libs import openscience


class Extractor:
    # setup variables and login to loris instance.
    def __init__(self):
        print('Extractor: init started.')
        # loris "username & password" required.
        self.loris = openscience.Loris(
            config.Settings.url,
            config.Settings.username,
            config.Settings.password
        )
        # online status (successful login or not) of loris.
        self.status = self.loris.login()
        # candidates from loris instance.
        self.candidates = []
        # instruments from loris instance.
        self.instruments = []
        # git annex (fetches data)
        self.annex = git.Annex()
        print('Extractor: init finished.')

    # retrieve latest data.
    def refresh(self):
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~')
        # refresh data from git annex
        self.annex.refresh()
        # loris login was successful.
        if self.status:
            print('Extractor: fetching instrument data.')
            self.loris.fetch_instruments(self.annex.collection_unique)
            self.annex.update(self.loris.history_file_and_url)
        else:
            print('Extractor: loris instance is offline.')

    # process data.
    def process(self):
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~')
        # loris login was successful.
        if self.status:
            # fetch latest candidates, return success or error.
            print('Extractor: processing data..')

            # self.status = self.loris.fetch_candidates()
            # if self.status:
            #     print 'Extractor: success fetching candidates.'
            #     self.loris.fetch_instruments()
            # else:
            #     print 'Extractor: error fetching candidates.'
        else:
            print('Extractor: loris instance is offline.')
