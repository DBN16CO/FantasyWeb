import re

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from League.models import League_Member
from .forms import UserRegistrationForm

@login_required(login_url="/login")
def home(request):
	username = request.user.username

	user_leagues = League_Member.objects.filter(member__username=username)
	leagues = []

	for league_db in user_leagues:
		lm_val = {
			"league_id": league_db.league.id,
			"league_name": league_db.league.name,
			"is_commish": league_db.is_commish,
			"team_name": league_db.team_name,
			"owner_limit": league_db.league.owner_limit
		}
		leagues.append(lm_val)


	context = {
		"leagues": leagues
	}

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
		if len(username) == 0 or len(email) == 0 or len(password) == 0 or len(confirm) == 0:
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

		if err_msg != "":
			context = {
				"is_register": True,
				"error": err_msg
			}
			return render(request, 'registration/login.html', context=context)

		User.objects.create_user(username, email, password)
		user = authenticate(username = username, password = password)
		login(request, user)
		return HttpResponseRedirect('/')

	return HttpResponseRedirect(reverse('login'))
