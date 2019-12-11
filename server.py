from flask import Flask,render_template
import psycopg2 as dbapi2


def executeSQL(sqlCode):
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')

        connection = dbapi2.connect(host="ec2-54-217-235-87.eu-west-1.compute.amazonaws.com", database="dfpj1pes2t0cba",
                              user="lwgysxzadqznqz", password="1d99ac08fda0c54c8e686f0057d88e65b9171c5bc3684551980e9b75ace378b9")

        cursor = connection.cursor()

        # Execute SQL code
        cursor.execute(sqlCode)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data

    except (Exception, dbapi2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

#def insertBike(title, color, frame_size, price, is_active, parts_id ,owner_nickname, city, country, model_id):


app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("homepage.html")

@app.route("/bikes" , methods=['GET'])
def bikes():
    bikes = executeSQL("""SELECT * FROM \"Country\"""")
    return render_template("deneme.html", bikes = bikes)


if __name__ == "__main__":
    app.run()



