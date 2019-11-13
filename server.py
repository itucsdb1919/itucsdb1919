from flask import Flask,render_template
import psycopg2 as dbapi2
from config import config


def connect():
    # Connect to the PostgreSQL database server
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("homepage.html")


if __name__ == "__main__":
    app.run()
