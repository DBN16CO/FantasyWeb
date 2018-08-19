from django import forms

class UserRegistrationForm(forms.Form):
	username = forms.CharField(
		required = True,
		label = 'Username',
		max_length = 32
	)
	email = forms.CharField(
		required = True,
		label = 'Email',
		max_length = 32,
	)
	password = forms.CharField(
		required = True,
		label = 'Password',
		max_length = 32,
		widget = forms.PasswordInput()
	)
	confirm = forms.CharField(
		required = True,
		label = 'Confirm',
		max_length = 32,
		widget = forms.PasswordInput()
	)

class HomePageForm(forms.Form):
	form_type = forms.CharField(
		required = True,
		widget=forms.HiddenInput()
	)

class CreateLeagueForm(HomePageForm):
	league_name = forms.CharField(
		required = True,
		label = "league-name",
		max_length = 25
	)
	num_players = forms.IntegerField(
		required = True,
		min_value = 2,
		max_value = 32
	)
