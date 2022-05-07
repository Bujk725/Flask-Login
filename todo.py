# pip install flask komutuyla indiriyoruz
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
# pip install flask_mysqldb komutuyla indiriyoruz
from flask_mysqldb import MySQL
# pip install passlib komutuyla indiriyoruz
from passlib.hash import sha256_crypt
from functools import wraps 


app = Flask(__name__)

# Kullanıcı Giriş Dekoratörleri
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "login" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("index"))
    return decorated_function

# mysql bağlantı ayarları
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "todoapp"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

app.secret_key = "sadasld02!"


# Giriş Sayfası
@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        list_title = request.form.get("list_title")
        sorgu = "SELECT * FROM users WHERE username = %s and password = %s"
        cursor = mysql.connection.cursor()
        result = cursor.execute(sorgu, (username, password))
        data = cursor.fetchone()

        cursor.close()
        if(list_title):
            pass
        else:
            if (result) > 0:
                session["name"] = data["name"][0].upper()
                session["lastname"] = data["lastname"][0].upper()
                session["name2"] = data["name"].capitalize()
                session["lastname2"] = data["lastname"].capitalize()
                session["login"] = True
                session["password"] = False
                session["id"] = data["id"]
                return redirect(url_for("dashboard"))
                
            return render_template("index.html")
            
    else:
        return render_template("index.html")

# Kontrol Paneli
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    cursor = mysql.connection.cursor()
    sorgu = "SELECT todos.*, users.username FROM users_todo JOIN todos ON users_todo.todoID = todos.id JOIN users ON users_todo.userID = users.id WHERE userID = %s"
    sorgu2 = "SELECT * FROM users_todo WHERE userID = %s"
    sorgu3 = "SELECT * FROM users_todo JOIN users ON users_todo.userID = users.id JOIN todos ON todos.id= users_todo.todoID WHERE todoID = %s"

    result2 = cursor.execute(sorgu2,(session["id"],))
    todo2 = cursor.fetchall()
    result3 = cursor.execute(sorgu3,(todo2[0]["todoID"],))
    todo3 = cursor.fetchall()
    result = cursor.execute(sorgu,(session["id"],))
    
    if result > 0:
        todo = cursor.fetchall()
        print(todo)
        cursor.close()
        return render_template("dashboard.html", todo = todo, todo3 = todo3)
    else:
        return render_template("dashboard.html")


# Detay Sayfası
@app.route("/todos/<string:id>")
@login_required
def detail(id):
    cursor = mysql.connection.cursor()
    sorgu2 = "SELECT todos.*, users.username FROM users_todo JOIN todos ON users_todo.todoID = todos.id JOIN users ON users_todo.userID = users.id WHERE userID = %s"
    result2 = cursor.execute(sorgu2,(session["id"],))
    todo2 = cursor.fetchall()
    sorgu = "SELECT * FROM todos WHERE id=%s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        todo = cursor.fetchone()
        sorgu1 = "SELECT * FROM todos WHERE title = %s"
        result1 = cursor.execute(sorgu1,(todo["title"],))
        todo1 = cursor.fetchall()
        cursor.close()
        return render_template("todos.html", todo1 = todo1, todo = todo2)
    else:
        return render_template("todos.html")


# Liste Silme
@app.route("/del/<string:id>")
def delete(id):
    sorgu = "DELETE FROM todos WHERE id = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(sorgu,(id,))
    mysql.connection.commit()
    return render_template("todos.html")

# Kullanıcı Kayıt
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        password = request.form.get("password")
        confirm = request.form.get("password_confirm")
        email = request.form.get("email")
        if password == confirm:
            sorgu = "INSERT INTO users(username,name,lastname,password,email) VALUES(%s,%s,%s,%s,%s)"
            cursor = mysql.connection.cursor()
            cursor.execute(sorgu,(username, name, lastname, password, email))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("index"))
        else:
            return render_template("register.html")
    else:
        return render_template("register.html")

# Çıkış yapma
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# Şifre sıfırlama
@app.route("/forget", methods = ["GET","POST"])
def forget():
    if request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        sorgu = "SELECT * FROM users WHERE username = %s AND name = %s AND lastname = %s AND email = %s"
        cursor = mysql.connection.cursor()
        result = cursor.execute(sorgu,(username,name,lastname,email))
        data = cursor.fetchone()
        if(result > 0):
            if (data["password"] == ""):
                return render_template("forget.html", message=2)
            elif (data["password"]):
                session["password"] = data["password"]
                return redirect(url_for("index"))
        else:
            return render_template("forget.html", message = 1)
    else:
        return render_template("forget.html")

if __name__ == "__main__":
    app.run(debug =True)