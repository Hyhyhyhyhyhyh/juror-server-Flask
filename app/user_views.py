from flask import Flask, request
from flask_restful import Resource, reqparse, abort

import hashlib, sys, MySQLdb,json,base64
sys.path.insert(0, '..')
from utils import db, functions


class CreateUser(Resource):
    """创建账号
    
    TODO:password字段未来作加密处理
    
    returns:
        1000 请求成功
        1001 捕捉到异常，请求失败
        1002 userid已存在
        1003 前端参数传递不完整
        1004 权限不足
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=str, default=None)
        self.parser.add_argument('pw', type=str, default=None)
        self.parser.add_argument('name', type=str, default=None)
        self.parser.add_argument('authType', type=str, default=None)
        self.parser.add_argument('jurorId', type=str, default=None)
        self.parser.add_argument('dept_id', type=str, default=None)
        self.parser.add_argument('token', type=str, default=None)
    
    def post(self):
        data = self.parser.parse_args()
        userid_post    = data.get('id')
        password_post  = data.get('pw')
        username_post  = data.get('name')
        auth_type_post = data.get('authType')
        jurorid_post   = data.get('jurorId')
        dept_id_post   = data.get('dept_id')
        token_post     = data.get('token')
        
        conn = db.mysql_connect()
        curs = conn.cursor()
        curs.execute('set autocommit=0')
        #防SQL注入
        if userid_post is None or password_post is None or username_post is None:
            return {"code":1003,"msg":"参数传递不完整"}
        else:
            userid    = MySQLdb.escape_string(userid_post).decode('utf-8')
            password  = MySQLdb.escape_string(password_post).decode('utf-8')
            username  = MySQLdb.escape_string(username_post).decode('utf-8')
        
        if jurorid_post is None:
            jurorid = '0'
        else:
            jurorid = MySQLdb.escape_string(jurorid_post).decode('utf-8')
        
        #判断账号是否存在
        sql = "select userid from users where userid='{0}'".format(userid)
        if curs.execute (sql) != 0:
            curs.close()
            conn.close()
            return {"code":1002, "msg":"账号已存在"}


        # 根据token判断新账号的权限
        # token为空，表示用户在“注册页面”创建账号，部门id默认=0
        # token不为空，表示用户在“用户管理”页面创建账号，验证token权限
        #     auth_type<9，创建用户则创建到当前用户的部门下
        #     auth_type=9，创建用户的部门使用post传入的dept_id
        
        if token_post is None:
            auth_type = 1
            token_auth_type = 999
            dept_id = 0
        else:
            token_auth_type = functions.token_auth(token_post)
            if token_auth_type is False:
                return {"code":1003, "msg":"非法token"}
            elif int(token_auth_type) == 9:
                dept_id = int(dept_id_post)
            else:
                dept_id = int(functions.token_auth_dept(token_post))

        if auth_type != 1:
            if int(auth_type_post) > int(token_auth_type):
                return {"code":1004, "msg":"权限不足"}
            else:
                auth_type = int(auth_type_post)

        try:
            # 插入账号信息
            sql = "insert into users(userid,password,username,auth_type,jurorid,account_status,dept_id) values('{0}','{1}','{2}',{3},{4},{5},'OPEN')".format(userid,password,username,auth_type,jurorid,dept_id)
            curs.execute(sql)
            conn.commit()
            curs.close()
            conn.close()
            #构造token
            token = functions.token_encode(userid,username,auth_type,jurorid,dept_id)
            json_data = {
                "id":       userid,
                "name":     username,
                "authType": auth_type,
                "token":    token,
                "jurorId":  jurorid,
                "dept_id":   dept_id
            }
            return {"code":1000, "msg":"注册成功", "data":json_data}
        except Exception as e:
            curs.close()
            conn.close()
            return {"code":1001, "msg":str(e)}


class Login(Resource):
    """验证登录
    
    returns:
        1000 请求成功
        1001 捕捉到异常，请求失败
        1002 账号名错误
        1003 密码错误
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=str, default=None)
        self.parser.add_argument('pw', type=str, default=None)
        
    def post(self):
        data = self.parser.parse_args()
        userid_post    = data.get('id')
        password_post  = data.get('pwd')
        
        conn = db.mysql_connect()
        curs = conn.cursor()
        curs.execute('set autocommit=0')
        if userid_post is None or password_post is None:
            return {"code":1001, "msg":"参数传递不完整"}
        else:
            userid = MySQLdb.escape_string(userid_post).decode('utf-8')
            password = MySQLdb.escape_string(password_post).decode('utf-8')
        try:
            sql = "select userid from users where userid='{0}'".format(userid)
            if curs.execute(sql) == 1:  #验证账号名存在，下一步验证密码
                sql = "select userid,username,auth_type,jurorid,dept_id,unix_timestamp(last_login) from users where userid='{0}' and password='{1}'".format(userid,password)
                if curs.execute(sql) == 1:  #验证密码通过
                    result = curs.fetchone()
                    id         = str(result[0])
                    username   = str(result[1])
                    auth_type  = str(result[2])
                    jurorid    = str(result[3])
                    dept_id     = str(result[4])
                    last_login = str(result[5])
                    #更新last_login
                    sql = "update users set last_login=current_timestamp() where userid='{0}'".format(userid)
                    curs.execute(sql)
                    conn.commit()
                    curs.close()
                    conn.close()
                    #构造token
                    token = functions.token_encode(userid,username,auth_type,jurorid,dept_id)
                    json_data = {
                        "id":       userid,
                        "name":     username,
                        "authType": auth_type,
                        "token":    token,
                        "jurorId":  jurorid,
                        "dept_id":   dept_id
                    }
                    print(token)
                    return {"code":1000, "msg":"登录成功", "data":json_data}
                else:
                    curs.close()
                    conn.close()
                    return {"code":1003, "msg":"密码错误"}
            else:
                curs.close()
                conn.close()
            return {"code":1002, "msg":"账号不存在"}
        except Exception as e:
            curs.close()
            conn.close()
            return {"code":1001, "msg":str(e)}


