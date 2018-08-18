from League.models import League_Member
from FantasyWeb.baseTest import BaseTestCase

class LeagueFreeAgentsTestCase(BaseTestCase):
	def setUp(self):
		self.response = None
		self.test_url = "/league/%s/free_agents" % self.league.pk

		self.login_user1()

	def test001_league_free_agents_without_login(self):
		"""Tests how the server handles viewing the league free agents screen without first logging in"""
		self.add_league_member(self.user, self.league, "team1")
		self.logout_user1()
		self.helper_test_unauthenticated_page_access(self.test_url)

	def test002_league_free_agents_no_membership(self):
		"""Tests how the server handles viewing the league free agents screen without being a member"""
		response = self.client.get(self.test_url, follow=True)
		content = str(response.content)

		self.assertFalse('League: league_name1' in content)
		self.assertTrue('Fantasy Web - Home' in content)

	def test003_league_free_agents_page_view(self):
		"""Tests how the server handles viewing the league free agents screen without being a member"""
		self.add_league_member(self.user, self.league, "team1")
		
		response = self.client.get(self.test_url, follow=True)
		content = str(response.content)

		self.assertTrue('League: league_name1' in content)
		self.assertTrue('<p>Free Agents</p>' in content)
		self.assertFalse('Commish Settings' in content)

		free_agents_nav_active = '<a class="nav-link white-text league-active" href="/league/%s/free_agents">Free Agents</a>' % self.league.pk
		self.assertTrue(free_agents_nav_active in content)

	def test004_league_free_agents_page_view_as_commish(self):
		"""Tests how the server handles viewing the league free agents screen without being a member"""
		self.add_league_member(self.user, self.league, "team1", commish=True)
		
		response = self.client.get(self.test_url, follow=True)
		content = str(response.content)

		self.assertTrue('League: league_name1' in content)
		self.assertTrue('<p>Free Agents</p>' in content)
		self.assertTrue('Commish Settings' in content)

		free_agents_nav_active = '<a class="nav-link white-text league-active" href="/league/%s/free_agents">Free Agents</a>' % self.league.pk
		self.assertTrue(free_agents_nav_active in content)
