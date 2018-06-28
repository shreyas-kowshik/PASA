'''

Generates the HTML files of each subject


'''

from selenium import webdriver
from bs4 import BeautifulSoup as bs 
import requests
import getpass

import os

if not os.path.exists('HTML_PARSED'):
	os.makedirs('HTML_PARSED')

ERP_HOMEPAGE_URL = 'https://erp.iitkgp.ac.in/IIT_ERP3/'
ERP_LOGIN_URL = 'https://erp.iitkgp.ac.in/SSOAdministration/auth.htm'
ERP_SECRET_QUESTION_URL = 'https://erp.iitkgp.ac.in/SSOAdministration/getSecurityQues.htm'

departments = ['AE','AG','AR','AT','BM','BS','BT','CD','CE','CH','CL','CR','CS','CY','DE','EC','EE','EF','ES','ET','GG','GS','HS','IM','IP','MA','ME','MI','MM','MS','MT','NA','NT','PH','RD','RE','EP','RT','SL','TS','WM']
DEPARTMENT = 'MA'
ERP_ADDITIONAL_LIST_BASE = 'https://erp.iitkgp.ac.in/Acad/timetable_track.jsp?action=second&dept='

def get_request():
	user = getpass.getpass("Enter roll number : ")
	erp_password = getpass.getpass("Enter password : ")

	ERP_HOMEPAGE_URL = 'https://erp.iitkgp.ac.in/IIT_ERP3/'
	ERP_LOGIN_URL = 'https://erp.iitkgp.ac.in/SSOAdministration/auth.htm'
	ERP_SECRET_QUESTION_URL = 'https://erp.iitkgp.ac.in/SSOAdministration/getSecurityQues.htm'



	headers = {
	    'timeout': '20',
	    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
	}

	s = requests.Session()
	r = s.get(ERP_HOMEPAGE_URL)
	soup = bs(r.text, 'html.parser')
	sessionToken = soup.find_all(id='sessionToken')[0].attrs['value']
	r = s.post(ERP_SECRET_QUESTION_URL, data={'user_id': user},
	           headers = headers)
	secret_question = r.text
	print (secret_question)
	secret_answer = getpass.getpass("Enter the answer to the security question: ")
	login_details = {
	    'user_id': user,
	    'password': erp_password,
	    'answer': secret_answer,
	    'sessionToken': sessionToken,
	    'requestedUrl': 'https://erp.iitkgp.ac.in/IIT_ERP3',
	}
	r = s.post(ERP_LOGIN_URL, data=login_details,
	           headers = headers)
	return r,s
	

r,s = get_request()

for dep in departments:
	print("PARSING : " + dep + "...")
	r = s.get(ERP_ADDITIONAL_LIST_BASE + dep)

	f = open('HTML_PARSED/' + dep + '.html','w')
	soup = bs(r.text,'html.parser')
	f.write(str(soup))


