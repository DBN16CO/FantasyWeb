from datetime import datetime, timedelta
from League.models import League_Setting, Player_Nomination

from FantasyWeb.baseTest import BaseTestCase, add_league_member, is_on_page, add_test_player

class LeagueDraftTestCase(BaseTestCase):
	def setUp(self):
		self.response = None
		self.test_url = "/league/%s/draft" % self.league.pk

		self.login_user1()

	def prepareLeagueForDraft(self):
		draft_time = League_Setting(league=self.league, name="draft_time",
			value=str((datetime.now() - timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%S.%f')))
		draft_time.save()
		draft_per = League_Setting(league=self.league, name="draft_period", value="10")
		draft_per.save()
		nom_count = League_Setting(league=self.league, name="nominations_per_period", value="3")
		nom_count.save()

	def test001_league_draft_without_login(self):
		"""Tests how the server handles viewing the league draft history screen without first logging in"""
		add_league_member(self.user, self.league, "team1")
		self.logout_user1()
		self.helper_test_unauthenticated_page_access(self.test_url)

	def test002_league_draft_no_membership(self):
		"""Tests how the server handles viewing the league draft history screen without being a member"""
		response = self.client.get(self.test_url, follow=True)

		self.assertFalse(is_on_page(response, 'League: league_name1'))
		self.assertTrue(is_on_page(response, 'Fantasy Web - Home'))

	def test003_league_draft_page_view(self):
		"""Tests how the server handles viewing the league draft history screen without being a member"""
		owner = add_league_member(self.user, self.league, "team1")

		# Setup league with appropriate draft time
		self.prepareLeagueForDraft()

		player1 = add_test_player("testPlayer1", "PIT", "RB")
		pn1 = Player_Nomination(owner=owner, player=player1)
		pn1.save()
		player2 = add_test_player("testPlayer2", "NE", "WR")
		pn2 = Player_Nomination(owner=owner, player=player2)
		pn2.save()
		pn2.nomination_time = datetime.now() + timedelta(minutes=59)
		pn2.save()

		response = self.client.get(self.test_url, follow=True)
		self.assertTrue('bid_players' in response.context)
		self.assertEqual([{'id': 1, 'name': 'testPlayer1', 'position': 'RB', 'team': 'PIT'}],
			response.context["bid_players"])
		self.assertTrue('nomination_players' in response.context)
		self.assertEqual([{'id': 2, 'name': 'testPlayer2', 'position': 'WR', 'team': 'NE'}],
				response.context["nomination_players"])
		self.assertTrue('player_nomination_count' in response.context)
		self.assertEqual("3", response.context["player_nomination_count"])

		self.assertTrue(is_on_page(response, 'League: league_name1'))
		self.assertTrue(is_on_page(response, '<p>Draft</p>'))
		self.assertFalse(is_on_page(response, 'Commish Settings'))

		draft_nav_active = '<a class="nav-link white-text league-active" '
		draft_nav_active += 'href="/league/%s/draft">Draft</a>' % self.league.pk
		self.assertTrue(is_on_page(response, draft_nav_active))

	def test004_league_draft_page_view_as_commish(self):
		"""Tests how the server handles viewing the league draft history screen without being a member"""
		add_league_member(self.user, self.league, "team1", commish=True)
		response = self.client.get(self.test_url, follow=True)

		self.assertTrue(is_on_page(response, 'League: league_name1'))
		self.assertTrue(is_on_page(response, '<p>Draft</p>'))
		self.assertTrue(is_on_page(response, 'Commish Settings'))

		draft_nav_active = '<a class="nav-link white-text league-active" '
		draft_nav_active += 'href="/league/%s/draft">Draft</a>' % self.league.pk
		self.assertTrue(is_on_page(response, draft_nav_active))
