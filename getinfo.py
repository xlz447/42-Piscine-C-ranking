import requests
import json
import csv
import urllib

r = requests.post("https://api.intra.42.fr/oauth/token", data={'grant_type': 'client_credentials', 'client_id': "<SOMEGUY'S UID>", 'client_secret': "<SOMEGUY'S SECRET>"})
access_token = json.loads(r.text)['access_token']
print(access_token)

f1 = open('july2018.csv', 'r')#----------->CHANGE name of the url file
filesize = len(f1.readlines())
f1.close()
print("file size: " + str(filesize))

countfile = open("startingcount.txt", "r") #----------------> something fancy
temp = countfile.read()
countfile.close()
if str(temp) == "DONE":
	print("nothing to do, go check ur ranking")
else:
	startingcount = int(temp)
	print("skip " + str(startingcount) + " users")
	infolist = []
	with open('july2018.csv', 'r') as csvfile: #----------->CHANGE name of the url file
		rd = csv.reader(csvfile)
		curcount = 0
		reqcount = 0
		get = 0
		skip = 0
		for row in rd:
			if reqcount == 1200: #------------------->request limit set to 10 for testing
				stc = open('startingcount.txt','w')
				print("hit request limit: " + str(reqcount))
				stc.write(str(curcount))
				stc.close()
				break
			curcount += 1
			if curcount > startingcount: #------------------------->skip the ones already done
				url = "https://api.intra.42.fr/v2/users/" + str(row[0]) + ('?access_token=%s' % (access_token))
				f = requests.get(url)
				data = f.text #----------->data, double quotes
				res = json.loads(data) #-->res, single quotes
				status = f.status_code
				reqcount += 1
				#------------------------------this part parse users----------------------------------------
				if status is 200:
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
					print(str(reqcount) + ":  status: " + str(status) + " Status error!!!")
		#-------------------------------------------------------------------------------------------
		if curcount >= filesize:
			stc = open('startingcount.txt','w')
			stc.write("DONE")
			stc.close()
	with open("julyinfo", "a") as output:
		for val in infolist:
			output.write(val)
			output.write(",\n")
	#-----this part verifies if we accidently missed someone-----#
	print("In this run, " + str(reqcount) + " users processed.")
	print("Total user logged: " + str(get))
	print("Total user skipped: " + str(skip))
