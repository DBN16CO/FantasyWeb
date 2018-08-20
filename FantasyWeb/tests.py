import copy

from League.models import League, League_Member, League_Setting
from .baseTest import BaseTestCase


class HomeTestCase(BaseTestCase):
	def setUp(self):
		self.response = None
		self.test_url = "/"

		self.login_user1()

		self.good_create_league_post_data = {
			"form_type": "create-league-form",
			"league_name": "test League 1",
			"num_players": 10
		}

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
		new_league = League(name="test_league_1", year_created=2018)
		new_league.save()
		new_league_setting = League_Setting(league=new_league, name="owner_limit", value=10)
		new_league_setting.save()
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

	def test004_create_league_invalid_data(self):
		"""Tests that forms with invalid data for creating a league are handled properly"""
		league_count = League.objects.count()

		for key in ["league_name", "num_players"]:
			bad_post_data = copy.deepcopy(self.good_create_league_post_data)
			bad_post_data.pop(key, None)

			self.response = self.client.post(self.test_url, bad_post_data)
			self.assertEqual(league_count, League.objects.count())

			self.assertTrue(self.good_create_league_post_data["league_name"] not in str(self.response.content))

	def test005_create_league_valid(self):
		"""Validates that a new league is created when proper league form data is sent"""
		league_count = League.objects.count()

		self.response = self.client.post(self.test_url, self.good_create_league_post_data)

		self.assertEqual(League.objects.count(), league_count + 1)
		self.assertTrue(self.good_create_league_post_data["league_name"] in str(self.response.content))
