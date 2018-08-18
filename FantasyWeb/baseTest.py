import time

from django.contrib.auth.models import User
from League.models import League, League_Member
from django.test.client import Client
from django.test import TestCase

class BaseTestCase(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.client = Client()
		cls.user = User.objects.create_user('user1', 'user@email.com', 'user1pwd')

		cls.league = League.objects.create(name="league_name1", owner_limit=10)

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

	def login_user1(self):
		hard_coded_password = 'user1pwd'
		self.client.login(username='user1', password=hard_coded_password)

	def logout_user1(self):
		self.client.logout()

	def add_league_member(self, user, league, team_name, commish=False):
		return League_Member.objects.create(league=league, member=user, team_name=team_name, is_commish=commish)
