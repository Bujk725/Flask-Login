
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
        title = request.form.get("list-title")
        username = request.form.get("username")
        password = request.form.get("password")
        sorgu = "SELECT * FROM users WHERE username = %s and password = %s"
        sorgu2 = "SELECT * FROM todos WHERE userId = %s and title = %s"
        cursor = mysql.connection.cursor()
        result = cursor.execute(sorgu, (username, password))
        veri = cursor.fetchone()
        try:
            result2 = cursor.execute(sorgu2, (veri["id"], title))
            if (result and result2) > 0:
                return redirect(url_for("todos"))
            else:
                return render_template("index.html")
        except:
            if (result and result2) > 0:
                return redirect(url_for("todos"))
            else:
                return render_template("index.html")
        
    else:
        return render_template("index.html")

@app.route("/todos", methods=["GET", "POST"])
def todos():
    return render_template("todos.html")


if __name__ == "__main__":
    app.run(debug =True)