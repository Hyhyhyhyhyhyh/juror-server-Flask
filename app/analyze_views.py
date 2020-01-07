from flask import Flask, request
from flask_restful import Resource, reqparse, abort
import re
import jieba
from collections import Counter
from itertools import chain

import hashlib, sys, MySQLdb,json,base64
sys.path.insert(0, '..')
from utils import db, functions

class WordFreqyency(Resource):
    '''
    usage: 传入-数据库名/表名/列名，分析文本中的热词
    url  : /api/analyze/wordfrequency/<string:database>/<string:table_name>/<string:col_name>

    returns:
        1000 查询成功
        1001 后端代码运行出错
        1002 请求参数缺失
    '''
    def get(self, database, table_name, col_name):
        if not all([database, table_name, col_name]):
            return {"code":1002, "msg":"请求参数缺失"}
        else:
            conn = db.analyze_db_connect(database)
            curs = conn.cursor()
            sql = "select {0} from {1}".format(col_name, table_name)
            curs.execute(sql)
            result = curs.fetchall()

            # 清洗标点
            pattern = r"[!\"#$%&'()*+,-.:;<=>?@[\\\]^_`{|}~——！，。？、￥…（）：；【】《》‘’“”\s]+"
            data = [re.sub(pattern, "", r[0]) for r in result]

            words = [jieba.lcut(r) for r in data]
            # print(words)

            # 停用词处理
            stopword = []
            with open ('/data/pyweb/juror-server/utils/stopword.txt', encoding='UTF-8') as f:
                for line in f:
                    stopword.append(line.strip())
                    
            words_new = [word[0] for word in words if word[0] not in stopword]
                    
            # 词汇统计
            # c = Counter(chain.from_iterable(words_new))
            c = Counter(words_new)
            common = c.most_common()
            # print(common)

            return common

"""
class NginxLogAnalyze(Resource):
    '''
    usage: nginx日志分析
    url  : /api/analyze/nginx

    returns:
        1000 查询成功
        1001 后端代码运行出错
    '''
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('begin_date', type=str, default=None)
        self.parser.add_argument('end_date', type=str, default=None)

    def get(self):
        data = self.parser.parse_args()
        begin_date = data.get('begin_date')
        end_date   = data.get('end_date')

        # 先到数据库查询日志信息，不存在则进行日志分析后保存到数据库中
        conn = db.analyze_db_connect('analyze_db')
        curs = conn.cursor()
        sql  = ""

        return
"""