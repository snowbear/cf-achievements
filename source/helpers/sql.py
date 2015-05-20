from django.db import *
import logging

def execute_sql(sql, params = []):
    cursor = connection.cursor()
    cursor.execute(sql, params)
    if sql.strip()[:10].lower().startswith('select'):
        return cursor
    else:
        logging.info("affected %d rows", cursor.rowcount)
        return cursor.rowcount

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

def batch_update(table_name, filter_column_name, update_column_name, data):
    assert(type(data) == list)
    if len(data) == 0: return
    
    logging.info("Updating {table_name}.{update_column_name}, filtering by {filter_column_name}. {n} items are supposed to be updated"
                    .format(table_name = table_name, update_column_name = update_column_name, filter_column_name = filter_column_name, n = len(data)))
    for t in data: 
        assert(type(t) == tuple)
        assert(len(t) == 2)
    
    query = """
        UPDATE {table_name} as c
        SET {update_column_name} = s.c2
        FROM (
            SELECT * 
            FROM ( VALUES {data_string} ) AS x(c1, c2)
        )s
        WHERE c.{filter_column_name} = s.c1
    """.format(
            table_name = table_name,
            filter_column_name = filter_column_name,
            update_column_name = update_column_name,
            data_string = ",".join(["('{c1}',{c2})".format(c1 = h[0], c2 = h[1]) for h in data])
        )

    return execute_sql(query)