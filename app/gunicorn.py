import os

accesslog = "/var/log/access.log"
bind = "0.0.0.0:" + os.environ.get("CONTAINER_PORT")
errorlog = "/var/log/error.log"
graceful_timeout = 3600
keep_alive = 3600
log_level = "debug"
pid = "partywiki.pid"
timeout = 3600
threads = 2
workers = os.environ.get("UWSGI_WORKERS")
capture_output = True
enable_stdio_inheritance = True
