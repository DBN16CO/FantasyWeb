from django.contrib.auth.models import User
from django.test.client import Client
from django.test import TestCase

class BaseTestCase(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.client = Client()
		cls.user = User.objects.create_user('user1', 'user@email.com', 'user1pwd')

	@classmethod
	def tearDownClass(cls):
		pass

	def setUp(self):
		print("=====   Testing test case: " + self.id() + " =====")

	def tearDown(self):
		print("===== Finishing test case: " + self.id() + " =====")
