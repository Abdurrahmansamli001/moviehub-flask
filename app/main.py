from flask import Flask, request, render_template, redirect
import mysql.connector
from app import config

app = Flask(__name__)



db = mysql.connector.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME
)


cursor = db.cursor()


@app.route("/", methods=["GET"]) 
def home():
    query = "SELECT * FROM movies"
    cursor.execute(query)
    movies = cursor.fetchall()
    return render_template("index.html", movies=movies)




@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")





@app.route("/login", methods=["POST"]) 
def login():
    try:
        username =request.form.get("username")
        password=request.form.get("password")

        if username and password:

            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query,(username, password))
            user = cursor.fetchone()

            if user : 
               return redirect("/")  # ← Bunu yaz (login başarılı)
            else:
                return redirect("/signup")  # ← Bunu yaz (login başarısız)
        else:
                return redirect("/signup")  # ← Bunu yaz (eksik veri)
          
    except mysql.connector.Error as db_error:
        return redirect("/signup")
    except Exception as e:
        return redirect("/signup")




@app.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")




@app.route("/add-user", methods=["GET", "POST"] )
def add_user():
    try:
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:
            query = "INSERT INTO users (username , password) VALUES (%s , %s)"
            cursor.execute(query,  (username, password))
            db.commit()
            

            return redirect("/")  # ← Bunu yaz (signup başarılı)
        else:
            return redirect("/signup")  # ← Bunu yaz (eksik veri)



    except mysql.connector.Error as db_error:
        return redirect("/signup")
    except Exception as e:
        return redirect("/signup")    







if __name__ == "__main__":
    app.run(debug=True)