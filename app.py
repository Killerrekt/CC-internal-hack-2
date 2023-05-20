from flask import Flask,render_template,request
from markupsafe import escape

app = Flask(__name__)

if __name__=="__main__":
    app.run(debug=True)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<name>')
def url(name):
    return f"The name is {escape(name)}!"

@app.route('/login',methods = ['GET','POST'])
def login():
    errorraised = 0
    if request.method == "POST":
        print(request.form['Username'])
    return render_template('login.html')

