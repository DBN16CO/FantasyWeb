from FantasyWeb.baseTest import BaseTestCase, add_league_member, is_on_page
from League.models import League_Setting

class LeagueSettingsTestCase(BaseTestCase):
	def setUp(self):
		self.response = None
		self.test_url = "/league/%s/settings" % self.league.pk

		self.login_user1()

	def test001_league_settings_without_login(self):
		"""Tests how the server handles viewing the league settings screen without first logging in"""
		add_league_member(self.user, self.league, "team1")
		self.logout_user1()
		self.helper_test_unauthenticated_page_access(self.test_url)

	def test002_league_settings_no_membership(self):
		"""Tests how the server handles viewing the league settings screen without being a member"""
		response = self.client.get(self.test_url, follow=True)

		self.assertFalse(is_on_page(response, 'League: league_name1'))
		self.assertTrue(is_on_page(response, 'Fantasy Web - Home'))

	def test003_league_settings_page_view(self):
		"""Tests how the server handles viewing the league settings screen without being a member"""
		add_league_member(self.user, self.league, "team1")
		setting1 = League_Setting(league=self.league, name="property1", value="value1")
		setting1.save()
		setting2 = League_Setting(league=self.league, name="property2", value="value2")
		setting2.save()
		expected_league_settings = League_Setting.objects.filter(league=self.league)

		response = self.client.get(self.test_url, follow=True)

		self.assertTrue('league_settings' in response.context)
		for ls in expected_league_settings:
			self.assertTrue(ls.name in response.context['league_settings'])
			self.assertEqual(ls.value, response.context['league_settings'][ls.name])

		self.assertTrue(is_on_page(response, 'League: league_name1'))
		self.assertTrue(is_on_page(response, '<p>Settings</p>'))
		self.assertFalse(is_on_page(response, 'Commish Settings'))

		settings_nav_active = '<a class="nav-link white-text league-active" '
		settings_nav_active += 'href="/league/%s/settings">Settings</a>' % self.league.pk
		self.assertTrue(is_on_page(response, settings_nav_active))

	def test004_league_settings_page_view_as_commish(self):
		"""Tests how the server handles viewing the league settings screen without being a member"""
		add_league_member(self.user, self.league, "team1", commish=True)
		response = self.client.get(self.test_url, follow=True)

		self.assertTrue(is_on_page(response, 'League: league_name1'))
		self.assertTrue(is_on_page(response, '<p>Settings</p>'))
		self.assertTrue(is_on_page(response, 'Commish Settings'))

		settings_nav_active = '<a class="nav-link white-text league-active" '
		settings_nav_active += 'href="/league/%s/settings">Settings</a>' % self.league.pk
		self.assertTrue(is_on_page(response, settings_nav_active))
