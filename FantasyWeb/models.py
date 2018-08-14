from django.contrib.auth.models import User
from django.db import models

class League(models.Model):
	name 		= models.CharField(max_length=25)
	owner_limit = models.IntegerField(default=10)

	def __str__(self):
		return self.name

class League_Member(models.Model):
	league 		= models.ForeignKey(League, on_delete=models.CASCADE)
	member		= models.ForeignKey(User, on_delete=models.CASCADE)
	is_commish	= models.BooleanField(default=False)

	def __str__(self):
		return self.league.name + "(" + self.member.username + ")"
