from .models import League, League_Member, Player, Player_Contract


def get_league(league_id):
	return League.objects.filter(pk=league_id).first()


def get_league_member(user, league_id):
	username = user.username
	league_member = League_Member.objects.filter(member__username=username, league__pk=league_id).first()

	return league_member

def get_free_agents(league_id):
	taken_players = Player_Contract.objects.filter(league__id=league_id).values_list('player__id', flat=True)
	free_agents = Player.objects.filter().exclude(id__in=taken_players)

	return free_agents
