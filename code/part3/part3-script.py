from sqlalchemy import create_engine

from settings import CREDENTIAL_FILE, json_import
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def main():
    # get credentials
    credentials = json_import(CREDENTIAL_FILE)['credentials']

    # connect using sqlalchemy engine
    conn_str = 'postgresql+psycopg2://'+ credentials['user'] +':' + credentials['password_parsed'] + '@' + credentials['host'] +'/' + credentials['database']
    
    engine = create_engine(conn_str)
    conn = engine.connect()
    
    # Display all the rows
    pd.set_option('display.max_rows', None)
    
    # question 1
    print("####################### Q1 #######################")
    conn.execute('drop table if exists patientsymptom;')
    patient_symptom = pd.read_sql_query('select ssno, name, dob as dateofbirth, gender , symptom, date as diagnosisdate from patient join symptomconsultation on patient.ssno = symptomconsultation.patient;', conn)
    patient_symptom.to_sql('patientsymptom', con=conn, index=True, if_exists='replace')
    print(patient_symptom.head)


    # question 2
    print("####################### Q2 #######################")
    q2_sql = " ".join(["with t1 as (","select","ssno as patientssNo,","v.date,","b.type as vaccinetype","from","vaccinatedat v","inner join vaccinationevent v2 on","v.date = v2.date","and v.place = v2.place","inner join batch b on","v2.batchid = b.batchid),","t2 as (","select","patientssNo,","min(date) as date1,","case","when count(*) = 1 then null","when count(*) = 2 then max(date)","end date2","from","t1","group by","patientssNo","order by","patientssNo),","t3 as (","select","t1.patientssNo,","date1,","vaccinetype as vaccinetype1,","date2","from","t1","inner join t2 on","t1.patientssNo = t2.patientssNo","and t1.date = t2.date1),","t4 as (","select","t3.patientssNo,","date1,","vaccinetype1,","date2,","t1.vaccinetype as vaccinetype2","from","t1","inner join t3 on","t1.patientssNo = t3.patientssNo","and t1.date = t3.date2)","select","t3.patientssNo,","t3.date1,","t3.vaccinetype1,","t4.date2,","t4.vaccinetype2","from","t3","full outer join t4 on","t3.patientssNo = t4.patientssNo","and t3.date1 = t4.date1;"])

    patient_vaccine_info = pd.read_sql_query(q2_sql, conn)
    print(patient_vaccine_info)
    patient_vaccine_info.to_sql('patientvaccineinfo', con=conn, index=True, if_exists='replace')
    
    # question 3
    print("####################### Q3 #######################")
    patient_symptom_female = pd.read_sql_query('select * from patientsymptom p where p.gender = \'F\';', conn)
    patient_symptom_male = pd.read_sql_query('select * from patientsymptom p where p.gender = \'M\';', conn)

    sql_query_to_answer_q3f=" ".join(["with f as (","select * from patientsymptom p where p.gender = 'F')","select symptom, count(*) as symptomcount","from f","group by symptom","order by symptomcount DESC;"])
    print("> FEMALE:")
    print(pd.read_sql_query(sql_query_to_answer_q3f, conn).head())
    # in female patients, the most frequently experienced symptoms are...
    # 1. muscle ache    8
    # 2. headache       7
    # and three-way tie for 3.
    #   feelings of illness	4
    #   fever	            4
    #   joint pain      	4

    sql_query_to_answer_q3m=" ".join(["with m as (","select * from patientsymptom p where p.gender = 'M')","select symptom, count(*) as symptomcount","from m","group by symptom","order by symptomcount DESC;"])
    print("> MALE:")
    print(pd.read_sql_query(sql_query_to_answer_q3m, conn).head())
    # in male patients, the most frequently experienced symptoms are...
    # 1. joint pain	    10
    # 2. muscle ache	7
    # and a tie for 3.
    #   fever       6
    #   headache	6

    # question 4
    print("####################### Q4 #######################")
    sql_query_to_answer_q4 = " ".join(["select","*,","case","when date_part('year', AGE(dob))>60 then '60+'","when date_part('year', AGE(dob))>40 then '40-60'","when date_part('year', AGE(dob))>20 then '20-40'","when date_part('year', AGE(dob))>10 then '10-20'","when date_part('year', AGE(dob))>0 then '0-10'","end ageGroup","from patient;"])

    patient_age_group_df = pd.read_sql_query(sql_query_to_answer_q4, conn)
    # print(patient_age_group_df.head)
    
    # ... we are almost done! you got this guys :-) ...
    # question 5 
    print("####################### Q5 #######################")
    sql_query_to_answer_q5 = "SELECT ssNo, count(*) as VaccinationStatus FROM Vaccinatedat GROUP BY ssNo"
    df_q5 = pd.read_sql_query(sql_query_to_answer_q5, conn)
    vaccination_status_df = pd.merge(patient_age_group_df, df_q5, on="ssno", how="outer")
    vaccination_status_df.fillna('0', inplace=True)
    vaccination_status_df = vaccination_status_df.astype({'vaccinationstatus':'int'})
    print(vaccination_status_df.head)
    print(vaccination_status_df.to_latex(index=False))
    
    # Question 6
    print("####################### Q6 #######################")
    age_group_str = ['0-10', '10-20', '20-40', '40-60', '60+']
    # Age group 0-10
    vax_status_df = vaccination_status_df[["agegroup", "vaccinationstatus"]].where(vaccination_status_df['agegroup'] == age_group_str[0]).dropna()
    vax_status_df_count = vax_status_df.groupby('vaccinationstatus').count()
    total = vax_status_df_count.sum()
    old_vax_status_df_perc = vax_status_df_count.div(total)
    
    for age_group in age_group_str[1:]:
       vax_status_df = vaccination_status_df[["agegroup", "vaccinationstatus"]].where(vaccination_status_df['agegroup'] == age_group).dropna()
       vax_status_df_count = vax_status_df.groupby('vaccinationstatus').count()
       total = vax_status_df_count.sum()
       new_vax_status_df_perc = vax_status_df_count.div(total)
       # merge old and new dataframes
       old_vax_status_df_perc = pd.merge(old_vax_status_df_perc, new_vax_status_df_perc, on="vaccinationstatus", how="outer")
       
    old_vax_status_df_perc.columns = age_group_str
    vaxstatus_by_agegroup_df = old_vax_status_df_perc.fillna(0)
    print(vaxstatus_by_agegroup_df.head)
    
    
    # Question 7
    print("####################### Q7 #######################")
    # Merge PatientSymptoms and PatientVaccineInfo on ssNo
    patient_symptom_freq_df = pd.merge(patient_symptom, patient_vaccine_info, how='left', left_on='ssno', right_on='patientssno')
    patient_symptom_freq_df = patient_symptom_freq_df[['ssno', 'symptom', 'diagnosisdate', 'date1', 'vaccinetype1', 'date2', 'vaccinetype2']]
    # Remove patients that have symptoms and are not vaccinates (e.g no date1, vaccinetype1)
    patient_symptom_freq_df = patient_symptom_freq_df[patient_symptom_freq_df['date1'].notna()]
    # Remove patients who have been vaccinated but with symptoms prior to a vaccine dose
    # The condition > is because the date format is string therefore 2000-01-10 > 2000-01-20, an improvement could be to use datetime
    patient_symptom_freq_df = patient_symptom_freq_df[patient_symptom_freq_df.diagnosisdate > patient_symptom_freq_df.date1]
    # Leave only the vaccine causing the symptom
    # Iterate over the rows
    df = patient_symptom_freq_df
    for ind in df.index:
        if not pd.isnull(df.at[ind, 'date2']): #if there is a second dose
            if df.at[ind, 'diagnosisdate'] >= df.at[ind, 'date2']: #if the symptom is after the second dose
                # Substitute the second dose in the first dose
                df.loc[ind, 'vaccinetype1'] = str(df.at[ind, 'vaccinetype2'])
             
    # rename column vaccinetype1 as vaxCause
    df.rename(columns={"vaccinetype1":"vaxCause"}, inplace=True)
    patient_symptom_freq_df = df.drop(['date2', 'vaccinetype2'], axis=1)
    # Count the number of symptoms for each vaccine type
    patient_symptom_freq_df = patient_symptom_freq_df[["symptom", "vaxCause"]]
    patient_symptom_freq_df = pd.crosstab(patient_symptom_freq_df.symptom, patient_symptom_freq_df.vaxCause)
    # Compute the total amount of vaccinations for each vaccine type
    patient_vaccine_info_date1_df = patient_vaccine_info['vaccinetype1'][patient_vaccine_info['vaccinetype1'].notna()]
    patient_vaccine_info_date2_df = patient_vaccine_info['vaccinetype2'][patient_vaccine_info['vaccinetype2'].notna()]
    # Create a summation for each of the two doses
    total_col1_df = patient_vaccine_info_date1_df.value_counts()
    total_col2_df = patient_vaccine_info_date2_df.value_counts()
    # Compute the sum for each vaccine type
    totals_vax_df = total_col2_df.add(total_col1_df, fill_value = 0)
    patient_symptom_freq_df['V01'] = patient_symptom_freq_df['V01'].div(totals_vax_df.loc['V01'])
    patient_symptom_freq_df['V02'] = patient_symptom_freq_df['V02'].div(totals_vax_df.loc['V02'])
    patient_symptom_freq_df['V03'] = patient_symptom_freq_df['V03'].div(totals_vax_df.loc['V03'])
    # Replace values with strings
    df = patient_symptom_freq_df
    for ind in df.index:
        for col in df.columns:
          if df.at[ind, col] >= 0.1:
              df.loc[ind, col] = "very common"
          elif df.at[ind, col] >= 0.05 and df.at[ind, col] < 0.1:
              df.loc[ind, col] = "common"
          elif df.at[ind, col] > 0 and df.at[ind, col] < 0.05:
              df.loc[ind, col] = "rare"
              
    patient_symptom_freq_df = df.replace(0, "-")
    print(patient_symptom_freq_df)
    
    # Question 8
    print("####################### Q8 #######################")
    # Select all vaccination events
    sql_vax_event = """
    SELECT * FROM vaccinationevent
    ;
    """
    vaccinationevent_df = pd.read_sql_query(sql_vax_event, conn)
    # Find expected number of people by the batch chosen for that day
    sql_batch_amount = """
    SELECT batchid, amount FROM batch 
    ;
    """
    batch_amount_df = pd.read_sql_query(sql_batch_amount, conn)
    # Find total vaccines available on a location on that day
    sql_vax_avail = """
    SELECT SUM(amount), productiondate, expirationdate, location
    FROM batch
    GROUP BY productiondate, expirationdate, location
    ORDER BY location, productiondate, expirationdate
    ;
    """
    vax_avail_df = pd.read_sql_query(sql_vax_avail, conn)
    # Find the number of attending patients on that location and day
    sql_patients_attending = """
    SELECT date, place, count(ssno)
    FROM vaccinatedat
    GROUP BY date, place
    ;
    """
    patients_per_event_df = pd.read_sql_query(sql_patients_attending, conn)
    # Merge VaccinationEvent and Batch on batchID and select amount and find number of attending patients
    vaccination_event_batch_df = pd.merge(vaccinationevent_df, batch_amount_df, on="batchid", how="inner")
    batch_amount_patients_df = pd.merge(vaccination_event_batch_df, patients_per_event_df, on=['date', 'place'], how="outer")
    batch_amount_patients_df = batch_amount_patients_df[['date', 'place', 'amount', 'count']]
    batch_amount_patients_df = batch_amount_patients_df.rename(columns={'place':'location', 'amount':'expectedpeople', 'count':'actualpeople'}, inplace=False)
    # Merge with the total number of vaccines available on that date
    df1 = batch_amount_patients_df
    df2 = vax_avail_df
    std_df = pd.merge(df1, df2, on="location", how="right")
    std_df = std_df[(std_df.date >= std_df.productiondate) & (std_df.date <= std_df.expirationdate)]
    # Sum all vaccines available on that date
    std_df = std_df.groupby(['date','location']).sum()
    # Compute the percentage of expected people as the expected people / total available vaccines
    # Compute the percentage of actual people as the actual people / total available vaccines
    std_df['percexp'] = std_df['expectedpeople']/std_df['sum']
    std_df['percact'] = std_df['actualpeople']/std_df['sum']
    # Mean and standard deviations
    mean = std_df['percexp'].mean().round(3)
    std = std_df['percact'].std().round(3)
    perc_for_minimal_waste = mean + std
    print(f"Mean: {mean}, Standard Deviation: {std}, Percentage for Minimal Waste: {perc_for_minimal_waste}")
    
    
    # question 9
    print("####################### Q9 #######################")
    sql_query_to_answer_q9 = "SELECT * from Vaccinatedat;"
    df_q9 = pd.read_sql_query(sql_query_to_answer_q9, conn)
    df_q9.date = pd.to_datetime(df_q9.date)
    df_q9 = df_q9.groupby('date').ssno.count()
    df_q9 = df_q9.groupby(df_q9.index.day).cumsum().reset_index()
    df_q9.rename(columns={'ssno': 'vaccinated_patients'}, inplace=True)
    df_q9['date'] = df_q9['date'].dt.strftime('%d/%m/%Y')
    ax = df_q9.plot.bar(x='date', y='vaccinated_patients', rot=0)
    plt.xlabel('date')
    plt.ylabel('number of vaccinated patients')
    plt.title('Total number of vaccinated patients by date')
    plt.show()

    # question 10
    print("####################### Q10 #######################")
    result_q10 = engine.execute('SELECT t2.ssNo, Patient.name from (SELECT distinct ssNo from Vaccinatedat where '
                                'place IN(SELECT place from Vaccinationshift Where staff=\'190974-7140\') AND date <= '
                                '\'2021-05-15\' AND date >= (date(\'2021-05-15\')-interval \'10\' day)) as t2, '
                                'Patient WHERE t2.ssNo= Patient.ssNo UNION SELECT  t1.staff, Staff.name from (SELECT '
                                'distinct staff from Vaccinationshift where place IN(SELECT place from '
                                'Vaccinationshift Where staff=\'190974-7140\') AND weekday IN (SELECT weekday from '
                                'Vaccinationshift Where staff=\'190974-7140\') AND Staff !=\'190974-7140\') as t1, '
                                'Staff WHERE t1.staff=Staff.ssNo;')
    for row in result_q10:
        print(row)
    
    conn.close()

main()
