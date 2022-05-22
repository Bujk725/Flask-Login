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
        sorgu = "SELECT * FROM users WHERE username = %s"
        cursor = mysql.connection.cursor()
        result = cursor.execute(sorgu, (username,))
        data = cursor.fetchone()
        cursor.close()
        if(list_title):
            cursor = mysql.connection.cursor()
            sorgu2 = "SELECT * FROM users_todo_head WHERE userID = %s"
            cursor.execute(sorgu2,(data["id"],))
            result2 = cursor.fetchone()
            if result2:
                if result2["todo_head_id"] == int(list_title):
                    session["name"] = data["name"][0].upper()
                    session["lastname"] = data["lastname"][0].upper()
                    session["name2"] = data["name"].capitalize()
                    session["lastname2"] = data["lastname"].capitalize()
                    session["login"] = True
                    session["password"] = False
                    session["id"] = data["id"]
                    return redirect(url_for("detail", id = result2["todo_head_id"]))
                else:
                    return render_template("index.html")
            else:
                return render_template("index.html")
        else:
            if (result) > 0:
                if  sha256_crypt.verify(password, data["password"]): 
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
    sorgu = "SELECT * FROM users_todo_head JOIN todo_head ON users_todo_head.todo_head_id = todo_head.id WHERE userid = %s"
    sorgu2 = "SELECT todo_head.title, userID, users.username FROM `users_todo_head` JOIN users ON users_todo_head.userID = users.id JOIN todo_head ON users_todo_head.todo_head_id = todo_head.id WHERE todo_head_id IN (SELECT todo_head_id from users_todo_head WHERE userID = %s) and userID != %s"
    result = cursor.execute(sorgu,(session["id"],))
    if result > 0:
        todo = cursor.fetchall()
        resutl2 = cursor.execute(sorgu2,(session["id"],session["id"]))
        todo2 = cursor.fetchall()

        # Kategori çeşit sayısı

        freelancerSorgu = "SELECT * FROM users_todo_head JOIN todo_head ON users_todo_head.todo_head_id = todo_head.id where userID = %s and todo_head.category = 'Serbest Çalışma' "
        freelancerSonuç = cursor.execute(freelancerSorgu,(session["id"],))
        freelancer = cursor.fetchall()


        hobiSorgu = "SELECT * FROM users_todo_head JOIN todo_head ON users_todo_head.todo_head_id = todo_head.id where userID = %s and todo_head.category = 'Hobi' "
        gobiSonuç = cursor.execute(hobiSorgu,(session["id"],))
        hobi = cursor.fetchall()



        işSorgu = "SELECT * FROM users_todo_head JOIN todo_head ON users_todo_head.todo_head_id = todo_head.id where userID = %s and todo_head.category = 'İş' "
        işSonuç = cursor.execute(işSorgu,(session["id"],))
        iş = cursor.fetchall()



        cursor.close()
        return render_template("dashboard.html", todo = todo, todo2 = todo2, freelancer = len(freelancer), hobi = len(hobi), iş = len(iş))
    else:
        return render_template("dashboard.html")


