import datetime
import json
import uuid
from math import floor

from .models import League, League_Member, League_Setting, Player, Player_Contract, Player_Nomination

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

def get_all_league_members(league_id):
	return League_Member.objects.filter(league__pk=league_id)

def get_league_setting_values(league_id):
	settings_values = League_Setting.objects.filter(league__id=league_id)
	league_settings = {}
	for setting in settings_values:
		if setting.name == "draft_time":
			dt = datetime.datetime.strptime(setting.value, '%Y-%m-%d %H:%M:%S')
			league_settings[setting.name] = dt.strftime('%A, %B %-d, %Y %-I:%M %p')
		else:
			league_settings[setting.name] = setting.value

	return league_settings

def get_player_contracts(league, user):
	return Player_Contract.objects.filter(league=league, owner__member=user)

def create_new_league(user, league_name, owner_limit):
	league = League(name=league_name, invite_id=None,
		year_created=datetime.date.today().year)
	league.save()

	# Update the league's invite id
	league.invite_id = "%s%s" % (league.pk, str(uuid.uuid4()))
	league.save()

	# Set all default settings for the league
	set_league_defaults(league.pk)

	league_setting = League_Setting.objects.filter(league=league, name="owner_limit").first()
	if league_setting is None:
		league_setting = League_Setting(league=league, name="owner_limit",
			value=owner_limit)
	else:
		league_setting.value = owner_limit
	league_setting.save()
	league_member = League_Member(
		league=league,
		member=user,
		team_name="%s's team" % user.username,
		is_commish=True
	)
	league_member.save()

def set_league_defaults(league_id):
	league = League.objects.filter(id=league_id).first()

	with open('FantasyWeb/league_settings_values.json') as settings_file:
		data = json.load(settings_file)
		for name,inner_dict in data.items():
			if name == "flex":
				name = "flex_1"
			league_setting = League_Setting(league=league, name=name, value=inner_dict["default"])
			league_setting.save()

def get_league_min_max():
	league_min = {}
	league_max = {}
	with open('FantasyWeb/league_settings_values.json') as settings_file:
		data = json.load(settings_file)
		for name,inner_dict in data.items():
			if "min" in inner_dict:
				league_min[name] = inner_dict["min"]
			if "max" in inner_dict:
				league_max[name] = inner_dict["max"]

	return league_min, league_max

def get_draft_bid_and_nomination_players(league, owner):
	bid_players_list = []
	nominate_players_list = []

	draft_time = League_Setting.objects.filter(league=league, name="draft_time").first()
	draft_period = League_Setting.objects.filter(league=league, name="draft_period").first()

	if draft_time is not None and draft_period is not None:
		draft_time = datetime.datetime.strptime(draft_time.value, "%Y-%m-%dT%H:%M:%S.%f")
		minute_offset = int(floor(float(draft_period.value)))
		second_offset = int((float(draft_period.value) % 1) * 60)
		start_time = draft_time + datetime.timedelta(minutes=minute_offset * league.cur_draft_round,
											seconds=second_offset * league.cur_draft_round)
		nominate_time = draft_time + datetime.timedelta(minutes=minute_offset * (league.cur_draft_round + 1),
												seconds=second_offset * (league.cur_draft_round + 1))
		bid_players = Player_Nomination.objects.filter(owner__league=league,
												nomination_time__range=(start_time, nominate_time))
		nominate_players= Player_Nomination.objects.filter(owner=owner, nomination_time__gt=nominate_time)

		for bp in bid_players:
			player = {}
			player["id"] = bp.player.pk
			player["name"] = bp.player.name
			player["position"] = bp.player.position
			player["team"] = bp.player.team
			bid_players_list.append(player)

		for np in nominate_players:
			player = {}
			player["id"] = np.player.pk
			player["name"] = np.player.name
			player["position"] = np.player.position
			player["team"] = np.player.team
			nominate_players_list.append(player)

	return bid_players_list, nominate_players_list
