from flask import Flask, request
from flask_restful import Resource, reqparse, abort
import re
import jieba
from collections import Counter
from itertools import chain

import hashlib, sys, MySQLdb,json,base64
sys.path.insert(0, '..')
from utils import db, functions

class Analyze(Resource):
    """数据分析
    
    returns:
        1000 查询成功
        1001 后端代码运行出错
        1002 请求参数缺失
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('db', type=str, default=None)
        self.parser.add_argument('table_name', type=str, default=None)
        self.parser.add_argument('col_name', type=str, default=None)
        
    def get(self, token):
        data = self.parser.parse_args()
        database    = data.get('db')
        table_name  = data.get('table_name')
        col_name    = data.get('col_name')

        if not all([db_ip, database, table_name, col_name]):
            return {"code":1002, "msg":"请求参数缺失"}
        else:
            mysql_host    = '127.0.0.1'
            mysql_port    = 3306
            conn_user     = 'system'
            conn_password = 'H5cT7yHB8_'
            conn = MySQLdb.connect(host=mysql_host,
                                port=mysql_port,
                                user=conn_user,
                                passwd=conn_password,
                                db=database,
                                charset='utf8',
                                use_unicode=True)
            curs = conn.cursor()
            sql = "select {0} from {1}".format(col_name, table_name)
            curs.execute(sql)
            result = curs.fetchall()

            # 清洗标点
            pattern = r"[!\"#$%&'()*+,-.:;<=>?@[\\\]^_`{|}~——！，。？、￥…（）：；【】《》‘’“”\s]+"
            data = [re.sub(pattern, "", r[0]) for r in result]

            words = [jieba.lcut(r) for r in data]
            # print(words)

            # 词汇统计
            c = Counter(chain.from_iterable(words))
            common = c.most_common(15)
            # print(common)