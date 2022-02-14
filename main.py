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
def sql_data():
    data=[]
    cursor=cnx.cursor(dictionary=True) 
    query='select * from cheklist;'
    cursor.execute(query)
    for row in cursor:
        data.append(row)
    return data

def deletesql(id):
    cursor2=cnx.cursor()
    query2='delete from cheklist where idcheklist = \'%s\' ;'%int(id)
    cursor2.execute(query2)
    cnx.commit()
    return True
def insert_sql(finaldata):
    Cursor3=cnx.cursor()
    query3='insert into cheklist (idcheklist,regulation,article,requirement,answer_type,high_limit,low_limit,guidance_type,guidance_filepath) values (\'%s\' , \'%s\' , \'%s\' ,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\' ) ;'%(finaldata["idcheklist"] ,finaldata["regulation"] ,finaldata["article"],finaldata["requirement"],finaldata["answer_type"],finaldata["high_limit"],finaldata["low_limit"],finaldata["guidance_type"],finaldata["guidance_filepath"])
    Cursor3.execute(query3)
    cnx.commit()
    return True
        
def insert_sql_layout(finaldata):
    Cursor10=cnx.cursor()
    query10='insert into layouts (idlayouts,layoutname,projectname,projectid,ifcfilepath,tilesetfilepath,facilitynumbers,safetypoint,traficalponit,safetyfactor,traficfactor) values (\'%s\' , \'%s\' , \'%s\' ,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\' ) ;'%(int(finaldata["idlayouts"]) ,finaldata["layout name"] ,finaldata["projectname"],finaldata["idprojects"],finaldata["ifcfilepath"],finaldata["tilesetfilepath"],int(finaldata["facilitynumbers"]),str(finaldata["safetypoint"]),str(finaldata["traficalponit"]),str(finaldata["safetyfactor"]),str(finaldata["traficfactor"]))
    Cursor10.execute(query10)
    cnx.commit()
    return True
    
#get safety and trafical factor
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

# get projects list from mysql
def projects_sql():
    data=[]
    Cursor4=cnx.cursor(dictionary=True)
    query4='select * from projects'
    Cursor4.execute(query4)
    for x in Cursor4:
        data.append(x)
    return data
def delete_project_sql(id):
    cursor5=cnx.cursor()
    query5='delete from projects where idprojects = \'%s\' ;'%int(id)
    cursor5.execute(query5)
    cnx.commit()
    return True
def layout_delete(id):
    cursor11=cnx.cursor()
    query11='delete from layouts where idlayouts = \'%s\' ;'%int(id)
    cursor11.execute(query11)
    cnx.commit()
    return True
def insert_sql_project(formdata):
    Cursor6=cnx.cursor()
    query6='insert into projects (idprojects,projectname,description,safetyfactor,traficfactor) values (\'%s\' , \'%s\' , \'%s\', \'%s\' , \'%s\'  ) ;'%(formdata["idprojects"] ,formdata["projectname"] ,formdata["description"],formdata["safetyfactor"] ,formdata["traficfactor"])
    Cursor6.execute(query6)
    cnx.commit()
    return True

def project_layout_getter(_id):
    data=[]
    ids=[]
    Cursor7=cnx.cursor(dictionary=True)
    query7='select * from layouts where projectid = \'%s\' ;'%int(_id)
    Cursor7.execute(query7)
    for x in Cursor7:
        data.append(x)
    query7="select * from layouts;"
    Cursor7.execute(query7)
    for x in Cursor7:
       ids.append(x['idlayouts']) 
    lenlayouts=max(ids)
    return (lenlayouts,data)
def get_layout_data(idlayout):
    data=[]
    Cursor14=cnx.cursor(dictionary=True)
    query14='select * from layouts where idlayouts = \'%s\' ;'%int(idlayout)
    Cursor14.execute(query14)
    for row in Cursor14:
        data.append(row)
    return (data)
def sql_layout_points(layout):
    data=[]
    Cursor8=cnx.cursor(dictionary=True)
    query8='select * from layouts where idlayouts = \'%s\' ;'%int(layout)
    Cursor8.execute(query8)
    for x in Cursor8:
        data.append(x)
    return data
