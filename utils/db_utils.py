import mysql.connector as mysql


def connectDb():
    return mysql.connect(host="localhost", user="root", password="root", database="login_info")


def createSchema():
    sql = '''CREATE TABLE IF NOT EXISTS`login_info`.`user` (
      `id` INT NOT NULL,
      `Name` VARCHAR(30) NULL,
      `Email Address` VARCHAR(40) NULL,
      `Password` VARCHAR(40) NULL,
      PRIMARY KEY (`id`));'''


    connection = connectDb()
    cursor = connection.cursor()

    cursor.execute(sql)

    connection.commit()
    connection.close()


def writeToDatabase(cmd):
    conn = connectDb()
    cur = conn.cursor()
    cur.execute(cmd)
    conn.commit()
    conn.close()

def readFromDatabase(cmd):
    conn = connectDb()
    cursor = conn.cursor()
    cursor.execute(cmd)
    val = cursor.fetchall()
    conn.close()
    return val


createSchema()