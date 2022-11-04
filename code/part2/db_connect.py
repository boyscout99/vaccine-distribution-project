import psycopg2
from psycopg2 import Error, ProgrammingError
import pandas as pd
import re

# join strings for pasing bind variables into sql queries
def bind_string(number_of_columms):
    list = ["%s" for i in range(number_of_columms)]
    str = ", "
    return str.join(list)


class Postgres(object):

    # connect to db
    def connect(self, host_name, port, database, user, password):
        try:
            self.connection = psycopg2.connect(
                database= database,
                user=user,    
                password=password, 
                host=host_name, 
                port=port
            )
            self.cursor = self.connection.cursor()
            print("PostgreSQL server information")
            print(self.connection.get_dsn_parameters(), "\n")
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    # disconnect from db
    def disconnect(self):
        if(self.connection):
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")
    
    # execute a single query
    def execute_single_sql(self, sql, bindvars=None, commit=False, return_df=False):
        try:
            if bindvars is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, bindvars)
            if return_df:
                col_names = [row[0] for row in self.cursor.description]
                df = pd.DataFrame(self.cursor.fetchall(), columns=col_names)
                return df
        except (Exception, Error) as e:
            self.connection.rollback()
            raise

        if commit:
            self.connection.commit()
        
    # execute whole file - used for queries that must be committed for example: create trigger, create table, alter tables, create procedure..
    def execute_file(self, file_path=None):
        if file_path is None:
            print("File path must be passed")
        else:
            try:
                sql_file = open(file_path, 'r')
                self.cursor.execute(sql_file.read())
                print("File executed")
            except (Exception, Error) as e:
                raise
    
    # execute file with queries in it and return a dict that contains queries and index of the queries in the file
    def execute_queries(self, file_path=None):
        if file_path is None:
            print("File path must be passed")
        else:
            # skip lines with -- and split blocks of sqls by ;
            full_sql = ''
            for line in open(file_path):
                li=line.strip()
                if not li.startswith("--"):
                    full_sql += li
            sql_commands = re.split(r';', full_sql)
            sql_commands= [sql.replace('\n', '') for sql in sql_commands]

            try:
                results = {}
                index = 0
            
                for sql_command in sql_commands:
                    # execute queries that can return results and return df
                    if sql_command.lower().startswith('select') or sql_command.lower().startswith('with'):
                        df = self.execute_single_sql(sql_command,return_df=True)
                        results[index] = df
                        index += 1
                    elif len(sql_command) == 0: 
                        continue
                    else:
                    # execute small queries i.e. update set while querying
                        df = self.execute_single_sql(sql_command,commit=True)
                return results
            except (Exception, Error) as e:
                pass                                                                                                                                                                                
    
    # insert data
    def execute_insert(self, df=None, sql_table=None):
        if df is None or sql_table is None:
            print("All parameters must be passed.")
        else:
            try: 
                # get amount of columns that we define in our tables
                sql_table = sql_table.lower()
                self.execute_single_sql('select count(*) as column_count from information_schema."columns" where table_schema = \'public\' and table_name = %s', (sql_table,))
                sql_cols = self.cursor.fetchone()[0]

                # insert only the first amount of columns that we define
                sql = "insert into " + sql_table + " values(" + bind_string(int(sql_cols)) + ")"

                # truncate table
                trunc_sql = 'truncate table ' + sql_table + ' cascade'
                self.execute_single_sql(trunc_sql)

                df = df[df.columns[:sql_cols]]
                
                for i in range(len(df.index)):
                    self.execute_single_sql(sql, df.values.tolist()[i], commit=True)
                
            except (Exception, Error) as e:
                raise

    # return cursor for unexpected use            
    def get_cursor(self):
        return self.cursor
