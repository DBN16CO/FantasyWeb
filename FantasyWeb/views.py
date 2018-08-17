import re

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import UserRegistrationForm
from League.models import League_Member

@login_required(login_url="/login")
def home(request):
	username = request.user.username

	#user_leagues = League_Member.objects.filter(member=username)



	return render(request, 'home.html')

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
		if username == "" or email == "" or password == "" or confirm == "":
			err_msg = "Please complete all fields in the form."
		elif User.objects.filter(username=username).first() is not None:
			err_msg = "Username already exists."
		elif User.objects.filter(email=email).first() is not None:
			err_msg = "Email already exists."
		elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
			err_msg = "Please enter a valid email address."
		elif  password != confirm:
			err_msg = "The password fields must match."
		elif password == "": # TO DO: Add password validation here
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
