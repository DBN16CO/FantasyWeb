from django.contrib.auth.models import Permission, User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
	if request.user.is_authenticated:
		return render(request, 'home.html')
	else:
		return HttpResponseRedirect(reverse('login'))
