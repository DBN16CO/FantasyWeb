import html.parser
import time

from django.contrib.auth.models import User
from django.test.client import Client
from django.test import TestCase
from League.models import League, League_Member, League_Setting, Player


def add_league_member(user, league, team_name, commish=False):
	return League_Member.objects.create(league=league, member=user, team_name=team_name, is_commish=commish)

def add_test_player(name, team, position):
	return Player.objects.create(name=name, team=team, number="1", position=position, status="ACT", height="5'11\"",
		weight="225", dob="8/7/87", experience="7", college="North Carolina")

def is_on_page(response, text):
	html_parser = html.parser.HTMLParser()
	unescaped = html_parser.unescape(str(response.content))
	content = str(unescaped)

	return text in content


class BaseTestCase(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.client = Client()
		cls.user = User.objects.create_user('user1', 'user@email.com', 'user1pwd')

		cls.league = League.objects.create(name="league_name1", year_created=2018, invite_id='abc123')

		cls.league_owner_limit = League_Setting(league=cls.league, name="owner_limit", value=10)
		cls.league_owner_limit.save()

		if cls is not BaseTestCase and cls.setUp is not BaseTestCase.setUp:
		   orig_setUp = cls.setUp
		   def setUpOverride(self, *args, **kwargs):
			   BaseTestCase.setUp(self)
			   return orig_setUp(self, *args, **kwargs)
		   cls.setUp = setUpOverride

	@classmethod
	def tearDownClass(cls):
		cls.user.delete()
		cls.league.delete()

	def setUp(self):
		print("=====   Testing test case: " + self.id() + " =====")
		self.startTime = time.time()

	def tearDown(self):
		t = time.time() - self.startTime
		print("===== Finishing test case: %s ===== [%.3f]" % (self.id(), t))

	def helper_test_unauthenticated_page_access(self, test_url):
		response = self.client.get(test_url, follow=True)

		self.assertTrue("login-form-link" in str(response.content))
		self.assertTrue("register-form-link" in str(response.content))

	def login(self, username, password):
		self.client.login(username=username, password=password)

	def login_user1(self):
		hard_coded_password = 'user1pwd'
		self.client.login(username='user1', password=hard_coded_password)

	def logout_user1(self):
		self.client.logout()
