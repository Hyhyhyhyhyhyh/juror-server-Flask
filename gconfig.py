from gevent import monkey
monkey.patch_all()

import multiprocessing

debug = True
loglevel = 'debug'
bind = '172.18.0.1:9100'         # 提供web服务的端口，如果要跟容器通信，ip不能设置为localhost或127.0.0.1
pidfile = 'logs/gunicorn.pid'

access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"' 
errorlog          = "/data/pyweb/juror-server/logs/gunicorn_error.log"        # 错误日志文件
capture_output    = True
accesslog         = '-'

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'             # 默认为阻塞模式，最好选择gevent模式