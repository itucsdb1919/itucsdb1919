from flask import Flask,render_template
import psycopg2 as dbapi2


def connect(sqlCode):
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = dbapi2.connect(host="localhost", database="postgres", user="postgres", password="docker")

        cursor = connection.cursor()

        # Execute SQL code
        cursor.execute(sqlCode)
        value = cursor.fetchall()

    except (Exception, dbapi2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # close the communication with the PostgreSQL
        if (connection):
            cursor.close()
            connection.close()
    return value

if __name__ == '__main__':
    connect()

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("homepage.html")


@app.route('/login', methods=['GET', 'POST'])
def login():

@app.route('/profile', methods=['GET', 'POST'])
def profile():


@app.route("/bikes" , methods=['GET'])
def bikes():



if __name__ == "__main__":
    app.run()



