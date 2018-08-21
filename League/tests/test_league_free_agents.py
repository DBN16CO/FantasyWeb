from FantasyWeb.baseTest import BaseTestCase, add_league_member, is_on_page
from League.models import Player, Player_Contract

class LeagueFreeAgentsTestCase(BaseTestCase):
	def setUp(self):
		self.response = None
		self.test_url = "/league/%s/free_agents" % self.league.pk

		self.login_user1()

	def test001_league_free_agents_without_login(self):
		"""Tests how the server handles viewing the league free agents screen without first logging in"""
		add_league_member(self.user, self.league, "team1")
		self.logout_user1()
		self.helper_test_unauthenticated_page_access(self.test_url)

	def test002_league_free_agents_no_membership(self):
		"""Tests how the server handles viewing the league free agents screen without being a member"""
		response = self.client.get(self.test_url, follow=True)

		self.assertFalse(is_on_page(response, 'League: league_name1'))
		self.assertTrue(is_on_page(response, 'Fantasy Web - Home'))

	def test003_league_free_agents_page_view(self):
		"""Tests how the server handles viewing the league free agents screen without being a member"""
		league_member = add_league_member(self.user, self.league, "team1")

		signed_player = {
			"name": "Player_name_1",
			"team": "JAX",
			"number": "69",
			"position": "FB",
			"status": "PUP",
			"height": "4'11\"",
			"weight": "415",
			"dob": "99596",
			"experience": "3",
			"college": "fake school"
		}
		displayed_player = {
			"name": "Player_name_2",
			"team": "PIT",
			"number": "7",
			"position": "QB",
			"status": "ACT",
			"height": "6'5\"",
			"weight": "240",
			"dob": "12345",
			"experience": "10",
			"college": "Miami (OH)"
		}

		# Add a player to the player table and player contract table (so not a free agent)
		player1 = Player(**signed_player)
		player1.save()
		player_contract = Player_Contract(league=self.league, owner=league_member, player=player1, acquired='')
		player_contract.save()

		# Add a player, not on contract (so a free agent)
		player2 = Player(**displayed_player)
		player2.save()

		response = self.client.get(self.test_url, follow=True)
		self.assertTrue('free_agents' in response.context)
		self.assertEqual([displayed_player], response.context["free_agents"])

		self.assertTrue(is_on_page(response, 'League: league_name1'))
		self.assertTrue(is_on_page(response, '<p>Free Agents</p>'))
		self.assertFalse(is_on_page(response, 'Commish Settings'))
		for _,v in displayed_player.items():
			self.assertTrue(is_on_page(response, v), v)

		self.assertFalse(is_on_page(response, "Player_name_1"))
		self.assertFalse(is_on_page(response, "fake school"))

		free_agents_nav_active = '<a class="nav-link white-text league-active" '
		free_agents_nav_active += 'href="/league/%s/free_agents">Free Agents</a>' % self.league.pk
		self.assertTrue(is_on_page(response, free_agents_nav_active))

	def test004_league_free_agents_page_view_as_commish(self):
		"""Tests how the server handles viewing the league free agents screen without being a member"""
		add_league_member(self.user, self.league, "team1", commish=True)
		response = self.client.get(self.test_url, follow=True)

		self.assertTrue(is_on_page(response, 'League: league_name1'))
		self.assertTrue(is_on_page(response, '<p>Free Agents</p>'))
		self.assertTrue(is_on_page(response, 'Commish Settings'))

		free_agents_nav_active = '<a class="nav-link white-text league-active" '
		free_agents_nav_active += 'href="/league/%s/free_agents">Free Agents</a>' % self.league.pk
		self.assertTrue(is_on_page(response, free_agents_nav_active))
