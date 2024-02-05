import sqlite3
import pandas as pd
import os

directory = os.getcwd()

database_path = directory + "\Databases\\"   # Store the Students data in an xlsx file in a Databases directory

os.makedirs(database_path, exist_ok=True)

database_file = database_path + "Students.db"

conn = sqlite3.connect(database_file)

c = conn.cursor()

print("Reading Excel file ------------------")
excel_path = directory + "\Databases\\"
excel_file = excel_path + "Students.xlsx"
x1 = pd.read_excel(excel_file)

print("Writing to db ------------------")
table_name = 'Students_data'
x1.to_sql(table_name, conn, if_exists='replace',index=False)

conn.commit()
conn.close()