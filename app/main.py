from flask import Flask
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


@app.route("/")
def home():
    return "server is running"


@app.route("/add-user")
def add_user():
    return ("true")

if __name__ == "__main__":
    app.run(debug=True)