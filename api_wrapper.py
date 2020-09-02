from __future__ import print_function
import configparser
import json
import os
import requests
import json_to_csv
import sys
import pandas as pd


def query(configfile):
    # Query the PatentsView database using parameters specified in configfile
    parser = configparser.ConfigParser()
    parser.read(configfile)

    # Loop through the separate queries listed in the config file.
    for q in parser.sections():

        print("Running query: ", q)

        # Parse parameters from config file
        entity = json.loads(parser.get(q, 'entity'))
        url = 'https://api.patentsview.org/'+entity+'/query?'

        input_file = json.loads(parser.get(q, 'input_file'))
        directory = json.loads(parser.get(q, 'directory'))
        input_type = json.loads(parser.get(q, 'input_type'))
        fields = json.loads(parser.get(q, 'fields'))


        try:
            # If specified, 'sort' should be a list of dictionaries, specifying 
            # the order of keys and direction of each key.

            sort = json.loads(parser.get(q, 'sort'))
            sort_fields, sort_directions = [], []
            for dct in sort:
                for field in dct:
                    # We can only sort by fields that are in the data
                    if field in fields:
                        sort_fields.append(field)
                        sort_directions.append(dct[field])
            if len(sort_fields) == 0:
                sort_fields = [fields[0]]
                sort_directions = ["asc"]
        except:
            sort_fields = [fields[0]]
            sort_directions = ["asc"]

        criteria = {"_and": [json.loads(parser.get(q, option)) for option in
                        parser.options(q) if option.startswith('criteria')]}

        item_list = list(set(open(os.path.join(directory, input_file)).read().split('\n')))
        results_found = 0

        item_list_len = len(item_list)

        for item in item_list:
            params = {
                'q': {"_and": [{input_type: item}, criteria]},
                'f': fields 
                }

            r = requests.post(url, data=json.dumps(params))

            if 400 <= r.status_code <= 499:
                print("Client error when quering for value {}".format(item))
                print(url)
            elif r.status_code >= 500:
                print("Server error when quering for value {}. You may be exceeding the maximum API request size (1GB).".format(item))
            elif json.loads(r.text)['count'] != 0:
                    outp = open(os.path.join(directory, q + '_' + \
                                str(results_found) + '.json'), 'w')
                    print(r.text, end = '', file=outp)
                    outp.close()
                    results_found += 1

        if results_found == 0:
            print("Query {} returned no results".format(q))
        else:
            # Output merged CSV of formatted results.
            json_to_csv.main(directory, q, results_found)

            # Clean csv: reorder columns, drop duplicates, sort, then save
            output_filename = os.path.join(directory, q+'.csv')
            df = pd.read_csv(output_filename, dtype=object, encoding='Latin-1')
            df = df[fields].drop_duplicates().sort_values(by=sort_fields,
                    ascending=[direction != 'desc' for direction in sort_directions])
            df.to_csv(output_filename, index=False)
            print('({} rows returned)'.format(len(df)))


if __name__ == '__main__':
    if sys.version_info[0] != 3:
        print("Please use Python version 3; you are using version:", sys.version)
        sys.exit(1)

    if len(sys.argv) < 2:
        print("USAGE: python api_wrapper.py config_file")
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        print("File not found: ", sys.argv[1])

    query(sys.argv[1])