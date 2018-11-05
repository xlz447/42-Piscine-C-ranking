import requests
import json
import csv
import re

r = requests.post("https://api.intra.42.fr/oauth/token", data={'grant_type': 'client_credentials', 'client_id': "xxx", 'client_secret': "xxx"})
access_token = json.loads(r.text)['access_token']
print(access_token)

url = 'https://api.intra.42.fr/v2/campus/fremont/users?access_token=%s' % (access_token)
page = 1
links = []
while 1:
	f = requests.get(url + "&page=" + str(page))
	res = f.text
	if len(res) > 2:
		temp = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', res)
		links += temp
	else:
		break
	page += 1
print(len(links))

with open("urls.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in links:
        writer.writerow([val])
