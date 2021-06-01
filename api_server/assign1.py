from flask import Flask, request , jsonify
from flask_restful import Api
from resources.user import Users, User
from resources.account import Account, Accounts
from resources.assign1_account import assAccount, assAccounts
import pymysql
import traceback
import jwt
import time

app = Flask(__name__)
api = Api(app)
#api.add_resource(Users,'/users')
#api.add_resource(User,'/user/<id>')
#####Assignment 1###############
#接回account_assignment即可
api.add_resource(assAccounts,'/assaccounts')
api.add_resource(assAccount,'/assaccount/<id>')





@app.route('/')
def index():
    return 'Hello world'

if __name__ == '__main__':
    app.debug = True
   # app.run(host='0.0.0.0',port=5000)
    app.run()