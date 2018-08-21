import json

from .models import League, League_Member, League_Setting, Player, Player_Contract

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

def get_league_setting_values(league_id):
	return League_Setting.objects.filter(league__id=league_id)

def set_league_defaults(league_id):
	league = League.objects.filter(id=league_id).first()

	with open('FantasyWeb/league_settings_values.json') as settings_file:
		data = json.load(settings_file)
		for name,inner_dict in data.items():
			league_setting = League_Setting(league=league, name=name, value=inner_dict["default"])
			league_setting.save()
