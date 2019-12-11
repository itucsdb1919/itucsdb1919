
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

if __name__ == "__main__":
    for element in executeSQL("""SELECT * FROM \"Country\""""):
        print(element)


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("homepage.html")

@app.route("/bikes")
def bike_page():
    bikes = executeSQL("""Select T1.title, T1.color,T1.owner_nickname, T3.image_url from \"Bikes\" as T1 LEFT JOIN \"Model\" as T2 ON T1.model_id = T2.model_id LEFT JOIN \"Bike_images\" as T3 ON T1.bike_id = T3.bike_id  WHERE T1.is_active ='yes';""")
    return render_template("bikes.html", bikes = bikes)


@app.route("/cities" , methods=['GET'])
def statistics_city():
    statistics = executeSQL("""SELECT * FROM \"City\"""")
    name = "city"
    return render_template("statistics.html", statistics = statistics, name = name)

@app.route("/countries" , methods=['GET'])
def statistics_country():
    statistics = executeSQL("""SELECT * FROM \"Country\"""")
    name = "country"
    return render_template("statistics.html", statistics = statistics, name = name)

@app.route("/brands" , methods=['GET'])
def statistics_brand():
    statistics = executeSQL("""SELECT * FROM \"Brand\"""")
    name = "brand"
    return render_template("statistics.html", statistics = statistics, name = name)

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

if __name__ == "__main__":
    app.run()



