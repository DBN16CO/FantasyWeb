from FantasyWeb.baseTest import BaseTestCase, add_league_member, is_on_page
from League.models import Player, Player_Contract

class LeagueMyTeamTestCase(BaseTestCase):
	def setUp(self):
		self.response = None
		self.test_url = "/league/%s/my_team" % self.league.pk

		self.login_user1()

	def test001_league_my_team_without_login(self):
		"""Tests how the server handles viewing the league my team screen without first logging in"""
		add_league_member(self.user, self.league, "team1")
		self.logout_user1()
		self.helper_test_unauthenticated_page_access(self.test_url)

	def test002_league_my_team_no_membership(self):
		"""Tests how the server handles viewing the league my team screen without being a member"""
		response = self.client.get(self.test_url, follow=True)

		self.assertFalse(is_on_page(response, 'League: league_name1'))
		self.assertTrue(is_on_page(response, 'Fantasy Web - Home'))

	def test003_league_my_team_page_view(self):
		"""Tests how the server handles viewing the league my team screen without being a member"""
		add_league_member(self.user, self.league, "team1")
		response = self.client.get(self.test_url, follow=True)

		self.assertTrue(is_on_page(response, 'League: league_name1'))
		self.assertTrue(is_on_page(response, '<p>My Team</p>'))
		self.assertFalse(is_on_page(response, 'Commish Settings'))
		self.assertTrue(is_on_page(response, '<table id="qb-table"'))
		self.assertTrue(is_on_page(response, '<table id="rb-table"'))
		self.assertTrue(is_on_page(response, '<table id="wr-table"'))
		self.assertTrue(is_on_page(response, '<table id="te-table"'))
		self.assertTrue(is_on_page(response, '<table id="k-table"'))
		self.assertTrue(is_on_page(response, '<table id="def-table"'))
		self.assertTrue(is_on_page(response, '<table id="db-table"'))
		self.assertTrue(is_on_page(response, '<table id="lb-table"'))
		self.assertTrue(is_on_page(response, '<table id="dl-table"'))

		my_team_nav_active = '<a class="nav-link white-text league-active" '
		my_team_nav_active += 'href="/league/%s/my_team">My Team</a>' % self.league.pk
		self.assertTrue(is_on_page(response, my_team_nav_active))

	def test004_league_my_team_page_view_as_commish(self):
		"""Tests how the server handles viewing the league my team screen without being a member"""
		add_league_member(self.user, self.league, "team1", commish=True)
		response = self.client.get(self.test_url, follow=True)

		self.assertTrue(is_on_page(response, 'League: league_name1'))
		self.assertTrue(is_on_page(response, '<p>My Team</p>'))
		self.assertTrue(is_on_page(response, 'Commish Settings'))
		self.assertTrue(is_on_page(response, '<table id="qb-table"'))
		self.assertTrue(is_on_page(response, '<table id="rb-table"'))
		self.assertTrue(is_on_page(response, '<table id="wr-table"'))
		self.assertTrue(is_on_page(response, '<table id="te-table"'))
		self.assertTrue(is_on_page(response, '<table id="k-table"'))
		self.assertTrue(is_on_page(response, '<table id="def-table"'))
		self.assertTrue(is_on_page(response, '<table id="db-table"'))
		self.assertTrue(is_on_page(response, '<table id="lb-table"'))
		self.assertTrue(is_on_page(response, '<table id="dl-table"'))

		my_team_nav_active = '<a class="nav-link white-text league-active" '
		my_team_nav_active += 'href="/league/%s/my_team">My Team</a>' % self.league.pk
		self.assertTrue(is_on_page(response, my_team_nav_active))

	def test005_league_my_team_players_in_tables(self):
		"""Tests that one player in every position will appear in tables on page"""
		league_member = add_league_member(self.user, self.league, "team1", commish=True)

		# Add one player of every position and assign it to the user's team
		positions = ["QB", "RB", "FB", "WR", "TE", "K", "DEF", "DB", "LB", "DL"]

		for position in positions:
			player_data = {
				"name": "player_%s" % position,
				"team": "team_%s" % position,
				"number": "69",
				"position": position,
				"status": "PUP",
				"height": "4'11\"",
				"weight": "415",
				"dob": "99596",
				"experience": "3",
				"college": "fake school"
			}

			new_player = Player(**player_data)
			new_player.save()

			new_contract = Player_Contract(league=self.league, owner=league_member, player=new_player, acquired='')
			new_contract.save()

		# Get the my team page and verify every player contract shows up on the page
		response = self.client.get(self.test_url, follow=True)

		for position in positions:
			self.assertTrue(is_on_page(response, "<td>player_%s</td>" % position),
				            "Could not find player for position %s" % position)
			self.assertTrue(is_on_page(response, "<td>team_%s</td>" % position),
				            "Could not find team for position %s" % position)

		self.assertTrue(is_on_page(response, "<td>0</td>"))
		self.assertTrue(is_on_page(response, "<td>1</td>"))
