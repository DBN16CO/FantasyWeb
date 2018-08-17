from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url="/login")
def get_league_standings(request, league_id):
	return render(request, 'league_standings.html')
