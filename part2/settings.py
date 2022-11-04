from os.path import dirname, abspath
import json

# global vars defined
PARENT_DIR = dirname(dirname(dirname(abspath(__file__))))

CODE_DIR = PARENT_DIR + '/code'

DATA_DIR =  PARENT_DIR + '/data'

SQL_FILE_PATH = DATA_DIR + '/part-2.sql'

SQL_FILE_PATH_QUERIES = DATA_DIR + '/queries.sql'

INPUT_DATA_FILE = DATA_DIR + '/vaccine-distribution-data.xlsx'

CREDENTIAL_FILE = CODE_DIR + '/credentials.json'

def json_import(file_path):
    with open(file_path) as f:
        data = json.load(f)
    
    return data

""" test = json_import(CREDENTIAL_FILE)['credentials']
print(test['database']) """
