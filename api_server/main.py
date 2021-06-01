from flask import Flask, request , jsonify
from flask_restful import Api
from resources.user import Users, User
from resources.account import Account, Accounts
import pymysql
import traceback
import jwt
import time
from server import app


api = Api(app)
api.add_resource(Users,'/users')
api.add_resource(User,'/user/<id>')
api.add_resource(Account,'/user/<user_id>/account/<id>')
api.add_resource(Accounts,'/user/<user_id>/accounts')

"""
####驗證
@app.before_request
def auth():
    token = request.headers.get('auth')
    user_id = request.get_json()['user_id']
    valid_token = jwt.encode(
        {
        'user_id':user_id,
        'timestamp':int(time.time())
        },
        'password',algorithm='HS256').decode('utf-8')
    print(jwt.encode({'user_id':user_id,'timestamp':int(time.time())},'password',algorithm='HS256'))
    print(valid_token)
    if token != valid_token:
        return {'msg':'invalid token'}

"""

@app.errorhandler(Exception)
def handle_error(error):
    status_code=500
    if type(error).__name__ == "NotFound":
        status_code=404
    elif type(error).__name__ == "TypeError":
        status_code =500
    elif type(error).__name__ == "BadRequest":
        status_code = 501
    return jsonify({'msg':type(error).__name__}),status_code




def get_account(id):
        db = pymysql.connect(host='localhost',user='root',password='elton8058',db='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = """
        SELECT * FROM api.accounts WHERE id = '{}' and deleted is not True
        """.format(id)
        cursor.execute(sql)
        return db,cursor,cursor.fetchone()


@app.route('/')
def index():
    return 'Hello world'


@app.route('/user/<user_id>/account/<id>/deposit',methods=['POST'])
def deposit(user_id,id):
#    123+"123"
    db,cursor,account = get_account(id)
    money = request.get_json()['money']
    balance = account['balance'] + int(money)
    sql = """
    UPDATE api.accounts SET balance = {} WHERE id = {} and deleted is not true
    """.format(balance,id)
    response = {}
    try:
        cursor.execute(sql)
        response['msg'] = "SUCCESS"
    except:
        traceback.print_exc()
        response['msg'] = "FAILED"
    db.commit()
    db.close()
    return jsonify(response)


@app.route('/user/<user_id>/account/<id>/withdraw',methods=['POST'])
def withdraw(user_id,id):
    db,cursor,account = get_account(id)
    money = request.get_json()['money']
    balance = account['balance'] - int(money)
    sql = """
    UPDATE api.accounts SET balance = {} WHERE id = {} and deleted is not true
    """.format(balance,id)
    response = {}
    try:
        cursor.execute(sql)
        response['msg'] = "SUCCESS"
    except:
        traceback.print_exc()
        response['msg'] = "FAILED"
    db.commit()
    db.close()
    return jsonify(response)
    

if __name__ == '__main__':
    app.debug = True
   # app.run(host='0.0.0.0',port=5000)
    app.run()




