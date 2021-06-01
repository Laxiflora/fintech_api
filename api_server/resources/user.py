from flask_restful import Resource, reqparse
from flask import jsonify , make_response
import pymysql
import traceback

from pymysql import cursors
from server import db
from models import UserModel




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
        #db,cursor = self.db_init()
        arg = parser.parse_args()
        '''
        #without server
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
        '''
        user = UserModel.query.filter_by(id = id , deleted = None).first()
        if arg['name'] != None:
            user.name = arg['name']

        response = {}
        try:
            status_code = 200
            #cursor.execute(sql)
            db.session.commit()
            response['msg'] = "SUCCESS"
        except:
            status_code = 400
            traceback.print_exc()
            response['msg'] = "FAILED"
        #db.commit()
        #db.close()
        return make_response(jsonify(response) , status_code)

    def get(self,id):
        users = UserModel.query.filter(UserModel.deleted.isnot(True)).all()
        return jsonify({'data':list(map(lambda user:user.serialize(),users))})

    def delete(self,id):
        #db, cursor = self.db_init()
       # sql = """ 
        #    UPDATE api.users SET deleted = True WHERE id = '{}'
        #""".format(id)
        user = UserModel.query.filter_by(id = id).first()
        print(user,end = "  LALA\n")
        response = {}
        try:
            #cursor.execute(sql)
            status_code = 200
            db.session.delete(user)
            db.session.commit()
            response['msg'] = 'SUCCESS'
        except:
            traceback.print_exc()
            if(user == None):
                status_code = 400
                response['msg'] = 'user not exists!'
            else:    
                status_code = 500
                response['msg'] = "FAILED"
    #    db.commit()
    #    db.close()
        return make_response(jsonify(response) , status_code)
    
class Users(Resource):
    def db_init(self):
        db = pymysql.connect(host='localhost',user='root',password='elton8058',db='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor    
    
    def post(self):
        #print("Function called")
        arg = parser.parse_args()
        user = {
            'name':arg['name'],
            'gender':arg['gender'] or 0,
            'birth':arg['birth'] or '1900-01-01',
            'note':arg['note'],
        }
        response = {}
        status_code=200
        try:
            new_user = UserModel(name = user['name'],gender=user['gender'],birth=user['birth'],note=user['note'])
            db.session.add(new_user)
            db.session.commit()
            response['msg']='success'
        except:
            status_code=400
            traceback.print_exc()
            response['msg'] = 'FAILED'
        return make_response(jsonify(response) , status_code)


    def get(self):
        users = UserModel.query.filter(UserModel.deleted.isnot(True)).all()
        return jsonify({'data':list(map(lambda user:user.serialize(),users))})

        ''' 
            #without using server

            db, cursor = self.db_init()
            arg = parser.parse_args()
            sql = "SELECT * FROM api.users where deleted is not True"
            if arg['gender'] != None:
                sql += ' and gender = "{}" '.format(arg['gender'])
            cursor.execute(sql)
            db.commit()
            users = cursor.fetchall()
            db.close()
            return make_response( jsonify({'data':users}) , 400 )
        '''