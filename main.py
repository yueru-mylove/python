#!flask/bin/python
# -- coding: utf-8 --

__author__ = 'cloudtogo'

from flask import render_template
from flask import Flask
import os
import sys
import ctypes
import mysql.connector

app = Flask(__name__)

reload(sys)
sys.setdefaultencoding('utf8')
MySQLAddr = os.environ.get("MYSQLADDR")
MySQLPwd = os.environ.get("MYSQLPWD")
#MySQLAddr = "127.0.0.1"
#MySQLPwd = "root"

@app.route('/')
def hello():
    db = mysql.connector.connect(
        host=MySQLAddr,           # your host
        user='root',              # username
        passwd=MySQLPwd,          # password
        auth_plugin='mysql_native_password', # caching_sha2_password for mysql 8.0
        charset='utf8',
        db='performance_schema')  # name of the database

    cur = db.cursor()

    # 查询MySQL系统变量

    version = ''
    cur.execute("show variables like 'version'")
    for row in cur.fetchall() :
    	version = row[0] + ": " + row[1]

    version_comment = ''
    cur.execute("show variables like 'version_comment'")
    for row in cur.fetchall() :
        version_comment = row[0] + ": " + row[1]

    version_compile_os = ''
    cur.execute("show variables like 'version_compile_os'")
    for row in cur.fetchall() :
        version_compile_os = row[0] + ": " + row[1]

    Uptime = ''
    cur.execute("show status like 'Uptime'")
    for row in cur.fetchall() :
        Uptime = row[0] + ": " + row[1]

    Bytes_received = ''
    cur.execute("show status like 'Bytes_received'")
    for row in cur.fetchall() :
        Bytes_received = row[0] + ": " + row[1]

    Bytes_sent = ''
    cur.execute("show status like 'Bytes_sent'")
    for row in cur.fetchall() :
        Bytes_sent = row[0] + ": " + row[1]

    html = '<html><head><style>body{font-family:\'verdana\';h4{font-weight:bold;}}</style></head><body>'
    html = html + '<h4>已连接到MySQL(Python):</h4>' + version + '<br>' + version_compile_os + '<br>' + version_comment + '<br>'    
    html = html + Uptime + 's<br>' + Bytes_received + '<br>' + Bytes_sent + '<br>'

    # 查询默认创建的表 "template"
    
    strTable = '<br><table border=\"1\"><tr><th>id</th><th>language</th><th>framework</th><th>create_time</th></tr>'
    
    cur.execute("USE template")
    cur.execute("SELECT * FROM template LIMIT 10")

    for row in cur.fetchall() :
    	strTable = strTable + '<tr><th>' + str(row[0]) + '</th><th>' + row[1] + '</th><th>' + row[2] + '</th><th>' + str(row[3]) + '</th></tr>'
    	
    strTable = strTable + '</table>'

    html = html + strTable + '</body></html>'

    cur.close()
    db.close()

    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0')

