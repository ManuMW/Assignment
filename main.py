from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "login_info"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']
            pt = mysql.connector.connect(host="127.0.0.1", user="root", passwd="root", database="login_info")
            ndb = pt.cursor()
            ndb.execute("SELECT * FROM user WHERE email=%s AND password=%s", (email, password))
            info = ndb.fetchall()
            if info[0] == email and info[1] == password:
                return "Login successfull"
            else:
                return "Login unsuccessfull"
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)