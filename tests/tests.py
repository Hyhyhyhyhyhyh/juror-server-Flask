from flask import Flask, request
from flask_restful import Resource, reqparse, abort

# 测试接口
class Test(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=str, default=None)
        
    def get(self, token):
        data = self.parser.parse_args()
        id   = data.get('id')
        return token+"|"+id
    
    def post(self):
        data = self.parser.parse_args()
        id   = data.get('id')
        return id