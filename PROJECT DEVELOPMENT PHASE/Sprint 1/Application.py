# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 19:35:25 2022

@author: pc
"""

from xml.etree.ElementTree import tostring
from flask import Flask, request, render_template, flash, session, redirect, url_for
import ibm_db


def connection():
    try:
        conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;\
            PORT=32716;PROTOCOL=TCPIP;UID=cyp26260;PWD=2u8Lfagovgh630DH;SECURITY=SSL;SSLServiceCertificate=DigiCertGlobalRootCA.crt", "", "")
        print("Connected to Database")
        return conn
    except:
        print("Not Connected to Database")


app = Flask(__name__)
app.secret_key = '123'
conn = connection()
app.debug = True
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/', methods=["GET", "POST"])
def defaultpage():
    if request.method == "POST":
        try:
            sql = "INSERT INTO USER VALUES('{}','{}','{}','{}')".format(request.form["rollno"], request.form["email"], request.form["username"],
                                                                        request.form["password"])
            ibm_db.exec_immediate(conn, sql)
            flash("Successfully Registered!")
            print('registered')

            return render_template('login.html')
        except Exception as inst:
            print(inst)
            print(inst.args)
            flash("Account already exists!")
            return render_template('register.html')
    else:
        return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sql = "SELECT COUNT(*) FROM USER WHERE USERNAME=? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        res = ibm_db.fetch_assoc(stmt)
        if res['1'] == 1:
            session['loggedin'] = True
            session['username'] = username
            return render_template('welcome.html')  
        else:
            flash("Username/ Password is incorrect!")
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':

    app.run()
