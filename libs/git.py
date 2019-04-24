import subprocess
from libs import utils


class Annex:
    def __init__(self):
        print('- Annex: init started.')
        # array of dict (annex data parsed)
        self.collection = []
        # array of dict (Candidate and Visit)
        self.collection_unique = []

    def refresh(self):
        # execute command: 'git annex metadata' in shell.
        p = subprocess.Popen(
            'git annex metadata',
            stdout=subprocess.PIPE,
            shell=True
        )
        (output, err) = p.communicate()
        # wait for date to terminate..
        p_status = p.wait()
        # verify return code 'p_status'.
        if p_status == 0:
            # success.
            parser = utils.Parser()
            self.collection = parser.read_annex_data(output)
            self.collection_unique = parser.get_candidate_and_timepoint_collection(
                self.collection
            )
            print(self.collection_unique)
            print('- Annex: success collecting data.')
        else:
            # error.
            print('- Annex: error! unable to read from git-annex.')
            self.collection = []
            self.collection_unique = []

    def update(self, file_and_url_array):
        # execute command: 'git annex add filename' in shell.
        for file_name_and_url in file_and_url_array:
            print('update for filename: ' + file_name_and_url[0] + ' and url: ' + file_name_and_url[1])
            p = subprocess.Popen(
                'git annex add ' + file_name_and_url[0],
                stdout=subprocess.PIPE,
                shell=True
            )
            (output, err) = p.communicate()
            # wait for date to terminate..
            p_status = p.wait()
            if p_status == 0:
                # success.
                print('1) success adding to git annex')
                # execute command: 'git annex lookupkey filename' in shell.
                p = subprocess.Popen(
                    'git annex lookupkey ' + file_name_and_url[0],
                    stdout=subprocess.PIPE,
                    shell=True
                )
                (output, err) = p.communicate()
                # wait for date to terminate..
                p_status = p.wait()
                if p_status == 0:
                    # success.
                    print('2) success on lookupkey of git annex.')
                    print('the output is:')
                    print(output)
                    output = str(output, 'utf-8')
                    output = output.replace(' ', '')
                    # execute command: 'git annex registerurl key url' in shell.
                    p = subprocess.Popen(
                        'git annex registerurl ' + output + ' ' + file_name_and_url[1],
                        stdout=subprocess.PIPE,
                        shell=True
                    )
                    (output, err) = p.communicate()
                    # wait for date to terminate..
                    p_status = p.wait()
                    if p_status == 0:
                        # success.
                        print('3) success on registerurl of git annex.')
                    else:
                        # error.
                        print('3) error on registerurl of git annex:')
                        print(err)
                else:
                    # error.
                    print('2) error on lookupkey of git annex:')
                    print(err)
            else:
                # error.
                print('1) error adding to git annex:')
                print(err)
