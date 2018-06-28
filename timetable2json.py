import json
from bs4 import BeautifulSoup as bs 
import os.path

import os
if not os.path.exists('TIMETABLES_JSON'):
	os.makedirs('TIMETABLES_JSON')

#Utility function
def toUpper(string):
	string = "".join(c.upper() for c in string)
	return string

departments = ['AE','AG','AR','AT','BM','BS','BT','CD','CE','CH','CL','CR','CS','CY','DE','EC','EE','EF','ES','ET','GG','GS','HS','IM','IP','MA','ME','MI','MM','MS','MT','NA','NT','PH','RD','RE','EP','RT','SL','TS','WM']
years = [2,3,4,5]

for dep in departments:
	for year in years:
		soup = 'no file'

		if(os.path.isfile(("TIMETABLES_HTML/" + dep + str(year)) + '.html')):
			f = open("TIMETABLES_HTML/" + dep + str(year) + ".html")
			soup = bs(f.read(),'html.parser')
		else:
			continue #continue over the department loop

		rows = soup.find_all('tr')

		days = ['MON','TUE','WED','THU','FRI']

		data = []

		day_id = 0

		jsonDumpData = {}
		rowsToSkip = 0
		for row in rows: #for each day
			tds = row.find_all('td') #find all courses

			if tds[0].text == 'Day Name':
				continue

			############# When 2 subjects are clubbed in one slot #################
			############# TODO: Make this work for more than 2 subjects ###########
			# print(tds[0])

			# try:
			# 	row_span_count = int(tds[0]['rowspan']) - 1

			# 	if row_span_count > 0:
			# 		row_span_count-=1
			# 		continue
			# except:
			# 	print("No rowspan exists")
			#######################################################################
			if rowsToSkip > 0:
				rowsToSkip-=1
				continue

			try:
				day_data = {}
				time = 1
				slot_data = []
				for td in tds: #for each course in the day
					# print(td.text + " " + str(len(td.text)))
					if toUpper(td.text) in days or td.text == 'Thur':
						if (int)(td['rowspan']) > 1:
							rowsToSkip = (int)(td['rowspan']) - 1
						continue
					isFreeSlot = False
					# print(len(td.text))
					if(len(td.text.strip(' ')) < 2):
						isFreeSlot = True

					for slot_time in range(int(td['colspan'])): #for duration of each course
						if(isFreeSlot):
							slot_data.append(1)
						else:
							slot_data.append(0)
					
				jsonDumpData[days[day_id]] = slot_data
				day_id+=1	

			except:
				print("Exception caught in the loop of courses over each day")

		with open('TIMETABLES_JSON/' + dep + str(year) + '.json','w') as f:
			json.dump(jsonDumpData,f)
