import json

from flask import Blueprint, render_template, jsonify

import pymysql
blue=Blueprint('myblue',__name__)

dbsettings={
    'host':'localhost',
    'port':3306,
    'user':'root',
    'password':'123',
    'db':"testajax"
}
@blue.route('/')
def index():
    return render_template('testPage.html')



@blue.route('/getData',methods=['GET','POST'])
def my_echart():

    conn=pymysql.connect(**dbsettings)
    with conn.cursor() as cursor:
        sql='select * from goods'
        cursor.execute(sql)
        items=cursor.fetchall()
    conn.close()

    for row in items:
        print(row)

    #转化成json格式数据
    jsonData={}
    xfname=[]
    yprice=[]
    for item in items:
        xfname.append(item[1])
        yprice.append(item[2])
    print('-------------->',xfname)
    print('-----------',yprice)
    jsonData['xfname']=xfname
    jsonData['yprice']=yprice
    return jsonify(jsonData)
    # dict2json=json.dumps(jsonData)
    # print(dict2json)
    # print(type(dict2json))
    print('myechart()执行完毕')
    # return dict2json


