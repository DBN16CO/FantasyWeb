from League.models import League, League_Member
from FantasyWeb.baseTest import BaseTestCase

class LeagueSettingsTestCase(BaseTestCase):
	def setUp(self):
		self.response = None
		self.test_url = "/league/%s/settings" % self.league.pk

		self.login_user1()

	def test001_league_settings_without_login(self):
		"""Tests how the server handles viewing the league settings screen without first logging in"""
		self.add_league_member(self.user, self.league, "team1")
		self.logout_user1()
		self.helper_test_unauthenticated_page_access(self.test_url)

	def test002_league_settings_no_membership(self):
		"""Tests how the server handles viewing the league settings screen without being a member"""
		response = self.client.get(self.test_url, follow=True)
		content = str(response.content)

		self.assertFalse('League: league_name1' in content)
		self.assertTrue('Fantasy Web - Home' in content)

	def test003_league_settings_page_view(self):
		"""Tests how the server handles viewing the league settings screen without being a member"""
		self.add_league_member(self.user, self.league, "team1")
		
		response = self.client.get(self.test_url, follow=True)
		content = str(response.content)

		self.assertTrue('League: league_name1' in content)
		self.assertTrue('<p>Settings</p>' in content)
		self.assertFalse('Commish Settings' in content)

		settings_nav_active = '<a class="nav-link white-text league-active" href="/league/%s/settings">Settings</a>' % self.league.pk
		self.assertTrue(settings_nav_active in content)

	def test004_league_settings_page_view_as_commish(self):
		"""Tests how the server handles viewing the league settings screen without being a member"""
		self.add_league_member(self.user, self.league, "team1", commish=True)
		
		response = self.client.get(self.test_url, follow=True)
		content = str(response.content)

		self.assertTrue('League: league_name1' in content)
		self.assertTrue('<p>Settings</p>' in content)
		self.assertTrue('Commish Settings' in content)

		settings_nav_active = '<a class="nav-link white-text league-active" href="/league/%s/settings">Settings</a>' % self.league.pk
		self.assertTrue(settings_nav_active in content)
