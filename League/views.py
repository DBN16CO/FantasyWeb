from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from League.league_helper import get_league_member, get_league, get_free_agents, get_player_contracts,\
							get_all_league_members, get_league_setting_values, get_league_min_max
from League.models import League_Setting


@login_required(login_url="/login")
def get_league_standings(request, league_id):
	league_member = get_league_member(request.user, league_id)
	if not league_member:
		return HttpResponseRedirect('/')

	league = get_league(league_id)
	league_members = get_all_league_members(league_id)

	context = {"league_id": league_id, "league_name": league.name,
			   "league_members": league_members,
	           "active": "standings", "is_commish": league_member.is_commish}
	return render(request, 'league_standings.html', context=context)


@login_required(login_url="/login")
def get_league_my_team(request, league_id):
	league_member = get_league_member(request.user, league_id)
	if not league_member:
		return HttpResponseRedirect('/')

	league = get_league(league_id)

	player_contracts = get_player_contracts(league, request.user)

	context = {"league_id": league_id, "league_name": league.name,
	           "active": "my_team",
	           "player_contracts": player_contracts,
	           "is_commish": league_member.is_commish}
	return render(request, 'league_my_team.html', context=context)

@login_required(login_url="/login")
def get_league_schedule(request, league_id):
	league_member = get_league_member(request.user, league_id)
	if not league_member:
		return HttpResponseRedirect('/')

	league = get_league(league_id)

	context = {"league_id": league_id, "league_name": league.name,
	           "active": "schedule", "is_commish": league_member.is_commish}
	return render(request, 'league_schedule.html', context=context)

@login_required(login_url="/login")
def get_league_free_agents(request, league_id):
	league_member = get_league_member(request.user, league_id)
	if not league_member:
		return HttpResponseRedirect('/')

	league = get_league(league_id)
	player_list = get_free_agents(league_id)

	free_agents = []
	for player in player_list:
		p = {}
		p["name"] = player.name
		p["team"] = player.team
		p["number"] = player.number
		p["position"] = player.position
		p["status"] = player.status
		p["height"] = player.height
		p["weight"] = player.weight
		p["dob"] = player.dob
		p["experience"] = player.experience
		p["college"] = player.college

		free_agents.append(p)

	context = {"league_id": league_id, "league_name": league.name, "free_agents": free_agents,
	           "active": "free_agents", "is_commish": league_member.is_commish}
	return render(request, 'league_free_agents.html', context=context)

@login_required(login_url="/login")
def get_league_trade_block(request, league_id):
	league_member = get_league_member(request.user, league_id)
	if not league_member:
		return HttpResponseRedirect('/')

	league = get_league(league_id)

	context = {"league_id": league_id, "league_name": league.name,
	           "active": "trade_block", "is_commish": league_member.is_commish}
	return render(request, 'league_trade_block.html', context=context)

@login_required(login_url="/login")
def get_league_draft_history(request, league_id):
	league_member = get_league_member(request.user, league_id)
	if not league_member:
		return HttpResponseRedirect('/')

	league = get_league(league_id)

	context = {"league_id": league_id, "league_name": league.name,
	           "active": "draft_history", "is_commish": league_member.is_commish}
	return render(request, 'league_draft_history.html', context=context)

@login_required(login_url="/login")
def get_league_forums(request, league_id):
	league_member = get_league_member(request.user, league_id)
	if not league_member:
		return HttpResponseRedirect('/')

	league = get_league(league_id)

	context = {"league_id": league_id, "league_name": league.name,
	           "active": "forums", "is_commish": league_member.is_commish}
	return render(request, 'league_forums.html', context=context)

@login_required(login_url="/login")
def get_league_settings(request, league_id):
	league_member = get_league_member(request.user, league_id)
	if not league_member:
		return HttpResponseRedirect('/')

	league = get_league(league_id)
	settings_values = get_league_setting_values(league_id)

	league_settings = {}
	for setting in settings_values:
		league_settings[setting.name] = setting.value

	context = {"league_id": league_id, "league_name": league.name, "league_settings": league_settings,
	           "active": "settings", "is_commish": league_member.is_commish}

	return render(request, 'league_settings.html', context=context)

@login_required(login_url="/login")
def get_league_commish_settings(request, league_id):
	league_member = get_league_member(request.user, league_id)
	if not league_member:
		return HttpResponseRedirect('/')

	if not league_member.is_commish:
		return HttpResponseRedirect('/league/%s' % league_id)

	league = get_league(league_id)
	league_min, league_max = get_league_min_max()

	# Process any settings updates
	if request.method == 'POST':
		if request.POST['form_type'] in ['draft-settings-form', 'roster-settings-form']:
			for setting_name in request.POST:
				league_setting_update = League_Setting.objects.filter(league=league, name=setting_name).first()

				if league_setting_update is None or setting_name not in league_min or setting_name not in league_max\
						or float(request.POST[setting_name]) < float(league_min[setting_name])\
						or float(request.POST[setting_name]) > float(league_max[setting_name]):
					continue

				league_setting_update.value = request.POST[setting_name]
				league_setting_update.save()

	settings_values = get_league_setting_values(league_id)

	league_settings = {}
	for setting in settings_values:
		league_settings[setting.name] = setting.value

	context = {"league_id": league_id, "league_name": league.name, "league_settings": league_settings,
	           "active": "commish_settings", "league_minimums": league_min, "league_maximums": league_max,
	           "invite_link": "https://fantasyfootballelites.com/invite/%s" % league.invite_id,
	           "is_commish": league_member.is_commish}
	return render(request, 'league_commish_settings.html', context=context)
