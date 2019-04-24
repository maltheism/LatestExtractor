import json
from libs import utils
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Loris:
    # setup variables.
    def __init__(self, url, username, password):
        print('- Loris: init started.')
        # Version number of API.
        self.version = 'v0.0.3-dev'
        # URL for accessing the API.
        self.url = url + '/api/' + self.version
        # API commands.
        self.api = {
            'login': '/login',
            'candidates': '/candidates/',
        }
        # Username and Password for login.
        self.username = username
        self.password = password
        # Token when successful login completes.
        self.token = ''
        # Error message details.
        self.error = ''
        # candidates data
        self.candidates = []
        # used to make files and save content.
        self.file = utils.File()
        # history of file & url created.
        self.history_file_and_url = []
        print('- Loris: init finished.')

    # login session for loris instance.
    def login(self):
        print('- Loris: login fired!')
        # login parameters for post.
        login_params = {
            'username': self.username,
            'password': self.password
        }
        # sending post request and saving the response.
        login_request = requests.post(
            url=self.url + self.api['login'],
            json=login_params,
            verify=False
        )
        try:
            # raise an exception for non-200 status code.
            login_request.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print('- Loris: login failed. HTTPError!')
            self.error = str(error)
            return False
        # extracting data in json format.
        login_data = login_request.json()
        # save token if success, return true and otherwise return false.
        if 'error' in login_data:
            self.error = 'Login token contains error.'
            print('- Loris: login failed.')
            return False
        else:
            self.token = login_data['token']
            print('- Loris: login success.')
            return True

    # fetch all candidates from loris instance.
    def fetch_candidates(self):
        print('- Loris: fetch_candidates fired!')
        candidates_response = json.loads(requests.get(
            url=self.url + self.api['candidates'],
            verify=False,
            headers={
                'Authorization': 'Bearer %s' % self.token
            }
        ).content.decode('ascii'))
        if 'Candidates' in candidates_response:
            self.candidates = candidates_response['Candidates']
            return True
        else:
            self.candidates = []
            return False

    # requires cand_id: CandID
    # return candidate from loris instance.
    def get_candidate(self, cand_id):
        print('- Loris: get_candidate from CandID: ' + cand_id)
        candidate = json.loads(requests.get(
            url=self.url + self.api['candidates'] + cand_id,
            verify=False,
            headers={
                'Authorization': 'Bearer %s' % self.token
            }
        ).content.decode('ascii'))
        return candidate

    # return all instruments from candidates
    # (array of dict: containing CandID) supplied.
    def fetch_instruments(self, collection):
        print('- Loris: fetch_instruments fired!')
        print ('HELP! Check:')
        print (collection)
        if collection:
            for item in collection:
                if item['Candidate']:
                    # get instruments for Candidate and Visit.
                    instruments_in_candidate = json.loads(requests.get(
                        url=self.url + self.api['candidates']
                                     + item['Candidate']
                                     + '/'
                                     + item['Visit']
                                     + '/instruments',
                        verify=False,
                        headers={
                            'Authorization': 'Bearer %s' % self.token
                        }
                    ).content.decode('ascii'))
                    # fetch instrument data from instruments (array).
                    if not instruments_in_candidate.get('error') \
                            and instruments_in_candidate['Instruments']:
                        # per instrument in instruments (array).
                        for instrument in instruments_in_candidate['Instruments']:
                            print(instrument)
                            # get instrument data received here.
                            instrument_data = json.loads(requests.get(
                                url=self.url + self.api['candidates']
                                             + item['Candidate']
                                             + '/'
                                             + item['Visit']
                                             + '/instruments/' + instrument,
                                verify=False,
                                headers={
                                    'Authorization': 'Bearer %s' % self.token
                                }
                            ).content.decode('ascii'))
                            if 'error' in instrument_data:
                                print('error - instrument data:')
                                print(instrument_data)
                            else:
                                # save instrument data to file
                                self.file.save_to_file(
                                    instrument_data['Meta']['Candidate'] + '_' +
                                    instrument_data['Meta']['Visit'] + '_' +
                                    instrument_data['Meta']['Instrument'],
                                    json.dumps(instrument_data)
                                )
                                # add "full_filename & url" to history_file_and_url array.
                                self.history_file_and_url.append(
                                    [
                                        instrument_data['Meta']['Candidate'] + '_' +
                                        instrument_data['Meta']['Visit'] + '_' +
                                        instrument_data['Meta']['Instrument'],
                                        self.url + self.api['candidates']
                                        + item['Candidate']
                                        + '/'
                                        + item['Visit']
                                        + '/instruments/' + instrument
                                     ]
                                )
                                print('instrument data: ')
                                print(instrument_data)
            print('- Loris: fetch_instruments complete.')
            return self.candidates
        else:
            print('Extractor: candidates empty.')
            return []

    # def fetch_instruments(self, collection):
    #     print '- Loris: fetch_instruments fired!'
    #     if self.candidates:
    #         for index, candidate in enumerate(self.candidates):
    #             if candidate['CandID']:
    #                 # get candidate object containing the visit_labels (array).
    #                 self.candidates[index] = self.get_candidate(candidate['CandID'])
    #                 for visit_label in (self.candidates[index])['Visits']:
    #                     print visit_label
    #                     # get instruments for visit_label.
    #                     instruments_in_candidate = json.loads(requests.get(
    #                         url=self.url + self.api['candidates']
    #                                      + candidate['CandID']
    #                                      + '/'
    #                                      + visit_label
    #                                      + '/instruments',
    #                         verify=False,
    #                         headers={
    #                             'Authorization': 'Bearer %s' % self.token
    #                         }
    #                     ).content.decode('ascii'))
    #                     # fetch instrument data from instruments (array).
    #                     if not instruments_in_candidate.get('error') \
    #                             and instruments_in_candidate['Instruments']:
    #                         # per instrument in instruments (array).
    #                         for instrument in instruments_in_candidate['Instruments']:
    #                             # get instrument data received here.
    #                             instrument_data = json.loads(requests.get(
    #                                 url=self.url + self.api['candidates']
    #                                              + candidate['CandID']
    #                                              + '/'
    #                                              + visit_label
    #                                              + '/instruments/' + instrument,
    #                                 verify=False,
    #                                 headers={
    #                                     'Authorization': 'Bearer %s' % self.token
    #                                 }
    #                             ).content.decode('ascii'))
    #                             print instrument_data
    #         print '- Loris: fetch_instruments complete.'
    #         return self.candidates
    #     else:
    #         print 'Extractor: candidates empty.'
    #         return []

    def get_instrument(self, cand_id, visit_label):
        print('- Loris: instrument fired!')
        if cand_id and visit_label:
            instrument = json.loads(requests.get(
                url=self.url + self.api['candidates'] + cand_id + '/' + visit_label + '/instruments'
            ))
