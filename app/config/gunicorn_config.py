import os
import logging
import datetime
from gunicorn.glogging import Logger


class CustomLogger(Logger):

    def setup(self, cfg):
        super().setup(cfg)
        logger = logging.getLogger("gunicorn.access")
        logger.addFilter(HealthCheckFilter())

    def now(self):
        return datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')


class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        return 'GET /health-check/' not in record.getMessage()


logger_class = CustomLogger

access_log_format = '%({x-real-ip}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
accesslog = "logviewer/gunicorn.log"
bind = "0.0.0.0:" + os.environ.get("CONTAINER_PORT")
capture_output = True  # Capture stdio
enable_stdio_inheritance = True  # Django errors from stderr to error log
errorlog = "logviewer/error.log"
graceful_timeout = 3600
keep_alive = 3600
log_level = "debug"
pid = "partywiki.pid"
threads = 2
timeout = 3600
workers = os.environ.get("UWSGI_WORKERS")
