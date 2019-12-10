from flask import Flask,render_template
import psycopg2 as dbapi2


def connect():
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = dbapi2.connect(host="localhost", database="postgres", user="postgres", password="docker")

        cursor = connection.cursor()

        # Execute SQL code
        cursor.execute("""SELECT version();""")
        version = cursor.fetchone()
        print("Postgress version: ",version)
        cursor.close()
        connection.close()

    except (Exception, dbapi2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


app = Flask(__name__)

if __name__ == "__main__":
    connect()


@app.route("/")
def home_page():
    return render_template("homepage.html")

@app.route("/bikes" , methods=['GET'])
def bikes():
    return render_template("homepage.html")


if __name__ == "__main__":
    app.run()



