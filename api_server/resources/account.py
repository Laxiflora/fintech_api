from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql
import traceback



parser = reqparse.RequestParser()
parser.add_argument('balance')
parser.add_argument('account_number')
parser.add_argument('user_id')


class Account(Resource):
    def db_init(self):
        db = pymysql.connect(host='localhost',user='root',password='elton8058',db='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def patch(self,user_id,id):
        db,cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            'balance':arg['balance'],
            'account_number':arg['account_number'],
            'user_id':arg['user_id'],
        }
        query = []
        print(account)
        for key,value in account.items():
            if value != None:
                print("{},{}".format(key,value))
                query.append(key + " = " + " '{}' ".format(value))
        query = ",".join(query)
        print(query)
        sql = """
        UPDATE api.accounts SET {} WHERE id = {};
        """.format(query,id)
        print(sql)

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

    def get(self,user_id,id):
        db, cursor = self.db_init()
        sql = """ SELECT * FROM api.accounts where id = '{}' and deleted is not True and user_id = '{}'
        """.format(id,user_id)
        cursor.execute(sql)
        db.commit()
        account = cursor.fetchone()
        db.close()
        return jsonify({'data':account})

    def delete(self,user_id,id):
        db, cursor = self.db_init()
        sql = """ 
            UPDATE api.accounts SET deleted = True WHERE id = '{}'
        """.format(id)
        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'SUCCESS'
        except:
            traceback.print_exc()
            response['msg'] = "FAILED"
        db.commit()
        db.close()
        return jsonify(response)
    
class Accounts(Resource):
    def db_init(self):
        db = pymysql.connect(host='localhost',user='root',password='elton8058',db='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor    
    
    def post(self,user_id):
        db, cursor=self.db_init()
        arg = parser.parse_args()
        print(arg)
        account = {
            'balance':arg['balance'],
            'account_number':arg['account_number'],
            'user_id':arg['user_id'],
        }
        sql = """
        INSERT INTO `api`.`accounts` (`balance`, `account_number`, `user_id`)
        VALUES ({},{},{});
        """.format(account['balance'],account['account_number'],account['user_id'])
        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'SUCCESS'
        except:
            traceback.print_exc()
            response['msg'] = 'FAILED'
        db.commit()
        db.close()
        return jsonify(response)


    def get(self,user_id):
        db, cursor = self.db_init()
        sql = """ SELECT * FROM api.accounts where deleted is not True
        """.format(user_id)
        cursor.execute(sql)
        db.commit()
        accounts = cursor.fetchall()
        db.close()
        return jsonify({'data':accounts})