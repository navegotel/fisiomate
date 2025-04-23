# Fisiomate

Fisiomate is a django-based web application for physiotherapists and other health professionals
that need to manage patient data.

**The app is still under heavy development and not yet ready for production!**

## Setup

The setup looks something like this, depending on your distro. 
On Debian or Ubunto you may set up a development environment as follows:
```
mkdir devel
cd devel
sudo apt install python3.11-venv
python3 -m venv env
source env/bin/activate
pip install django
pip install Pillow
pip install markdown
pip install markdown_checklist
pip install django-markdownify
git clone git@github.com:navegotel/fisiomate.git
cd fisiomate
./manage.py createsuperuser
./manage.py makemigrations tfgcore
./manage.py makemigrations tfgcash
./manage.py migrate
	
```

With this you have set up a basic instance. For a production employment you must:

- edit settings.py, adjust settings to your production database, set Debug to False, set a proper random key
- install gunicorn and configure the app as wsgi application
- set up nginx as reverse proxy and configure accordingly
