# todo
[ ] user_views创建账号未对密码加密
[ ] juror_views未区分陪审员部门

# 项目结构
```
|-- app
|   |-- __init__.py
|   `-- user_views.py       账号API
|-- docs                    接口文档
|-- gconfig.py              gunicorn配置文件
|-- logs                    日志
|-- nginx.conf
|-- README.md
|-- requirements
|   `-- requirements.txt    python环境要求
|-- run.py                  Flask项目入口文件
|-- tests
|   `-- tests.py
`-- utils
    |-- __init__.py
    |-- db.py               数据库连接配置
    |-- ddl.sql             数据库表结构
    |-- functions.py        重用函数
```

# 后端API
```
功能            请求      URL路由
-----------  ---------  ------------------------------
测试接口      GET, POST  /api/test
 
创建用户      POST       /api/user/create
删除用户      DELETE     /api/user/drop
登录验证      POST       /api/user/login
修改用户信息  PUT        /api/user/modify
查询用户列表  GET        /api/user/query/<string:token>
```

## 查看项目url路由
```
FLASK_APP=/data/pyweb/juror-server/run.py flask routes
```

# gunicorn运行Flask项目
```
nohup gunicorn -c /data/pyweb/juror-server/gconfig.py run:app >> /data/pyweb/juror-server/logs/gunicorn-run.log &
```

