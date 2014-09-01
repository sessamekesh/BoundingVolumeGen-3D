##### SORT list of genes by score #####
def Sort(myList):
	sorted = True
	x = 0
	for i in range(0, len(myList)):
		x = i
		for j in range(i, len(myList)):
			if myList[j][1] >= myList[x][1]:
				x = j
				sorted = False
		temp = myList[x]
		myList[x] = myList[i]
		myList[i] = temp
		if sorted is True:
			return
		else:
			sorted = True

def secondsToElapsed(time):
	time = int(time)

	# First, shave off number of seconds:
	nSeconds = time % 60
	time = int(time / 60)

	# Next, shave off number of minutes:
	nMinutes = time % 60
	time = int(time / 60)

	# Next, shave off number of hours:
	nHours = time % 24
	time = int(time / 24)

	# Next, shave off number of days:
	nDays = time % 7
	time = int(time / 7)

	# Finally, shave off weeks:
	nWeeks = int(time)

	# Output based on what we have:
	toReturn = "Elapsed Time: "
	if(nWeeks > 0):
		toReturn += str(nWeeks)
		toReturn += " Weeks, " if nWeeks > 1 else " Week, "
	if(nDays > 0):
		toReturn += str(nDays) 
		toReturn += " Days, " if nDays > 1 else " Day, "
	if(nHours > 0):
		toReturn += str(nHours) + ":"
	if(nMinutes > 0):
		toReturn += str(nMinutes) + ":"
		toReturn += str(nSeconds) + "\n"
	else:
		toReturn += str(nSeconds) + " seconds\n"

	return toReturn