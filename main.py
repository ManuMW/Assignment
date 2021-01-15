from flask import Flask, render_template, redirect, url_for, session, request
import mysql.connector



app = Flask(__name__)

app.config["MYSQL_HOST"] = "localmain"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "login"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']
            cursor = mysql.connector.connect(host="localmain", user="root", password="root", port="3306")
            cursor.execute("SELECT * FROM user WHERE email=%s AND password=%s",(email,password))
            info = cursor.fetchone()
            if info['email'] == email and info['password'] == password:
                return "Login successfull"
            else:
                return "Login unsuccessfull"

    return render_template("login.html")




if __name__ == '__main__':
    app.run(debug=True)