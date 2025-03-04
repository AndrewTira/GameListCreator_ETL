import os
import pyodbc
import regex as re



username = os.environ['SQL_USER']
password = os.environ['SQL_PASSWORD']
server = os.environ['SQL_DATABASE']
database_name = 'master'
drivers = [driver for driver in pyodbc.drivers()]
for pyodbc_driver in drivers:
            if re.search(r'SQL Server', pyodbc_driver, re.IGNORECASE):
                driver = pyodbc_driver
            else:
                break
connectionString = f'mssql+pyodbc://{username}:{password}@{server}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server'
