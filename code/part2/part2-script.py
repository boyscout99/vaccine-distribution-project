# work on part2 script here
from db_connect import Postgres
from settings import INPUT_DATA_FILE, SQL_FILE_PATH, CREDENTIAL_FILE, json_import, SQL_FILE_PATH_QUERIES
from process_raw import clean_whole_excel

def main():
    # get credentials
    credentials = json_import(CREDENTIAL_FILE)['credentials']

    # declare 'excel sheet' : 'sql tables' here
    # parent relations must be inserted first to avoid error key not found.
    data_location = {
        'VaccineType' : 'VaccineType',
        'VaccinationStations' : 'MedicalFacility',
        'Symptoms' : 'Symptom',
        'Patients' : 'Patient',
        'Manufacturer' : 'Manufacturer',
        'VaccineBatch' : 'Batch',
        'Vaccinations' : 'VaccinationEvent',
        'VaccinePatients' : 'VaccinatedAt',
        'Transportation log' : 'TransportationLog',
        'StaffMembers' : 'Staff',
        'Shifts': 'VaccinationShift',
        'Diagnosis' : 'SymptomConsultation'
    }

    # connect to database
    grp09_db = Postgres()
    grp09_db.connect(credentials['host'], credentials['port'], credentials['database'], credentials['user'], credentials['password'])
    
    # clean excel input
    print("Cleaning the data.")
    df_list = clean_whole_excel(INPUT_DATA_FILE)

    #create tables and constraints
    grp09_db.execute_file(SQL_FILE_PATH)
    
    # insert everything from Excel
    for key, val in data_location.items():
        grp09_db.execute_insert(df_list[key], val)
    print('Table inserted')

    # run queries
    """ results = grp09_db.execute_queries(SQL_FILE_PATH_QUERIES)
    print(results) """
    
    grp09_db.disconnect()

#run only when you have closed Excel
main()
