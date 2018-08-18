from League.models import League, League_Member
from FantasyWeb.baseTest import BaseTestCase

class LeagueStandingsTestCase(BaseTestCase):
	def setUp(self):
		self.response = None
		self.test_url = "/"

		self.login_user1()
