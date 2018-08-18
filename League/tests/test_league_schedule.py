from League.models import League, League_Member
from FantasyWeb.baseTest import BaseTestCase

class LeagueScheduleTestCase(BaseTestCase):
	def setUp(self):
		self.response = None
		self.test_url = "/league/%s/schedule" % self.league.pk

		self.login_user1()

	def test001_league_schedule_without_login(self):
		"""Tests how the server handles viewing the league schedule screen without first logging in"""
		self.add_league_member(self.user, self.league, "team1")
		self.logout_user1()
		self.helper_test_unauthenticated_page_access(self.test_url)

	def test002_league_schedule_no_membership(self):
		"""Tests how the server handles viewing the league schedule screen without being a member"""
		response = self.client.get(self.test_url, follow=True)
		content = str(response.content)

		self.assertFalse('League: league_name1' in content)
		self.assertTrue('Fantasy Web - Home' in content)

	def test003_league_schedule_page_view(self):
		"""Tests how the server handles viewing the league schedule screen without being a member"""
		self.add_league_member(self.user, self.league, "team1")
		
		response = self.client.get(self.test_url, follow=True)
		content = str(response.content)

		self.assertTrue('League: league_name1' in content)
		self.assertTrue('<p>Schedule</p>' in content)
		self.assertFalse('Commish Settings' in content)

		schedule_nav_active = '<a class="nav-link white-text league-active" href="/league/%s/schedule">Schedule</a>' % self.league.pk
		self.assertTrue(schedule_nav_active in content)

	def test004_league_schedule_page_view_as_commish(self):
		"""Tests how the server handles viewing the league schedule screen without being a member"""
		self.add_league_member(self.user, self.league, "team1", commish=True)
		
		response = self.client.get(self.test_url, follow=True)
		content = str(response.content)

		self.assertTrue('League: league_name1' in content)
		self.assertTrue('<p>Schedule</p>' in content)
		self.assertTrue('Commish Settings' in content)

		schedule_nav_active = '<a class="nav-link white-text league-active" href="/league/%s/schedule">Schedule</a>' % self.league.pk
		self.assertTrue(schedule_nav_active in content)
