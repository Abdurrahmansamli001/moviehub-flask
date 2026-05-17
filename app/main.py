from flask import Flask, request, render_template
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
                return{"status": "success", "message": "login successfull"}
            else:
                return {"status": "failed", "message": "invalid credentials"}, 401
        else:
            return{"status": "failed", "message" : " username or  password missing"}, 400
          
    except mysql.connector.Error as db_error:
        return {"error": "database error"}, 500
    except Exception as e:
        return{"error": "Unknown error"}, 400




@app.route("/add-user", methods=["POST"] )
def add_user():
    try:
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:
            query = "INSERT INTO users (username , password) VALUES (%s , %s)"
            cursor.execute(query,  (username, password))
            db.commit()
            

            return {"status": "success", "message": "user created"}
        else:
            return{"status": "failed", "message": "missing fields"}, 400
         


    except mysql.connector.Error as db_error:
        return {"error": "database error"}, 500
    except Exception as e:
        return {"error": "Unknown error"}, 400    







if __name__ == "__main__":
    app.run(debug=True)