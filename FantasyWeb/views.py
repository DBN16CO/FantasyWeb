from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import UserRegistrationForm

@login_required(login_url="/login")
def home(request):
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

		if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
			return HttpResponse("Username or email already exists.")

		User.objects.create_user(username, email, password)
		user = authenticate(username = username, password = password)
		login(request, user)
		return HttpResponseRedirect('/')

	return HttpResponse("Register not yet implemented.")
