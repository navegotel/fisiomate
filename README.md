# Fisiomate

Fisiomate is a django-based web application for physiotherapists and other health professionals
that need to manage patient data.

**The app is still in active development and not yet ready for production!**

## Setup

Setup looks something like this, depending on distro. you may set this up in your home dir:
```
	mkdir fisiomate
	cd fisiomate
	python3 -m venv env
	source env/bin/activate
	pip install django
	git clone https://github.com/navegotel/fisiomate.git
	cd fisiomate
	./manage.py makemigrations
	./manage.py migrate
	./manage.py createsuperuser
	
```

With this you have set up a basic instance. For a production employment you must:

- edit settings.py, adjust settings to your production database, set Debug to False, set a proper random key
- install gunicorn and configure the app as wsgi application
- set up nginx as reverse proxy and configure accordingly
