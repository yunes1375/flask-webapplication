from contextlib import nullcontext
from sqlite3 import Cursor
from flask import Flask,request,render_template, flash,redirect, send_file,url_for,jsonify,session
from h11 import Data
from pymysql import NULL
import json
# from flask_mysqldb import MySQL
import mysql.connector
import os
from zipfile import ZipFile
from flask_cors import CORS,cross_origin
from werkzeug.utils import secure_filename
from random import random
from werkzeug.datastructures import ImmutableMultiDict
images_folder = os.path.join('static')
#database user pass must be enterd here
cnx = mysql.connector.connect(user='root', password='1290',
                              host='127.0.0.1',
                              database='civil',
                              auth_plugin='mysql_native_password')
def sql_project_factors(projectid) :
    safetyfactor=0
    traficfactor=0
    cursor12=cnx.cursor(dictionary=True)
    query12='select safetyfactor,traficfactor from projects where idprojects =\'%s\';'%int(projectid)
    cursor12.execute(query12)
    for row in cursor12:
        safetyfactor=row["safetyfactor"]
        traficfactor=row["traficfactor"]
    return (safetyfactor,traficfactor)
sql_project_factors(6)