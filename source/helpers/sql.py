from django.db import *

def execute_sql(sql, params = []):
    cursor = connection.cursor()
    cursor.execute(sql, params)
    return cursor
