from .baseTest import BaseTestCase

class HomeTestCase(BaseTestCase):
	def setUp(self):
		print("Testing test case:" + self.id())

		self.user = None
		self.response = None


	def test001_home_without_login(self):
		"""Tests how the server handles a viewing the home screen without first logging in"""
		#self.client.login(username='user1', password='user1pwd')
		self.response = self.client.get('/')

		print(self.response)
