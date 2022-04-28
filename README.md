# test_228
Yet another test for job interview
## Installation
### Windows 

```
python -m venv env
.\env\Scripts\activate
pip install Django
```

#### In case of db errors:

```
pythom manage.py makemigrations
python manage.py makemigrations blog
python manage.py migrate
python manage.py createsuperuser
```

### Linux (Ubuntu) - test server
1) install python 3.9.7 or higher (Already shipped for default Ubuntu)
2) install git 
`sudo apt install git`
3) clone repo
`git clone https://github.com/maxim-kocheganov/test_228.git`
4) `cd testBoEn`
5) install python venv (Ubuntu way)
`sudo apt install python3.9-venv`
6) create environment in new foldier .venv
`python3 -m venb .env`
7) apply environment
`source .env/bin/activate`
8) install requirements
`pip3 install -r requirements.txt`
9) goto projects foldier
`cd exeldb`
10) do migrations
```python3 manage.py makemigrations
python manage.py makemigrations blog
```
`python3 manage.py migrate`
11) run test server on localhost
`python3 manage.py runserver`

### linux (Ubuntu) - production
Do everuthing as priviously done, exept running test server and using embeded DB (10 and 11 steps)

12) apply updates 
`sudo apt apdate`, `sudo apt upgrade`
13) install Postresql `sudo apt install postgresql`
14) check it's installation
```
sudo systemctl is-active postgresql
sudo systemctl is-enabled postgresql
sudo systemctl status postgresql
```
15) confirm readiness
`sudo pg_isready`
16) log in as pq user and run shell
```
sudo su - postgres
psql
```
17) create user and db (place your user/pass instead of admin and pass)
```
CREATE USER admin WITH PASSWORD 'pass';
CREATE DATABASE test;
GRANT ALL PRIVILEGES ON DATABASE test to admin;
\q
```
18) exit from user
`exit`
19) alternatively - setup pgadmin4 (google for yourself)
20) open exeldb/settings.py and connect your database (instead of default DATABASES)
```
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql',
        'NAME': 'test',
        'USER' : 'admin',
        'PASSWORD':'pass',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
```
21) do migrations
`python3 manage.py makemigrations`
`python manage.py makemigrations blog`
`python3 manage.py migrate`
22) install Apache and it's module
`sudo apt install apache2 libapache2-mod-wsgi-py3`
23) configure Django hosts in exeldb/settings.py Use your ip or host instead
`ALLOWED_HOSTS = ["127.0.0.1", "another ip"]`
24) configure Django static in exeldb/settings.py
```
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
```
25) change exeldb/settings.py secret
```
SECRET_KEY = 'random instead'
```
26) turn off debug mode in  exeldb/settings.py
`DEBUG = False`
27) Create Django's superuser
`python3 manage.py createsuperuser`
28) Collect project's static
`python3 manage.py collectstatic`
29) Change /etc/apache2/sites-available/000-default.conf to
```
<VirtualHost *:80>
	Alias /static /home/user/testBoEn/exeldb/static
	<Directory /home/user/testBoEn/exeldb/static>
		Require all granted
	</Directory>

	<Directory /home/user/testBoEn/exeldb/exeldb>
		Require all granted
	</Directory>

	WSGIDaemonProcess exeldb python-home=/home/user/testBoEn/.env python-path=/home/user/testBoEn/exeldb
	WSGIProcessGroup exeldb
	WSGIScriptAlias / /home/user/testBoEn/exeldb/exeldb/wsgi.py

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
30) check config
```
sudo apache2ctl configtest
```
31) reload apache
`sudo systemctl restart apache2`
32) go to /home/user/testBoEn/exeldb and create a dir `media`
```
cd /home/user/testBoEn/exeldb
mkdir media
chmod 777 media
```
33) ....
34) PROFIT!!!