# Detay Sayfası
@app.route("/todos/<string:id>", methods=["GET", "POST"])
@login_required
def detail(id):
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM todo JOIN todo_head ON todo.todo_head_id = todo_head.id WHERE todo_head_id = %s"
    sorgu2 = "SELECT * FROM users_todo_head JOIN todo_head ON users_todo_head.todo_head_id = todo_head.id WHERE userid = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        todo = cursor.fetchall()
        cursor.execute(sorgu2,(session["id"],))
        todo2 = cursor.fetchall()
        cursor.close()
        return render_template("todos.html",todo = todo, todo2 = todo2)   
    else:
        sorgu3 = "DELETE FROM todo_head WHERE id = %s"
        cursor.execute(sorgu3,(id,))
        mysql.connection.commit()
        sorgu4 = "DELETE FROM users_todo_head WHERE todo_head_id = %s"
        cursor.execute(sorgu4,(id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("dashboard"))


# Liste Silme
@app.route("/del/<string:id>")
@login_required
def delete(id):
    cursor = mysql.connection.cursor()
    sorgu2 = "SELECT todo_head_id FROM todo where id = %s"
    cursor.execute(sorgu2,(id,))
    result = cursor.fetchone()
    result = result["todo_head_id"]
    sorgu = "DELETE FROM todo WHERE id = %s"
    cursor.execute(sorgu,(id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("detail", id = result))


# Liste Tamamlama
@app.route("/edit/<string:id>")
@login_required
def edit(id):
    cursor = mysql.connection.cursor()
    sorgu = "SELECT todo_head_id FROM todo where id = %s"
    cursor.execute(sorgu,(id,))
    result = cursor.fetchone()
    result = result["todo_head_id"]
    sorgu2 = "SELECT complete FROM todo WHERE id = %s "
    cursor.execute(sorgu2,(id,))
    result2 = cursor.fetchone()
    result2 = result2["complete"]
    result2 = not(result2)
    sorgu3 = "UPDATE todo SET complete = %s WHERE id = %s"
    cursor.execute(sorgu3,(result2,id))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("detail", id = result))
 
# Görev ve Kullanıcı Ekle
@app.route("/addTask/<string:id>", methods=["GET","POST"])
@login_required
def addTask(id):
    usernameAndTask = request.form.get("usernameAndTask")
    cursor = mysql.connection.cursor()
    if(usernameAndTask.startswith("@")):
        usernameAndTask = usernameAndTask.split(",")
        for i in usernameAndTask:
            x = i.replace("@","")
            sorgu = "SELECT id FROM users WHERE username = %s"
            cursor.execute(sorgu,(x,))
            result = cursor.fetchone()
            result = result["id"]
            sorgu2 = "INSERT INTO users_todo_head(userID, todo_head_id) VALUES(%s,%s)"
            cursor.execute(sorgu2,(result,id))
            mysql.connection.commit()
    else:
        sorgu = "INSERT INTO todo(todo_head_id, content, complete) VALUES(%s,%s, 0)"
        cursor.execute(sorgu,(id,usernameAndTask))
        mysql.connection.commit()
        cursor.close()
    return redirect(url_for("detail", id = id))


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
            password = sha256_crypt.encrypt(password)
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
        session["userPassword"] = username
        print(session["userPassword"])
        if(result > 0):
            if (data["password"] == ""):
                return render_template("forget.html", message=2)
            elif (data["password"]):
                session["password"] = data["password"]
                return redirect(url_for("newPassword"))
        else:
            return render_template("forget.html", message = 1)
    else:
        return render_template("forget.html")

# Yeni Parola
@app.route("/newPassword", methods = ["GET","POST"])
def newPassword():
    if request.method == "POST":
        newPassword = request.form.get("new_password")
        newPassword_confirm = request.form.get("new_confirm")
        if newPassword == newPassword_confirm:
            print(session["userPassword"])
            crypt_password = sha256_crypt.encrypt(newPassword)
            cursor = mysql.connection.cursor()
            sorgu = "UPDATE users SET password = %s WHERE username = %s"
            cursor.execute(sorgu,(crypt_password,session["userPassword"]))
            mysql.connection.commit()
            return redirect(url_for("index"))
        else:
            return render_template("newPassword.html")
    else:
        return render_template("newPassword.html")

# Yeni liste oluşturma
@app.route("/newlist", methods = ["GET","POST"])
@login_required
def newlist():
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM users_todo_head JOIN todo_head ON users_todo_head.todo_head_id = todo_head.id WHERE userid = %s"
    result = cursor.execute(sorgu,(session["id"],))
    todo = cursor.fetchall()
    if request.method == "POST":
        title = request.form.get("title")
        kategori = request.form.get("category")
        team = request.form.get("teamUsername")
        content = request.form.get("firstodo")
        x = team.split(',')

        sorgu2 = "INSERT INTO todo_head(title,category) VALUES(%s,%s)"
        result2 = cursor.execute(sorgu2,(title,kategori))
        mysql.connection.commit()

        sorgu3 = "SELECT id FROM todo_head WHERE title = %s"
        resut3 = cursor.execute(sorgu3,(title,))
        data = cursor.fetchone()

        sorgu4 = "INSERT INTO users_todo_head(userID,todo_head_id) VALUES(%s,%s)"
        result4 = cursor.execute(sorgu4,(session["id"], data["id"]))
        mysql.connection.commit()
        if team:
            idlist = []
            for i in x:
                sorgu5 = "SELECT id FROM users WHERE username = %s "
                cursor.execute(sorgu5,(i,))
                ID = cursor.fetchone()
                if ID != None :
                    idlist.append(ID["id"])
            if idlist:
                for a in idlist:
                    sorgu6 = "INSERT INTO users_todo_head(userID,todo_head_id) VALUES(%s,%s)"
                    result6 = cursor.execute(sorgu6,(a, data["id"]))
                    mysql.connection.commit()   
        sorgu7 = "INSERT INTO todo(todo_head_id, content, complete) VALUES(%s,%s, 0)"
        cursor.execute(sorgu7,(data["id"],content))
        mysql.connection.commit()
        cursor.close()
        return render_template("newlist.html", todo = todo)
    else:
        return render_template("newlist.html", todo = todo)

if __name__ == "__main__":
    app.run(debug =True)