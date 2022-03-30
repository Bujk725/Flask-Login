
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
# pip install flask_mysqldb komutuyla indiriyoruz
from flask_mysqldb import MySQL
# pip install passlib komutuyla indiriyoruz
from passlib.hash import sha256_crypt
app = Flask(__name__)

# mysql bağlantı ayarları
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "todoapp"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        sorgu = "SELECT * FROM users WHERE username = %s and password = %s"
        cursor = mysql.connection.cursor()
        result = cursor.execute(sorgu, (username, password))

        if (result) > 0:
            return redirect(url_for("todos"))
        
        return render_template("index.html")
        
    else:
        return render_template("index.html")

@app.route("/todos", methods=["GET", "POST"])
def todos():
    return render_template("todos.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        print("deneme")
        username = request.form.get("username")
        name = request.form.get("name")
        firstname = request.form.get("firstname")
        password = request.form.get("password")
        confirm = request.form.get("password_confirm")
        email = request.form.get("email")
        if password == confirm:
            sorgu = "INSERT INTO users(username,name,lastname,password,email) VALUES(%s,%s,%s,%s,%s)"
            cursor = mysql.connection.cursor()
            cursor.execute(sorgu,(username, name, firstname, password, email))
            mysql.connection.commit()
            return redirect(url_for("index"))
        else:
            return render_template("register.html")
    else:
        print("get")
        return render_template("register.html")

if __name__ == "__main__":
    app.run(debug =True)