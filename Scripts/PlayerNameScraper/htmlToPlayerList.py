import codecs
import os

from bs4 import BeautifulSoup
from League.models import Player

team_directory = "./Scripts/PlayerNameScraper/teams"
directory = os.fsencode(team_directory)

header_mapping = {
	'No': "number",
	'Name': "name",
	'Pos': "position",
	'Status': "status",
	'Height': "height",
	'Weight': "weight",
	'Birthdate': "dob",
	'Exp': "experience",
	'College': "college"
}
headers = []
data = []

for filename in os.listdir(team_directory):
	with codecs.open(os.path.join(team_directory, filename), "r",encoding='utf-8', errors='ignore') as f:
		content = f.read()

	soup_data = BeautifulSoup(content, "html5lib")

	headers = []
	for th in soup_data.find_all("th"):
		headers.append(th.text.strip())

	print(headers)

	itr = 0
	for tr in soup_data.find_all("tr"):
		# Skip first row
		if itr == 0:
			itr += 1
			continue

		pk_data = {}
		i = 0
		for td in tr.find_all("td"):
			if headers[i] in ['Name', 'Birthdate', 'College']:
				pk_data[header_mapping[headers[i]]] = td.text.strip()
			i += 1

		i = 0
		player = Player.objects.filter(name=pk_data["name"], dob=pk_data["dob"], college=pk_data["college"]).first()
		if player is None:
			player = Player()
		player.team = filename.split(".")[0]
		for td in tr.find_all("td"):
			setattr(player, header_mapping[headers[i]], td.text.strip())
			i += 1

		player.save()

		#print(data)
