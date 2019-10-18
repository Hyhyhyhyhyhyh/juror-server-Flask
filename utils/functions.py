import sys, MySQLdb, jwt
sys.path.insert(0, '..')
from . import db

secret_key  = 'HvcqYXeCN8YW1*Q%l0EmDllf#UF^6PNe'

# 构造JWT
def token_encode(userid,username,auth_type,jurorid,dept_id):
    token = jwt.encode({'userid':userid,
                        "username":username,
                        "auth_type":auth_type,
                        "jurorid":jurorid,
                        "dept_id":dept_id}, secret_key, algorithm='HS256')
    return token.decode('utf-8')

def token_auth(token):
    """
    1. 解析JWT
    2. 验证传入的token的合法性
    3. 返回当前token的权限auth_type
    """
    token_data = jwt.decode(token, secret_key,algorithms=['HS256'])
    userid    = token_data['userid']
    username  = token_data['username']
    auth_type = token_data['auth_type']
    jurorid   = token_data['jurorid']
    dept_id   = token_data['dept_id']
    
    conn = db.mysql_connect()
    curs = conn.cursor()
    sql  = "select auth_type from users where userid='{0}' and username='{1}' and auth_type={2} and jurorid={3} and dept_id={4}".format(userid,username,auth_type,jurorid,dept_id)
    if curs.execute(sql) == 1:
        auth_type = curs.fetchone()
        curs.close()
        conn.close()
        for i in auth_type:
            return i
    else:
        curs.close()
        conn.close()
        return False
    
# 根据token获取用户所在部门
def token_auth_dept(token):
    token_data = jwt.decode(token, secret_key,algorithms=['HS256'])
    userid    = token_data['userid']
    username  = token_data['username']
    auth_type = token_data['auth_type']
    jurorid   = token_data['jurorid']
    dept_id   = token_data['dept_id']
    
    conn = db.mysql_connect()
    curs = conn.cursor()
    sql  = "select dept_id from users where userid='{0}' and username='{1}' and auth_type={2} and jurorid={3} and dept_id={4}".format(userid,username,auth_type,jurorid,dept_id)
    if curs.execute(sql) == 1:
        dept_id = curs.fetchone()
        curs.close()
        conn.close()
        for i in dept_id:
            return i
    else:
        curs.close()
        conn.close()
        return False