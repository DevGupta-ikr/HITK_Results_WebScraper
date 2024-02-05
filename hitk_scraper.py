import os
import sqlite3
import pandas as pd
import time
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("start-maximized")

from selenium.webdriver.chrome.service import Service

# Download and store the latest version of Chrome Webdriver
driver = webdriver.Chrome(service=Service("C:/Windows/chromedriver.exe"), options=options)

directory = os.getcwd()

file_path = directory + "\\result.txt"

if os.path.isfile(file_path):
    os.remove(file_path)

f = open(file_path, "a")

s = ""   # Results website goes here
driver.get(s)

time.sleep(2)


def marks_getter(roll_number):
    
    time.sleep(1)

    roll_number_xpath = "//*[local-name()='table']/*/*[2]/*/*/*[7]/*/*[2]/*/*/*/*/*/*[local-name()='input']"

    roll = driver.find_element("xpath", roll_number_xpath)
    roll.clear() # If not cleared, old value is used for result
    roll.send_keys(roll_number)

    # Change Semester number by selecting correct xpath option value !
    semester_xpath = "//*[local-name()='table']/*/*[2]/*/*/*[7]/*/*[2]/*/*/*/*/*/*[local-name()='select']/*[8]"
    sem = driver.find_element("xpath", semester_xpath).click()

    show_result_xpath = "//*[local-name()='table']/*/*[2]/*/*/*[7]/*/*[3]/*/*[2][local-name()='input']"

    time.sleep(1)

    driver.find_element("xpath", show_result_xpath).click()
    
    if (driver.find_element("xpath", "//*[local-name()='td']")).text == "No such student exists in this database or the student has not given the particular semester exam":
        return
    else:

        time.sleep(1)

        name_xpath = "//*/*/*/*/*[local-name()='table']/*/*/*/*[@id = 'lblname']"

        name = driver.find_element("xpath", name_xpath)

        odd_sem_xpath = "//*/*/*/*/*[local-name()='table']/*/*/*/*[@id = 'lblbottom1']"

        odd_sem = driver.find_element("xpath", odd_sem_xpath)

        even_sem_xpath = "//*/*/*/*/*[local-name()='table']/*/*/*/*[@id = 'lblbottom2']"

        even_sem = driver.find_element("xpath", even_sem_xpath)

        year_sgpa_xpath = "//*/*/*/*/*[local-name()='table']/*/*/*/*[@id = 'lblbottom3']"

        year_sgpa = driver.find_element("xpath", year_sgpa_xpath)

        time.sleep(2)

        # print(name.text)
        # print(odd_sem.text)
        # print(even_sem.text)
        # print(year_sgpa.text)
        f.write(name.text)
        f.write("\n")
        f.write(odd_sem.text)
        f.write("\n")
        f.write(even_sem.text)
        f.write("\n")
        f.write(year_sgpa.text)
        f.write("\n")
    

directory = os.getcwd()

database_path = directory + "\Databases\\"
database_file = database_path + "Students.db"  # Connect to students.db for student data

conn = sqlite3.connect(database_file)

c = conn.cursor()

query = """SELECT `Autonomy Roll` FROM Students_data
        """

c.execute(query)
data = c.fetchall()

roll_list = []

for i in data:
    roll_list.append(i[0])

conn.close()

print("------ Program Starting ------")
for i in range(len(roll_list)):
    marks_getter(roll_list[i])
    driver.back()

f.close()
driver.close()
print("------ Program Ended ------")
