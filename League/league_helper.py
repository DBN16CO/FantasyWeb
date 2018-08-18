from .models import League, League_Member


def get_league(league_id):
	return League.objects.filter(pk=league_id).first()


def get_league_member(user, league_id):
	username = user.username
	league_member = League_Member.objects.filter(member__username=username, league__pk=league_id).first()

	return league_member
