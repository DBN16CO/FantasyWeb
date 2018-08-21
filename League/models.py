from django.contrib.auth.models import User
from django.db import models

class League(models.Model):
	name 			= models.CharField(max_length=25)
	invite_id 	= models.CharField(max_length=100, unique=True)
	year_created 	= models.IntegerField()

	def __str__(self):
		return self.name + "[" + str(self.year_created) + "]"

class League_Setting(models.Model):
	league 		= models.ForeignKey(League, on_delete=models.CASCADE)
	name 		= models.CharField(max_length=25)
	value 		= models.CharField(max_length=25)

	class Meta:
		unique_together = (('league', 'name'),)

	def __str__(self):
		return self.league.name + "[" + self.name + "] = " + self.value

class League_Member(models.Model):
	league 		= models.ForeignKey(League, on_delete=models.CASCADE)
	member		= models.ForeignKey(User, on_delete=models.CASCADE)
	team_name   = models.CharField(max_length=25)
	cap_hit 	= models.IntegerField(default=0)
	is_commish	= models.BooleanField(default=False)

	class Meta:
		unique_together = (('league', 'member'),('league', 'team_name'))

	def __str__(self):
		return self.league.name + "(" + self.member.username + ")"

class Player(models.Model):
	name		= models.CharField(max_length=50)
	team		= models.CharField(max_length=3)
	number 		= models.CharField(max_length=3)
	position 	= models.CharField(max_length=10)
	status 		= models.CharField(max_length=5)
	height 		= models.CharField(max_length=5)
	weight 		= models.CharField(max_length=5)
	dob 		= models.CharField(max_length=10)
	experience 	= models.CharField(max_length=3)
	college 	= models.CharField(max_length=50)

	class Meta:
		unique_together = (('name', 'dob', 'college'),)

	def __str__(self):
		return self.name + "(" + self.team + ") -" + self.position

class Player_Contract(models.Model):
	league 		= models.ForeignKey(League, on_delete=models.CASCADE)
	owner 		= models.ForeignKey(League_Member, on_delete=models.CASCADE)
	player 		= models.ForeignKey(Player, on_delete=models.CASCADE)
	value		= models.IntegerField(default=0)
	length 		= models.IntegerField(default=1)
	acquired 	= models.CharField(max_length=25)

	class Meta:
		unique_together = (('league', 'player'),)

	def __str__(self):
		return self.league.name + '[' + self.owner.member.username + "]: " + self.player.name + " " +\
			str(self.value) + "/" + str(self.length)

class Player_Bid(models.Model):
	owner 		= models.ForeignKey(League_Member, on_delete=models.CASCADE)
	player 		= models.ForeignKey(Player, on_delete=models.CASCADE)
	value		= models.IntegerField()
	length 		= models.IntegerField(default=1)
	bid_time	= models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = (('owner', 'player', 'bid_time'),)

	def __str__(self):
		return self.owner.league.name + '[' + self.owner.member.username + "]: " + self.player.name + " " +\
			str(self.value) + "/" + str(self.length) + " @ " + str(self.bid_time)

class Player_Nomination(models.Model):
	owner 			= models.ForeignKey(League_Member, on_delete=models.CASCADE)
	player 			= models.ForeignKey(Player, on_delete=models.CASCADE)
	nomination_time	= models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = (('owner', 'player', 'nomination_time'),)

	def __str__(self):
		return self.owner.league.name + '[' + self.owner.member.username + "]: " + self.player.name + " " +\
			" @ " + str(self.nomination_time)

class Draft_Pick(models.Model):
	league 			= models.ForeignKey(League, on_delete=models.CASCADE)
	owner 			= models.ForeignKey(League_Member, on_delete=models.CASCADE)
	player 			= models.ForeignKey(Player, on_delete=models.CASCADE)
	pick_time		= models.DateTimeField(auto_now_add=True)
	pick_round		= models.IntegerField()
	pick_position 	= models.IntegerField()

	class Meta:
		unique_together = (('league', 'pick_round', 'pick_position'),('league', 'player'))

	def __str__(self):
		return self.league.name + '[' + self.owner.member.username + "]: " + self.player.name + " " +\
			str(self.pick_round) + "." + str(self.pick_position)
