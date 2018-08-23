import requests
import json
import csv
import urllib
import os

FILE_NAME_TO_OPEN = 'aug2018.csv'
FILE_NAME_TO_SAVE = 'aug2018info'

r = requests.post("https://api.intra.42.fr/oauth/token", data={'grant_type': 'client_credentials', 'client_id': "YOUR UID", 'client_secret': "YOUR SECRET"})
access_token = json.loads(r.text)['access_token']
print(access_token)

f1 = open(FILE_NAME_TO_OPEN, 'r')#----------->CHANGE name of the url file
filesize = len(f1.readlines())
f1.close()
print("File size: " + str(filesize) + "\n")

request_limit = input("How many request? do you want to do in this run?\nMax 1200/hour, resets every hour\n")
while True:
	if request_limit.isdigit() and int(request_limit) != 0:
		request_limit = int(request_limit)
		print("In this run, " + str(request_limit) + " requests will be made\n")
		break
	request_limit = input("How many requests? Give me a nonzero number!\n");
countfile = open("startingcount.txt", "r") #----------------> something fancy
temp = countfile.read()
countfile.close()
if "DONE" in str(temp).upper():
	text = input("Finished fetching all urls, Do you want to restart? yes/no\n")
	while True:
		if text.lower() == "yes" or text.lower() == "y":
			print("ok fine")
			temp = 0
			if os.path.exists(FILE_NAME_TO_SAVE):
				os.remove(FILE_NAME_TO_SAVE)
			break
		elif text.lower() == "no" or text.lower() == "n":
			print("Okay, go check ur ranking, Bye")
			exit()
		else:
			text = input("yes/no\n")
startingcount = int(temp)
print("Base on startingcount, skipping " + str(startingcount) + " users\n")
infolist = []
with open(FILE_NAME_TO_OPEN, 'r') as csvfile: #----------->CHANGE name of the url file
	rd = csv.reader(csvfile)
	curcount = 0
	reqcount = 0
	get = 0
	skip = 0
	for row in rd:
		if reqcount == request_limit: #------------------->request limit set to 100 for testing
			stc = open('startingcount.txt','w')
			print("hit request limit: " + str(reqcount) + "\n")
			stc.write(str(curcount))
			stc.close()
			break
		curcount += 1
		if curcount > startingcount: #------------------------->skip the ones already done
			if len(str(row[0])) > 33:
				url = str(row[0]) + ('?access_token=%s' % (access_token))
			else:
				url = "https://api.intra.42.fr/v2/users/" + str(row[0]) + ('?access_token=%s' % (access_token))
			f = requests.get(url)
			data = f.text #----------->data, double quotes
			status = f.status_code
			reqcount += 1
			#------------------------------this part parse users----------------------------------------
			if status is 200:
				res = json.loads(data) #-->res, single quotes
				if not res['staff?']:
					if str(res['image_url']) != "https://cdn.intra.42.fr/users/default.png":
						infolist.append(data) # here, append single or double (data or res)
						print(str(reqcount) + ":  status: " + str(status) + " user get: " + str(res['login']))
						get += 1
					else:
						print(str(reqcount) + ":  status: " + str(status) + " skip user: " + str(res['login']))
						skip += 1
				else:
					print(str(reqcount) + ":  status: " + str(status) + " skip staff: " + str(res['login']))
					skip += 1
			else:
				print(str(reqcount) + ":  status: " + str(status) + " " + str(f))
				stc = open('startingcount.txt','w')
				print("Encountered error, stopping at: " + str(curcount - 1))
				stc.write(str(curcount - 1))
				stc.close()
				break
	#-------------------------------------------------------------------------------------------
	if curcount >= filesize:
		stc = open('startingcount.txt','w')
		stc.write("DONE")
		stc.close()
with open(FILE_NAME_TO_SAVE, "a") as output:
	for val in infolist:
		output.write(val)
		output.write(",\n")
#-----this part verifies if we accidently missed someone-----#
print("In this run, " + str(reqcount) + " users processed.")
print("User logged: " + str(get))
print("User skipped: " + str(skip) + "\n")
print("Total progress: " + str(int(temp)+get+skip) + " users processed\nThis number will be stored in startingcount.txt\nNext time "  + str(int(temp)+get+skip) +  " users will be skipped\n")
