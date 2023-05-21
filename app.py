from flask import Flask,render_template,request
from markupsafe import escape
import mysql.connector

app = Flask(__name__)

con = mysql.connector.connect(host="localhost",password="140604",user="root",charset="utf8")
cur = con.cursor()
cur.execute('use clubs')

if __name__=="__main__":
    app.run(debug=True)

@app.route("/", methods = ["POST","GET"])
def events():
    cur.execute("select distinct club from event")
    club = cur.fetchall()
    a = str(club)
    a = a.replace("('","")
    a = a.replace("',)","")
    a = a.replace("[","")
    a = a.replace("]","")
    club = a.split(',')
    club.sort()
    if request.method == "POST":
        clb = str(request.form['CLUB'])
        print(clb)
        clb = clb.strip()
        cur.execute("select * from event where club = '"+clb+"'")
        details = cur.fetchall()
        return render_template('login.html',club = club, check = details)
    else:
        return render_template('login.html',club = club)


@app.route('/transfer')
def transfer():
    cur.execute("select * from transfer")
    data = cur.fetchall()
    a = str(data)
    a = a.replace("('","")
    a = a.replace("',),","")
    a = a.replace("[","")
    a = a.replace("]","")
    a = a.replace("\\r\\n"," ")
    data = a.split('!')
    data = data[:-1]
    return render_template('index.html',transfer = data)

@app.route('/internship')
def intern():
    cur.execute("select * from internship")
    data = cur.fetchall()
    a = str(data)
    print(a)
    a = a.replace("('","")
    a = a.replace("(\"","")
    a = a.replace("',),","")
    a = a.replace("[","")
    a = a.replace("]","")
    a = a.replace("\\r\\n"," ")
    data = a.split('?')
    data = data[:-1]
    return render_template('intern.html',intern = data)