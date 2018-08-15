from random import randint
from time import sleep

import requests
from bs4 import BeautifulSoup

def get_team_player_data():
	hdr = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)\
		 	Chrome/67.0.3396.99 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'none',
		'Accept-Language': 'en-US,en;q=0.8'
	}
	team_list = [
		"CAR", "BUF", "CHI", "CIN", "NO", "JAX", "TB", "MIA", "CLE", "NYG", "PIT", "PHI", "LA", "BAL",
		"WAS", "NE", "TEN", "GB", "HOU", "KC", "DAL", "SF", "IND", "SEA", "ATL", "NYJ", "DET", "OAK",
		"MIN", "DEN", "LAC", "ARI"
	]

	for team in team_list:
		print("Getting data for: " + team)

		team_page="<URL>" + team

		r = requests.get(team_page, headers=hdr)
		soup_page = BeautifulSoup(r.text, 'html5lib')
		table = soup_page.find("table", id="result")
		open("./teams/" + team + ".txt", "w").write(table.prettify())

		sleep(randint(3,5))

get_team_player_data()