def sql_safetypoint_inserter(point,layout):
    Cursor9=cnx.cursor()
    query9='update layouts set safetypoint = \'%s\' where idlayouts = \'%s\' ;'%(point,layout)
    Cursor9.execute(query9)
    cnx.commit()
def sql_trficalpoint_inserter(point,layout):
    Cursor13=cnx.cursor()
    query13='update layouts set traficalponit = \'%s\' where idlayouts = \'%s\' ;'%(point,layout)
    Cursor13.execute(query13)
    cnx.commit()
app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = images_folder
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
@app.route('/home')
def home():
    data=sql_data()
    return render_template('questions.html',data=data)
    # return render_template('Update.html') 
##UPLOAD TEST
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/add', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        formdata= request.form
        finaldata={}
        for x in formdata.keys():
            finaldata[x]=formdata[x]
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect('/home')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            finaldata["guidance_type"]="No"
            finaldata["guidance_filepath"]=""
            if "high_limit" not in finaldata.keys():
                finaldata["high_limit"]=""
                finaldata["low_limit"]=""
            insert_sql(finaldata)
            return redirect('/edit')
        if file and allowed_file(file.filename):
            filename =finaldata["idcheklist"]+secure_filename(file.filename)
            finaldata["guidance_type"]="image"
            finaldata["guidance_filepath"]=filename
            if "high_limit" not in finaldata.keys():
                finaldata["high_limit"]=""
                finaldata["low_limit"]=""
            insert_sql(finaldata)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/edit') 
# add project route
@app.route('/addproject', methods=['GET', 'POST'])
def add_projects():
    if request.method == 'POST':
        formdata= request.form
        insert_sql_project(formdata)
        return redirect('/') 
# add layout
@app.route('/addlayout/<_id>/<projectname>/<projectid>', methods=['GET', 'POST'])
def add_layout(_id,projectname,projectid):
    if request.method == 'POST':
        formdata= request.form.to_dict()
        if request.files["cesiumfile"].filename != '':
            path = os.getcwd()
            cesiumfilepath = os.path.join(path,"static")
            if not os.path.isdir(cesiumfilepath):
                os.mkdir(cesiumfilepath)
            cesiumfilepath = os.path.join(cesiumfilepath,projectid)
            if not os.path.isdir(cesiumfilepath):
                os.mkdir(cesiumfilepath)
            cesiumfilepath = os.path.join(cesiumfilepath,_id)
            if not os.path.isdir(cesiumfilepath):
                os.mkdir(cesiumfilepath)
            cesiumfilepath = os.path.join(cesiumfilepath,'cesium')
            if not os.path.isdir(cesiumfilepath):
                os.mkdir(cesiumfilepath)       
            if not os.path.isdir(cesiumfilepath):
                os.mkdir(cesiumfilepath) 
            request.files["cesiumfile"].save(os.path.join(cesiumfilepath, request.files["cesiumfile"].filename))
            file_name = cesiumfilepath+"\\"+request.files["cesiumfile"].filename
            with ZipFile(file_name, 'r') as zip:
                zip.printdir()
                zip.extractall(cesiumfilepath)
            formdata['tilesetfilepath']=str(request.files["cesiumfile"].filename)
        else:
            formdata['tilesetfilepath']=""
            
        
        if request.files["ifcfile"].filename != '':
            path = os.getcwd()
            ifcfilepath = os.path.join(path,"static")
            if not os.path.isdir(ifcfilepath):
                os.mkdir(ifcfilepath)
            ifcfilepath = os.path.join(ifcfilepath,projectid)
            if not os.path.isdir(ifcfilepath):
                os.mkdir(ifcfilepath)
            ifcfilepath = os.path.join(ifcfilepath,_id)
            if not os.path.isdir(ifcfilepath):
                os.mkdir(ifcfilepath)
            ifcfilepath = os.path.join(ifcfilepath,"ifcfile")
            if not os.path.isdir(ifcfilepath):
                os.mkdir(ifcfilepath)
            if not os.path.isdir(ifcfilepath):
                os.mkdir(ifcfilepath) 
            request.files["ifcfile"].save(os.path.join(ifcfilepath, request.files["ifcfile"].filename))
            formdata['ifcfilepath']=str(request.files["ifcfile"].filename)
        else:
            formdata['ifcfilepath']=""
        formdata["safetypoint"]=0.00   
        formdata["traficalponit"]=0.00
        (safetyfactor,traficfactor)=sql_project_factors(projectid)
        formdata["safetyfactor"]=safetyfactor
        formdata["traficfactor"]=traficfactor  
        insert_sql_layout(formdata)
        redirectpath='/'+'project'+'/'+projectid+'/'+projectname
        return redirect(redirectpath)
