from django.contrib.auth.models import Permission, User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
	if request.user.is_authenticated:
		return HttpResponse("Welcome %s!".format(request.user.username))
	else:
		return HttpResponseRedirect(reverse('login'))
