import multiprocessing

bind = "127.0.0.1:8080"
workers = 2

errorlog = '/var/log/gunicorn/error.log'
accesslog = '/var/log/gunicorn/access.log'

timeout = 60
debug = True
loglevel = 'debug'
daemon = False