@app.route('/submit', methods = ['POST','GET'])
def submit():
    formdata= request.form
    _keys=formdata.keys()
    points=0.0
    count=0
    for key in _keys:
        if "description" not in str(key):
            points=points+random()
            count=count+1
    point=points/count
    return render_template("score_page.html",point=point)
@app.route('/submit_safety/<project>/<layout>', methods = ['POST','GET'])
def submit_layout_safety(project,layout):
    formdata= request.data
    formdata=json.loads(formdata.decode('utf-8'))
    _keys=dict(formdata).keys()
    points=0.0
    count=0
    for key in _keys:
        if "description" not in str(key):
            points=points+random()
            count=count+1
    safetypoint=points/count
    sql_safetypoint_inserter(safetypoint,layout)
    return jsonify("safetypoint",str(safetypoint))
@app.route('/submit_trafic/<project>/<layout>', methods = ['POST'])
def submit_layout_trafic(project,layout):
    formdata= request.data
    formdata=json.loads(formdata.decode('utf-8'))
    _keys=dict(formdata).keys()
    points=0.0
    count=0
    for key in _keys:
        if "description" not in str(key):
            points=points+random()
            count=count+1
    traficpoint=points/count
    sql_trficalpoint_inserter(traficpoint,layout)
    print(traficpoint)
    return jsonify("traficponit",str(traficpoint))
@app.route('/delete/<_id>', methods = ['POST','GET'])
def deletesqlflask(_id):
    deletesql(_id) 
    return redirect ('/edit')
# delete project
@app.route('/projects/delete/<_id>', methods = ['POST','GET'])
def projectsdelete(_id):
    delete_project_sql(_id) 
    return redirect ('/')
@app.route('/deletelayout/<_id>/<projectname>/<projectid>', methods = ['POST','GET'])
def layoutdelete(_id,projectname,projectid):
    layout_delete(_id) 
    rediretpath="/project/"+projectid+"/"+projectname
    return redirect (rediretpath)
@app.route('/edit', methods = ['POST','GET'])
def edit():
    data=sql_data()
    ids=[]
    print(len(data[0]))
    for x in data:
        ids.append(int(x["idcheklist"]))
    lendata=max(ids)
    return render_template('edit.html',data=data,lendata=lendata)   
@app.route('/showimage/<filepath>', methods = ['POST','GET'])
def show_image(filepath):  
    return render_template("image_show.html",filepath=filepath)
@app.route('/', methods = ['POST','GET'])
def index():
    data=projects_sql() 
    ids=[]
    for x in data:
        ids.append(int(x["idprojects"]))
    lendata=max(ids) 
    return render_template("index.html",data=data,lendata=lendata)
@app.route('/project/<_id>/<name>', methods = ['POST','GET'])
def projects(_id,name):
    (lenlayout,layouts)=project_layout_getter(_id)
    for x in layouts:
        x["layoutpoint"]=float(x["safetyfactor"])*float(x["safetypoint"])+float(x["traficfactor"])*float(x["traficalponit"])
    return render_template('layout.html',layouts=layouts,_id=_id,name=name,lenlayout=int(lenlayout)+1)  
@app.route('/layout/<project>/<layout>', methods = ['POST','GET'])
def layout(project,layout):
    data=sql_data()
    points=sql_layout_points(layout)
    lenfacility=points[0]["facilitynumbers"]
    return render_template('validation.html',project=project,layout=layout,data=data,points=points,lenfacility=lenfacility)  
@app.route('/cesiumviewer/<idlayout>', methods = ['POST','GET'])
def cesium(idlayout):
    layoutdata=get_layout_data(idlayout)
    return render_template('cesiumviewer.html',layoutdata=layoutdata) 
@app.route('/ifcviewer/<idlayout>', methods = ['POST','GET'])
def ifc(idlayout):
    return render_template('ifcviewer.html') 
if __name__ == "__main__":
       app.debug=True
       app.run(host='176.97.218.65', port=5000)