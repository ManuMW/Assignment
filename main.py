from flask import Flask, render_template, request
import mysql.connector as mysql

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
    mydb = mysql.connect(host="localhost", user="root", password="root", database="login_info")
    if request.method == 'POST':
        if 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM user WHERE email=%s AND password=%s", (email, password))
            for db in mycursor:
                print(db)
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)