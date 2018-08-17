from League.models import League, League_Member
from .baseTest import BaseTestCase


class HomeTestCase(BaseTestCase):
	def setUp(self):
		self.response = None
		self.test_url = "/"

		self.login_user1()

	def helper_basic_league_return(self):
		self.assertTrue("leagues" in self.response.context, "Context does not contain 'leagues'")

	def test001_home_without_login(self):
		"""Tests how the server handles a viewing the home screen without first logging in"""
		self.logout_user1()
		self.helper_test_unauthenticated_page_access(self.test_url)

	def test002_basic_no_leagues(self):
		"""Tests that a user with no leagues receives an empty league context"""
		self.response = self.client.get(self.test_url)

		self.helper_basic_league_return()
		self.assertEqual([], self.response.context["leagues"])

	def test003_basic_one_leagues(self):
		"""Tests that a league is returned if the user is part of one"""
		new_league = League(name="test_league_1", owner_limit=10)
		new_league.save()
		new_league_member = League_Member(league=new_league, member=self.user, team_name="user1 unique team", is_commish=True)
		new_league_member.save()

		return_league = {
			"league_id": new_league.pk,
			"league_name": "test_league_1",
			"owner_limit": 10,
			"team_name": "user1 unique team",
			"is_commish": True
		}

		self.response = self.client.get(self.test_url)

		self.helper_basic_league_return()
		self.assertEqual([return_league], self.response.context["leagues"])

		self.assertTrue("test_league_1" in str(self.response.content))
		self.assertTrue("user1 unique team (C)" in str(self.response.content), str(self.response.content))
		self.assertEqual(str(self.response.content).count("<tr>"), 2)
