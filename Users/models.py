from django.db import models

class User(models.Model):
	username 	= models.CharField(max_length=25, unique=True)
	email		= models.EmailField()
	password	= models.CharField(max_length=25)

	def __str__(self):
		return self.username
