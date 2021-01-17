from flask import Flask, render_template, request, session, redirect, url_for, app
from utils.db_utils import  writeToDatabase, readFromDatabase
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "wakawaka"

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    if "username" in session:
        return render_template("/homepage.html")
    return render_template("login.html")


@app.route('/register', methods=['GET'])
def registerPage():
    return render_template("register.html")


@app.route('/register', methods=['POST'])
def register_user():
    email = request.form["email"]
    password = request.form["password"]
    name = request.form["username"]

    writeToDatabase(f"INSERT INTO user (Name, email, password) VALUES ('{name}','{email}', '{password}');")
    return "Registration successful!!"


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']


    result = readFromDatabase(f"SELECT * FROM user WHERE email='{email}' AND password='{password}' limit 1")
    if len(result) == 0:
        return "Invalid Login Credentials"
    else:

        user = result[0][1]

        session["username"] = user
        return redirect(url_for("username"))

@app.route("/profile", methods=['GET'])
def username():
    if "username" in session:
        user_id = session["username"]
        print (user_id)
        return render_template('/profile.html')
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    session.pop("username")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

