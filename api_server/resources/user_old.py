from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql
import traceback




parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')


class User(Resource):
    def db_init(self):
        db = pymysql.connect(host='localhost',user='root',password='elton8058',db='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    

    def patch(self,id):
        db,cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name':arg['name'],
            'gender':arg['gender'],
            'birth':arg['birth'],
            'note':arg['note'],
        }
        query = []
        for key,value in user.items():
            if value != None:
                print("{},{}".format(key,value))
                query.append(key + " = " + " '{}' ".format(value))
        query = ",".join(query)
        print(query)
        sql = """
        UPDATE api.users SET {} WHERE id = {};
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

    def get(self,id):
        db, cursor = self.db_init()
        sql = """ SELECT * FROM api.users where id = '{}' and deleted is not True
        """.format(id)
        cursor.execute(sql)
        db.commit()
        user = cursor.fetchone()
        db.close()
        return jsonify({'data':user})

    def delete(self,id):
        db, cursor = self.db_init()
        sql = """ 
            UPDATE api.users SET deleted = True WHERE id = '{}'
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
    
class Users(Resource):
    def db_init(self):
        db = pymysql.connect(host='localhost',user='root',password='elton8058',db='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor    
    
    def post(self):
        db, cursor=self.db_init()
        arg = parser.parse_args()
        user = {
            'name':arg['name'],
            'gender':arg['gender'] or 0,
            'birth':arg['birth'] or '1900-01-01',
            'note':arg['note'],
        }
        sql = """
        INSERT INTO `api`.`users` (`name`, `gender`, `birth`, `note`)
        VALUES ('{}','{}','{}','{}');
        """.format(user['name'],user['gender'],user['birth'],user['note'])
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


    def get(self):
        db, cursor = self.db_init()
        sql = """ SELECT * FROM api.users where deleted is not True"""
        cursor.execute(sql)
        db.commit()
        users = cursor.fetchall()
        db.close()
        return jsonify({'data':users})