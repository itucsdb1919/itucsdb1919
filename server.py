from flask import Flask,render_template
import psycopg2 as dbapi2

def connect():
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = dbapi2.connect(host="localhost", database="postgres", user="postgres", password="docker")

        cur = conn.cursor()

        # display tables
        print('PostgreSQL database tables:')
        cur.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema = 'public'""")
        for table in cur.fetchall():
            print(table)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, dbapi2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    connect()

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("homepage.html")


if __name__ == "__main__":
    app.run()