class ModifyUser(Resource):
    """账号信息修改
    
    returns:
        1000 请求成功
        1001 捕捉到异常，请求失败
        1002 token为空
        1003 token验证不通过
        1004 权限不足
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=str, default=None)
        self.parser.add_argument('pw', type=str, default=None)
        self.parser.add_argument('name', type=str, default=None)
        self.parser.add_argument('authType', type=str, default=None)
        self.parser.add_argument('jurorId', type=str, default=None)
        self.parser.add_argument('dept_id', type=str, default=None)
        self.parser.add_argument('token', type=str, default=None)
        
    def put(self):
        data = self.parser.parse_args()
        userid_post    = data.get('id')
        password_post  = data.get('pw')
        username_post  = data.get('name')
        auth_type_post = data.get('authType')
        jurorid_post   = data.get('jurorId')
        dept_id_post   = data.get('dept_id')
        token          = data.get('token')
    
        if token is None:
            return {"code":1002, "msg":"token为空"}
        else:    #判断新账号的权限
            token_auth_type = functions.token_auth(token)
            if token_auth_type is False:
                return {"code":1003, "msg":"非法token"}

        conn = db.mysql_connect()
        curs = conn.cursor()
        curs.execute('set autocommit=0')

        #防SQL注入
        if userid_post is None or password_post is None or username_post is None or auth_type_post is None or dept_id_post is None:
            return {"code":1001, "msg":"参数传递不完整"}
        else:
            userid    = MySQLdb.escape_string(userid_post).decode('utf-8')
            password  = MySQLdb.escape_string(password_post).decode('utf-8')
            username  = MySQLdb.escape_string(username_post).decode('utf-8')
            auth_type = MySQLdb.escape_string(auth_type_post).decode('utf-8')
            dept_id    = MySQLdb.escape_string(dept_id_post).decode('utf-8')

        if jurorid_post is None:
            jurorid = '0'
        else:
            jurorid = MySQLdb.escape_string(jurorid_post).decode('utf-8')

        #不能修改把账号权限修改为比当前登录账号权限高
        if int(auth_type) > int(token_auth_type):
            return {"code":1004, "msg":"权限不足"}

        #修改用户信息
        try:
            sql = "update users set password='{0}',username='{1}',auth_type={2},jurorid={3},dept_id={5} where userid='{4}'".format(password,username,auth_type,jurorid,userid,dept_id)
            curs.execute(sql)
            conn.commit()
            curs.close()
            conn.close()
            #构造token
            token = functions.token_encode(userid,username,auth_type,jurorid,dept_id)
            json_data = {
                "id":       userid,
                "name":     username,
                "authType": auth_type,
                "token":    token,
                "jurorId":  jurorid,
                "dept_id":   dept_id
            }
            return {"code":1000, "msg":"更新成功", "data":json_data}
        except Exception as e:
            curs.close()
            conn.close()
            return {"code":1001, "msg":str(e)}


class UserList(Resource):
    """用户列表
    
    returns:
        1000 查询成功
        1001 后端代码运行出错
        1002 token为空
        1003 token验证不通过
    """
    def get(self, token, page, limit, id, authType, name):
        if token is None:       #根据token判断新账号的权限
            return {"code":1002, "msg":"token为空"}
        else:
            token_auth_type = str(functions.token_auth(token))
            token_dept_id   = functions.token_auth_dept(token)
            if token_auth_type is False or token_dept_id is False:
                return {"code":1003, "msg":"非法token"}


        #前端查询条件传递的参数
        get_page      = page
        get_limit     = limit
        get_userid    = id
        get_auth_type = authType
        get_username  = name
        
        ####### 根据前端搜索条件查询 #######
        sql = """select u.userid,u.username,u.auth_type,u.jurorid,u.created,u.last_login,u.last_modified,u.account_status,
        d.name,d.level,d.city,d.region
        from users u
        left join dept d
        on u.dept_id=d.id
        where 1=1"""
        
        try:
            """
            若get请求传入的auth_type>0 -> 只查询这个权限的用户
            若get请求传入的auth_type=0 -> 根据token里面的auth_type判断查询权限
            """
            if int(authType) > 0:
                auth_type = int(MySQLdb.escape_string(get_auth_type).decode('utf-8'))
                auth_type = " and auth_type={0} and dept_id={1}".format(auth_type,int(token_dept_id))
            elif int(get_auth_type) == 0:
                if token_auth_type == '9':
                    auth_type  = ""
                else:
                    auth_type = int(MySQLdb.escape_string(token_auth_type).decode('utf-8'))
                    auth_type  = " and auth_type<={0} and dept_id={1}".format(auth_type,int(token_dept_id))

            if get_userid is None:
                userid = ""
            elif get_userid is not None:
                userid = MySQLdb.escape_string(get_userid).decode('utf-8')
                userid = " and userid like '%{0}%'".format(userid)

            if get_username is None:
                username = ""
            elif get_username is not None:
                username = MySQLdb.escape_string(get_username).decode('utf-8')
                username = " and username like '%{0}%'".format(username)

            if get_page is None:
                if get_limit is None:    #如果查询条件传入的分页为空，则默认10行
                    limit = " limit 0,10"
                elif int(get_limit) > 0:
                    limit = MySQLdb.escape_string(get_limit).decode('utf-8')
                    limit = " limit 0,{0}".format(limit)
            elif int(get_page) > 0:
                if get_limit is None:
                    page  = MySQLdb.escape_string(get_page).decode('utf-8')
                    page  = (int(page)-1)*10
                    limit = " limit {0},10".format(page)
                elif int(get_limit) > 0:
                    page  = MySQLdb.escape_string(get_page).decode('utf-8')
                    limit = MySQLdb.escape_string(get_limit).decode('utf-8')
                    page  = (int(page)-1)*int(limit)
                    limit = " limit {0},{1}".format(page,limit)

            sql = sql + userid + username + auth_type + " order by userid" + limit
            row_count_sql = "select count(*) from users where 1=1" + userid + username + auth_type
            print(sql)
        except Exception as e:
            return {"code":1001, "msg":str(e)}
        
        #查询数据库获取用户信息列表
        conn = db.mysql_connect()
        curs = conn.cursor()
        try:
            curs.execute(sql)
            result = curs.fetchall()
            result_list = []
            for i in result:
                result_dict = {}
                result_dict['id']             = str(i[0])
                result_dict['name']           = str(i[1])
                result_dict['authType']       = str(i[2])
                result_dict['jurorId']        = str(i[3])
                result_dict['created']        = str(i[4])
                result_dict['last_login']     = str(i[5])
                result_dict['last_modified']  = str(i[6])
                result_dict['account_status'] = str(i[7])
                result_dict['dept_name']      = str(i[8])
                result_dict['dept_level']     = str(i[8])
                result_dict['dept_city']      = str(i[8])
                result_dict['dept_region']    = str(i[8])
                result_list.append(result_dict)
            #获取本次查询的总数
            curs.execute(row_count_sql)
            for i in curs.fetchone():
                row_count = i
            curs.close()
            conn.close()
            response_data = {"code":1000,"msg":"查询成功","data":result_list,"total": row_count}
            print(response_data)
            return response_data
        except Exception as e:
            curs.close()
            conn.close()
            return {"code":1001, "msg":str(e)}


class DropUser(Resource):
    """删除用户
    
    returns:
        1000 删除用户成功
        1001 后端代码运行出错
        1002 账号权限不足
        1003 token验证不通过
        1004 传入的token为空
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('token', type=str, default=None)
        self.parser.add_argument('id', type=str, default=None)
        
    def delete(self):
        data = self.parser.parse_args()
        token       = data.get('token')
        userid_post = data.get('id')
        
        #根据token判断新账号的权限
        if token is None:
            return {"code":1004, "msg":"token为空"}
        else:
            token_auth_type = functions.token_auth(token)
            token_dept_id   = functions.token_auth_dept(token)
            if token_auth_type is False or token_dept_id is False:
                return {"code":1003, "msg":"非法token"}
            
        #防SQL注入
        if userid_post is None:
            return {"code":1001, "msg":"参数传递不完整"}
        else:
            userid = MySQLdb.escape_string(userid_post).decode('utf-8')
        conn = db.mysql_connect()
        curs = conn.cursor()
        curs.execute('set autocommit=0')
        
        try:
            if int(token_auth_type) < 9:
                #鉴权，只能删除比当前账号权限低的用户
                sql = "select auth_type from users where userid='{0}'".format(userid)
                curs.execute(sql)
                for i in curs.fetchone():
                    if i >= int(token_auth_type):
                        return {"code":1002, "msg":"权限不足"}
                #鉴权，只能删除同部门的用户
                sql = "select dept_id from users where userid='{0}'".format(userid)
                curs.execute(sql)
                for i in curs.fetchone():
                    if i != int(token_dept_id):
                        return {"code":1002, "msg":"跨部门删除权限错误"}
                    
            sql = "delete from users where userid='{0}'".format(userid)
            curs.execute(sql)
            conn.commit()
            curs.close()
            conn.close()
            return {"code":1000, "msg":"删除成功"}
        except Exception as e:
            curs.close()
            conn.close()
            return {"code":1001, "msg":str(e)}


# 测试接口
class Test(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=str, default=None)
        
    def get(self, id):
        return id
    
    def post(self):
        data = self.parser.parse_args()
        id   = data.get('id')
        return id