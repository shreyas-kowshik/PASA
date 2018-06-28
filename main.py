import json

#Input the details
dep = raw_input("Enter your deparement code  : ")
year = (int)(raw_input("Enter your year of study : "))
additional_deps =  raw_input("Enter the deparement code whose additionals you wish to take(Use MA,CS,ME for multiple depts.) : ")

#Form a list of the target departments
list_additional_deps = additional_deps.split(',')


for additional_dep in list_additional_deps: #loop over all target departments
	ADDITIONALS_PATH = 'JSON_SUBJECTS/'
	TIMETABLE_PATH = 'TIMETABLES_JSON/'

	'''
	----------- FORMAT OF SCRAPED DATA ---------
	JSON_SUBJECTS stores data of each department's additionals being offered this semester
	This data is in the form of a dictionary where every element is a dictionary for a particular course.
	Each element stores:
		SLOT
		LTP
		PROFS.
		(COURSE) NAME
		CREDITS
		SUBJECT CODE
		ROOM NUMBER 

	slots.json sotres the description of the different slots (G2,G3,etc.)
	Each slot data is a dictionary storing:
		SLOT NAME
		TIME : 
			DAY : SLOT NUMBER ARRAY
		--> Each day is divided into 9 slots of one hour each...
			8-8:55 is slot 1
			...5-5:55 is slot 9

	TIMETABLES_JSON stores data of timetable of each department based on it's year for the current semester
	AE2.json - sotres the 2nd year department timetable for Aerospace Engineering Department
	Data is stored in a dictionary: 
		DAY : binary array of free slots
		The binary array is in the form of eg. [0,0,0,0,1,1,0,0,0]
		This means that the first four slots are not free and have lectures,the fourth and fifth are free and so on
	'''

	with open(ADDITIONALS_PATH + additional_dep + '.json') as f:
		d = str(f.read())

	additionals_data = json.loads(d)

	with open(TIMETABLE_PATH + dep + str(year) + '.json') as f:
		d = str(f.read())

	student_data = json.loads(d)

	with open('slots.json') as f:
		d = str(f.read())
	slots = json.loads(d)

	# print(slots)
	########### End of I/O ##############

	################# Obtain Free Slots ###################
	free_slots = [] #Stores list of slots which are free
	for slot in slots:
		slot_name = slot['SLOT']
		timings = slot['TIME'] #Get the dictionary of slot timings from slots.json - data in form of 
		# print(timings)

		isThisSlotFree = True

		for day in timings.keys(): #iterate over each day of the slot
			student_day_data = student_data[day] #Gives binary values of free slots of the student in that day
			# print(student_data)
			for slot_in_day in timings[day]: #for each slot in the given day
				if student_day_data[slot_in_day - 1] == 0: #If the binary value at that index if 0
					isThisSlotFree = False
					break

			if isThisSlotFree == False:
				break

		if isThisSlotFree == True:
			free_slots.append(slot_name)

	# print(free_slots)
	########################################################

	# print(additionals_data)

	############ Display the additionals ###########
	possible_additionals = []

	for course in additionals_data:
		if course['SLOT'] in free_slots:
			possible_additionals.append(course)

	# print(possible_additionals)
	print("----------The Following Additionals Are Possible For You: (Dep : " + additional_dep + ")---------" +  "\n")
	for additional in possible_additionals:
		print(additional['CODE'] + " : " + additional['NAME'] + " : " + additional['SLOT'] + "\n" + additional['PROFS.'] + "\n")