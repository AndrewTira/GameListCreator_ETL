import os
import pyodbc
import regex as re
from sqlalchemy import create_engine

user = os.environ['SQL_USER']
password = os.environ['SQL_PASSWORD']
database_name = os.environ['SQL_DATABASE']
drivers = [driver for driver in pyodbc.drivers()]
for pyodbc_driver in drivers:
            if re.search(r'SQL Server', pyodbc_driver, re.IGNORECASE):
                driver = pyodbc_driver
            else:
                break


connection_string = f"mssql+pyodbc://{user}:{password}@host:1433/{database_name}?driver={driver}"
engine = create_engine(connection_string)