
class File:
    def __init__(self):
        pass

    def save_to_file(self, name_and_extension, content):
        myfile = open(name_and_extension, 'w')
        myfile.write(content)
        myfile.close()


class Parser:
    def __init__(self):
        pass

    # parse annex data into array of dictionaries.
    def read_annex_data(self, data):
        d = {}
        collection = []
        # loop line by line (the data).
        for line in data.splitlines():
            if not line or line is None:
                continue
            line = str(line)
            # strip whitespace and split string by '=' into array.
            arr = (line.replace(' ', '')).split('=')

            if len(arr) == 1:
                if bool(d):
                    collection.append(d)
                    d = {}
                arr = (line.strip()).split(' ')
                if len(arr) == 2:
                    d[arr[0]] = arr[1]
            elif len(arr) == 2:
                d[arr[0]] = arr[1]
        return collection

    def get_candidate_and_timepoint_collection(self, collection):
        arr = []
        # create collection of dict: 'Candidate' & 'Visit'
        for item in collection:
            item = item.decode('ascii')
            print (item)
            if 'Candidate' in item and 'Visit' in item:
                print('WTF')
                arr.append({
                    'Candidate': item['Candidate'],
                    'Visit': item['Visit']
                })
        # remove duplicates
        seen = set()
        new_collection = []
        for d in arr:
            print ('d:')
            print (d)
            t = tuple(sorted(d.items()))
            if t not in seen:
                seen.add(t)
                new_collection.append(d)
        print ('Santiago Check new_collection:')
        print (new_collection)
        return new_collection
