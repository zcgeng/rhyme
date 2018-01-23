alias 'uwsgi=/usr/local/python3/bin/uwsgi'
uwsgi --stop ./uwsgi.pid;
sleep 1;
uwsgi --ini uwsgi_conf.ini -d ./uwsgi.log --uid www --pidfile uwsgi.pid;
