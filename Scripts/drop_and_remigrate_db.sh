#!/bin/bash

heroku login
rc=$?
if [ "$rc" -ne "0" ]; then
	echo "Heroku Login Failed"
	exit 1
fi

heroku pg:reset --app fantasyfootballelites --confirm fantasyfootballelites
heroku run bash -c "python manage.py migrate"