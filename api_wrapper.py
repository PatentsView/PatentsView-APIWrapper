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

        # Parse parameters from config file
        entity = json.loads(parser.get(q, 'entity'))
        url = 'http://www.patentsview.org/api/'+entity+'/query?'

        input_file = json.loads(parser.get(q, 'input_file'))
        directory = json.loads(parser.get(q, 'directory'))
        input_type = json.loads(parser.get(q, 'input_type'))
        fields = json.loads(parser.get(q, 'fields'))

        try:
            sort = json.loads(parser.get(q, 'sort'))
        except:
            sort = fields[0]

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

            if json.loads(r.text)['count'] != 0:
                outp = open(os.path.join(directory, q + '_' + \
                            str(results_found) + '.json'), 'w')
                print(r.text, end = '', file=outp)
                outp.close()
                results_found += 1

        # Output merged CSV of formatted results.
        json_to_csv.main(directory, q, results_found)

        # Clean csv: reorder columns, drop duplicates, sort, then save
        output_filename = os.path.join(directory, q+'.csv')
        df = pd.read_csv(output_filename)
        df = df[fields].drop_duplicates().sort_values(by=sort)
        df.to_csv(output_filename, index=False)


if __name__ == '__main__':
    query('config.cfg')