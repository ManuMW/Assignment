from flask import Flask, render_template, request

from utils.db_utils import connectDb, writeToDatabase, readFromDatabase

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
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
        return render_template("homepage.html", context = {"name": result[0][1]})


if __name__ == '__main__':
    app.run(debug=True)
