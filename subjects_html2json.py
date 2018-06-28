'''

Generates the json files for the parsed HTML files


'''

from bs4 import BeautifulSoup as bs 
import re
import json

import os
if not os.path.exists('JSON_SUBJECTS'):
	os.makedirs('JSON_SUBJECTS')

departments = ['AE','AG','AR','AT','BM','BS','BT','CD','CE','CH','CL','CR','CS','CY','DE','EC','EE','EF','ES','ET','GG','GS','HS','IM','IP','MA','ME','MI','MM','MS','MT','NA','NT','PH','RD','RE','EP','RT','SL','TS','WM']


for dep in departments:
	print("Starting : " + dep + "...")
	f = open("HTML_PARSED/" + dep + ".html","r")

	soup = bs(f,'html.parser')

	rows = soup.find_all('tr')
	# rows = soup.find_all('td',text = re.compile(r"^AE[0-9]"))

	valid_sub_codes = soup.find_all(text = re.compile(r"^" + dep + "[0-9]"))
	valid_sub_codes = [code.encode('ascii') for code in valid_sub_codes]

	data = []

	for row in rows:
		tds = row.find_all('td')
		if len(tds) < 1:
			continue
		first_data = tds[0].text
		if first_data not in valid_sub_codes:
			continue
		elif len(tds) < 7:
			continue
		elif tds[6].text in valid_sub_codes:
			continue
		else:
			json_text =  {
				"CODE":tds[0].text.encode('ascii'),
				"NAME":tds[1].text.encode('ascii'),
				"PROFS.":tds[2].text.encode('ascii'),
				"LTP":tds[3].text.encode('ascii'),
				"CREDITS":tds[4].text.encode('ascii'),
				"SLOT":tds[5].text.encode('ascii'),
				"ROOM":tds[6].text.encode('ascii')
			}

			data.append(json_text)
		# print(first_data.text)
		# print(len(tds))

	with open('JSON_SUBJECTS/' + dep + '.json','w+') as f:
		json.dump(data,f)
#Read
# with open('AE.json','r+') as f:
# 	d = str(f.read())

# j = json.loads(d)
