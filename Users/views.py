from django.contrib.auth.models import Permission, User
from django.http import HttpResponse


def index(request):
	if request.user.is_authenticated:
		return HttpResponse("Welcome %s!".format(request.user.username))
	else:
		return HttpResponse("Please log in first.")
