from hashlib import sha1
import hmac
from logging import debug
from wsgiref.handlers import format_date_time
import datetime
from time import mktime
import base64
from requests import request
from pprint import pprint
import json
import math

import requests
import geocoder

app_id = 'defd5cd9124746788be43e840b5b66b8'
app_key = 'rdKMsBfEiW4eXe4d5a9nshnfGWs'

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }

def getNearestStation():
    response = request('get', 'https://ptx.transportdata.tw/MOTC/v3/Rail/TRA/Station?$format=JSON', headers= a.get_auth_header())
    data = json.loads(response.text)
    near = {"name": "undefined" , "length" : 999999}
    current_loc = geocoder.ip('me').latlng
    for station in data['Stations']:
        lat = station['StationPosition']['PositionLat']
        lon = station['StationPosition']['PositionLon']
        result = math.sqrt( (current_loc[0] - lat)**2 + (current_loc[1] - lon)**2)
        if(near['length']>result):
            near['length'] = result
            near['name'] = station['StationName']['Zh_tw']
            near['id'] = station['StationID']
    return near


def getNextTrain(stationID):
    response = request('get' , ('https://ptx.transportdata.tw/MOTC/v3/Rail/TRA/DailyStationTimetable/Today/Station/'+stationID), headers= a.get_auth_header())
    data = json.loads(response.text)
    countdown = 999999
    trainTypeID=""
    now_time_hr = datetime.datetime.now().timetuple().tm_hour
    now_time_min = datetime.datetime.now().timetuple().tm_min
    for stop in data['StationTimetables'][0]['TimeTables']:
        stop_time = ( int(stop['ArrivalTime'][3:5]) - now_time_min ) + (int(stop['ArrivalTime'][0:2]) - now_time_hr)*60
        if(countdown > stop_time and stop_time > 0):
            countdown = stop_time
            trainTypeID = stop['TrainTypeID']
            arrive_time= stop['ArrivalTime']
    return (trainTypeID,arrive_time,countdown)



if __name__ == '__main__':
    a = Auth(app_id, app_key)
    nearestStation = getNearestStation()
    trainTypeID,nextArriveTime,timeLeft = getNextTrain(nearestStation['id'])
    print("現在時刻 : {}".format( format_date_time(mktime(datetime.datetime.now().timetuple()))   ))
    print("距離你最近的火車站為 : {}".format(nearestStation['name']))
    print("最近到達{}站的車次為{},該車次到達時間為{},你尚有{}秒".format(nearestStation['name'],trainTypeID,nextArriveTime,timeLeft*60))