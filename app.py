from flask import Flask,request,render_template 
import pandas as pd


from pymongo import MongoClient 
client = MongoClient('localhost', 27017)
app = Flask(__name__)
@app.route('/')
def login():
    return render_template('index.html')

@app.route('/validation_login',methods=['POST','GET'])
def validation_login():
    
    data=pd.DataFrame(list(client.newdatabase.latha_table.find()))
    mail=request.form['username']
    pwd=request.form['password']
    if mail not in list(data['email']):
	    return render_template('index.html',info='Invalid User')
    else:
        if pwd not in list(data['password']):
            return render_template('index.html',info='Invalid Password')
    
    name=list(data['name'])[list(data['email']).index(mail)]
    return render_template('home.html',name=name)
    

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/uplode_database",methods=['POST','GET'])
def uplode_database():
    name1=request.form['name']
    mail=request.form["email"]
    pwd=request.form['password']
    d=dict()
    d['name'],d['email'],d['password']=name1,mail,pwd
    data=pd.DataFrame(list(client.newdatabase.latha_table.find()))
    if mail in list(data['email']):
	    return render_template('index.html',info='Alreaday User please login')
    client['newdatabase']['latha_table'].insert_one(d)
    return render_template("home.html",name=name1)
if __name__ == '__main__':
    app.run(debug=True)
    