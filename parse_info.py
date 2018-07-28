import json
import csv


## read file
with open("julyinfo") as f:
	inter = f.read()

inter = "[" + inter + "{}]"
full_info = json.loads(inter)
## container for all data
all_data = []
months = ["january", "february", "march", "april", "may", "june",
"july", "august", "september", "october", "november", "december"]
## get individual data
for user_info in full_info:
	if len(user_info) is 0:
		break
	level = 0.0
	login = user_info['login']
	time = None
	if user_info['pool_month'] and user_info['pool_year']:
		time = user_info['pool_year'] + "/" + str(months.index(user_info['pool_month']) + 1)
	all_cursus = user_info['cursus_users']
	for cursus in all_cursus:
		if cursus['cursus']['id'] is 4:
			level = cursus['level']
			all_data.append((login, level, time))

def lv_cmp(e):
	return e[1]

all_data.sort(reverse = True, key = lv_cmp)

rank = 1
with open("july2018results.txt", "w") as output:
	for ppl in all_data:
		output.write(str(rank) + " ")
		if ppl[2]:
			output.write(ppl[0] + " " + str('{:5.2f}'.format(ppl[1])) + " (" + ppl[2] + ")\n")
		else:
			output.write(ppl[0] + " " + str('{:5.2f}'.format(ppl[1])) + " (Month Unknown)\n")
		rank += 1
