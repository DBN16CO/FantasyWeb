import copy
from django.contrib.auth.models import User

from League.models import League, League_Member, League_Setting
from FantasyWeb.baseTest import BaseTestCase, is_on_page


class InviteTestCase(BaseTestCase):
	def setUp(self):
		self.test_url = "/invite"
		self.login_user1()

	def test001_invite_not_logged_in(self):
		"""Tests that the server properly sets a cookie for anonymous users"""
		self.logout_user1()

		response = self.client.get(self.test_url + "/invite-id")
		self.assertEquals(response.client.cookies['invite_uri'].value, "/invite/invite-id")

	def test002_invite_invalid_link(self):
		"""Tests that the server properly handles invalid link ids"""
		response = self.client.get(self.test_url + "/invalid-id")

		expected_response = "Your invite link is invalid. Did you copy-paste it correctly?"
		self.assertTrue(is_on_page(response, expected_response))

	def test003_invite_already_a_member(self):
		"""Test that the server properly handles revisiting an invite link"""

		# Link id abc123 created in baseTest setup logic
		response = self.client.get(self.test_url + "/abc123", follow=True)

		self.assertTrue(is_on_page(response, "League: league_name1"))
		self.assertTrue(is_on_page(response, "Standings"))

	def test004_invite_league_full(self):
		"""Test that the server properly handles invites for leagues that are full"""

		self.logout_user1()
		League_Member.objects.create(league=self.league,
                                     member=self.user, team_name="user1's team",
                                     is_commish=True)

		self.league_owner_limit.value = 1
		self.league_owner_limit.save()

		new_user = User.objects.create_user('user2', 'user2@email.com', 'user2pwd')
		self.login("user2", "user2pwd")

		response = self.client.get(self.test_url + "/abc123")

		expected_response = "The League is full. Please yell at the commisioner of this league."
		self.assertTrue(is_on_page(response, expected_response))

	def test005_invite_success(self):
		"""Test that the server properly handles valid invite accept requests"""
		self.logout_user1()

		new_user = User.objects.create_user('user2', 'user2@email.com', 'user2pwd')
		self.login("user2", "user2pwd")

		response = self.client.get(self.test_url + "/abc123", follow=True)

		self.assertTrue(is_on_page(response, "League: league_name1"))
		self.assertTrue(is_on_page(response, "Standings"))

	