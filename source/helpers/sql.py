from django.db import *
import logging

def execute_sql(sql, params = []):
    cursor = connection.cursor()
    cursor.execute(sql, params)
    if sql.strip()[:10].lower().startswith('select'):
        return cursor
    else:
        logging.info("affected %d rows", cursor.rowcount)

def batch_insert(table_name, column_names, values_list):
    assert(type(column_names) == tuple)
    if len(values_list) == 0: return
    
    values_string = ",".join(str(val) for val in values_list)
    query = '''
            INSERT INTO %s (%s)
            VALUES
            %s
            ''' % (table_name , ",".join(column_names) , values_string)
    execute_sql(query)
