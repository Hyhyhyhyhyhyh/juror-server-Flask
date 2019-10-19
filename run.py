from flask import Flask
from flask_restful import Api
from flask_cors import *

from app.user_views import *
from tests.tests import *

app = Flask(__name__, template_folder=None, static_folder=None)
api = Api(app)
CORS(app, resources={r"/.*": {"origins": "http://www.sghen.cn"}}, supports_credentials=True)


api.add_resource(CreateUser,    '/api/user/create')
api.add_resource(Login,         '/api/user/login')
api.add_resource(ModifyUser,    '/api/user/modify')
api.add_resource(UserList,      '/api/user/query/<string:token>')
api.add_resource(DropUser,      '/api/user/drop')
api.add_resource(Test,          '/api/test/<string:token>')
# api.add_resource(CreateUser, '/api/juror/query')

if __name__ == '__main__':
    app.run(debug=True)