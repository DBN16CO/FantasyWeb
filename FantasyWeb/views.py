import datetime
import re

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from League.models import League, League_Member, League_Setting
from .forms import UserRegistrationForm, HomePageForm, CreateLeagueForm

@login_required(login_url="/login")
def home(request):
	username = request.user.username
	user = User.objects.filter(username=username).first()
	context = {}

	# First process any forms
	if request.method == 'POST':
		context['is_form_request'] = True
		context['form_success'] = False

		form = HomePageForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			if data['form_type'] == 'create-league-form':
				form = CreateLeagueForm(request.POST)
				if form.is_valid():
					data = form.cleaned_data
					if League_Member.objects.filter(member__username=username,
													league__name=data['league_name']).first() is not None:
						context["error"] = "You are already in a league with this name"
					else:
						year = datetime.date.today().year
						league = League(name=data['league_name'], invite_link='', year_created=year)
						league.save()
						league_setting = League_Setting(league=league, name="owner_limit", value=data['num_players'])
						league_setting.save()
						league_member = League_Member(
							league=league,
							member=user,
							team_name="%s's team" % username,
							is_commish=True
						)
						league_member.save()
						context['form_success'] = True

		# If form was not valid, errors will now be within context
		context['form'] = form

	user_leagues = League_Member.objects.filter(member__username=username)
	leagues = []

	for league_db in user_leagues:
		owner_limit = League_Setting.objects.filter(league=league_db.league, name="owner_limit").first()
		if owner_limit is None:
			owner_limit = -1
		else:
			owner_limit = owner_limit.value

		lm_val = {
			"league_id": league_db.league.id,
			"league_name": league_db.league.name,
			"is_commish": league_db.is_commish,
			"team_name": league_db.team_name,
			"owner_limit": int(owner_limit)
		}
		leagues.append(lm_val)

	context["leagues"] = leagues

	return render(request, 'home.html', context=context)

def register(request):
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('login'))

	form = UserRegistrationForm(request.POST)
	if form.is_valid():
		userObj 	= form.cleaned_data
		username 	= userObj['username']
		email 		=  userObj['email']
		password 	=  userObj['password']
		confirm 	=  userObj['confirm']

		err_msg = ""
		if not (username and email and password and confirm):
			err_msg = "Please complete all fields in the form."
		elif User.objects.filter(username=username).first() is not None:
			err_msg = "Username already exists."
		elif User.objects.filter(email=email).first() is not None:
			err_msg = "Email already exists."
		elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
			err_msg = "Please enter a valid email address."
		elif  password != confirm:
			err_msg = "The password fields must match."
		elif password is None: # TO DO: Add password validation here
			pass

		if err_msg:
			context = {
				"is_register": True,
				"error": err_msg
			}
			return render(request, 'registration/login.html', context=context)

		User.objects.create_user(username, email, password)
		user = authenticate(username = username, password = password)
		login(request, user)
		return HttpResponseRedirect('/')

	context = {
		"is_register": True,
		"error": "Please complete all fields in the form."
	}
	return render(request, 'registration/login.html', context=context)
