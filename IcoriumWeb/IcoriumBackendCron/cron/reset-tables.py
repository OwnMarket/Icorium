import pymssql

MSSQL_SERVER = 'icoriummasterdb.cqc4c8d1cdmf.us-west-2.rds.amazonaws.com'
MSSQL_USER = 'icouser'
MSSQL_PWD = 'D6zqZ6UXfd'
MSSQL_DB = 'Icorium'

conn = pymssql.connect(MSSQL_SERVER, MSSQL_USER, MSSQL_PWD, MSSQL_DB)        
cursor = conn.cursor()

cursor.execute("TRUNCATE TABLE tokenmarket") 
cursor.execute("TRUNCATE TABLE icolist") 
cursor.execute("TRUNCATE TABLE icorating") 
cursor.execute("TRUNCATE TABLE smithandcrown") 
cursor.execute("TRUNCATE TABLE coinschedule") 
conn.commit()
