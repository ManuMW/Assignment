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

@app.route('/posting', methods=['POST'])
def posting():
    post = request.form["comment"]
    name = session["username"]
    writeToDatabase(f"INSERT INTO post (create_time, post_message, user) VALUES (CURRENT_TIME(), '{post}','{name}')")
    return redirect(url_for(username))


@app.route("/homepage", methods=['GET'])
def username():
    if "username" in session:
        user = session["username"]
        data = readFromDatabase(f"SELECT user, post_message FROM post ORDER BY create_time DESC")
        return render_template('/homepage.html', context={"name": user}, context2={"data": data})
    else:
        return redirect('/')

@app.route("/search_page")
def search_page():
    return render_template("/search.html")


@app.route("/search", methods=['POST'])
def search():
    search  = request.form["search"]
    data=readFromDatabase(f"SELECT user FROM user WHERE name='{search}'")
    return render_template("/search.html", context={"search": data})

@app.route("/update", methods=['POST'])
def update():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]
    if name==session["username"] and password==confirm_password:
        writeToDatabase(f"UPDATE user SET name='{name}', email = '{email}', password = '{password}'")
        return redirect(url_for(username))
    return "failed to update"


@app.route('/profile_jmp')
def profile_jmp():
    return render_template('/profile.html')

@app.route('/homepage_jmp')
def homepage_jmp():
    return redirect(url_for('username'))

@app.route('/logout')
def logout():
    session.pop("username")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

