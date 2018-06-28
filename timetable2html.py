import re
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from bs4 import BeautifulSoup as bs 
import getpass

import os
if not os.path.exists('TIMETABLES_HTML'):
	os.makedirs('TIMETABLES_HTML')

semester = "AUTUMN"
session = "2018-2019"

#As an example
ERP_TIMETABLE_URL = 'https://erp.iitkgp.ac.in/Acad/view/dept_tt1.jsp?session=' + session + '&semester=' + semester + '&course='
departments = ['AE','AG','AR','AT','BM','BS','BT','CD','CE','CH','CL','CR','CS','CY','DE','EC','EE','EF','ES','ET','GG','GS','HS','IM','IP','MA','ME','MI','MM','MS','MT','NA','NT','PH','RD','RE','EP','RT','SL','TS','WM']

driver = webdriver.Chrome('chromedriver.exe')
driver.maximize_window()
driver.get("https://erp.iitkgp.ernet.in/SSOAdministration/login.htm?sessionToken=4BD68AB998A06C5181566BB9BF079295.worker2&requestedUrl=https://erp.iitkgp.ernet.in/IIT_ERP3/")


roll_no = driver.find_element_by_id("user_id")
password = driver.find_element_by_id("password")

#Insert the answers in the quotes left empty
roll_no_text = getpass.getpass("Enter roll number : ")
password_text = getpass.getpass("Enter password : ")

roll_no.send_keys(roll_no_text)

time.sleep(1)
driver.find_element_by_class_name("row").click()
time.sleep(2)
password.send_keys(password_text)

time.sleep(3)

question = driver.find_element_by_id("answer_div").text 
print(question)
ans = getpass.getpass("Enter aswer : ")

answer = driver.find_element_by_id("answer")
answer.send_keys(ans)

#Submit the form
driver.find_element_by_xpath("//input[@class='btn btn-primary']").click()
time.sleep(2)

for dep in departments:
	print('Parsing : ' + dep + '...')
	years = [2,3,4,5]

	for year in years:
		driver.get(ERP_TIMETABLE_URL + dep + '&role=' + dep)
		#TODO : make a seperate case for dual degree
		if len(driver.find_elements_by_id('tab' + str(year))) != 0: #The course is a 5 yr course (Integrated Msc.)
			year_tab = driver.find_element_by_id('tab' + str(year)).click()
			time.sleep(5)
			driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))
			soup = bs(driver.page_source,'html.parser')

			with open("TIMETABLES_HTML/" + dep + str(year) + ".html","w") as f:
				f.write(str(soup))
# try:
# 	driver.find_element_by_id("skiplink").click()#Coz I don't yet have a voter card and some stuff they ask for
# 	time.sleep(2)
# except NoSuchElementException:
# 	pass

# driver.find_element_by_xpath("//a[@href='menulist.htm?module_id=16']").click()
# time.sleep(2)

