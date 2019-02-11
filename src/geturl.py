import requests
import json
import csv
import re

r = requests.post("https://api.intra.42.fr/oauth/token", data={'grant_type': 'client_credentials', 'client_id': "", 'client_secret': ""})
access_token = json.loads(r.text)['access_token']
print(access_token)

url = 'https://api.intra.42.fr/v2/campus/fremont/users?access_token=%s' % (access_token)
page = 1
links = []
ref = []
while 1:
	f = requests.get(url + "&page=" + str(page))
	res = f.text
	if len(res) > 2:
		temp = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', res)
		links += temp
		print("Got " + str(len(temp)) + " links from page " + str(page))
	else:
		break
	page += 1
print("Total links: " + str(len(links)))

print("\nReading old links from file...")
with open('../csvfiles/allurls.csv', 'r') as f:
  reader = csv.reader(f)
  temp = list(reader)
for i in temp:
	ref += i

print("\nFinding new links")
unique = list(set(links) - set(ref))
print(str(len(unique)) + "new links found")
print("Storing new and all links to file")

with open("../csvfiles/allurls.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in links:
        writer.writerow([val])

with open("../csvfiles/newurls.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in unique:
        writer.writerow([val])