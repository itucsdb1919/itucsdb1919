
from flask import Flask,render_template,request, redirect, url_for
import psycopg2 as dbapi2
from datetime import datetime


def executeSQL(sqlCode,operation):
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = dbapi2.connect(host="ec2-54-217-235-87.eu-west-1.compute.amazonaws.com", database="dfpj1pes2t0cba",
                              user="lwgysxzadqznqz", password="1d99ac08fda0c54c8e686f0057d88e65b9171c5bc3684551980e9b75ace378b9")

        cursor = connection.cursor()
        
        # Execute SQL code
        cursor.execute(sqlCode)
        if(operation == "select"):
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            return data
        if(operation == "insert"):
            connection.commit()
            cursor.close()
            connection.close()  
            

    except (Exception, dbapi2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

#def insertBike(title, color, frame_size, price, is_active, parts_id ,owner_nickname, city, country, model_id):

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("homepage.html")

@app.route("/bikes", methods=['GET','POST'])
def bike_page():
    if request.method == "GET":
        sqlCode ="Select T1.title, T1.color,T1.owner_nickname, T3.image_url, T1.bike_id from \"Bikes\" as T1 LEFT JOIN \"Model\" as T2 ON T1.model_id = T2.model_id LEFT JOIN( select bike_id, MIN(image_url) as image_url from \"Bike_images\" GROUP BY bike_id )T3 ON T1.bike_id = T3.bike_id WHERE T1.is_active ='yes'"
        bikes = executeSQL(sqlCode, "select")

        return render_template("bikes.html", bikes = bikes)
    if request.method == "POST":
        bike_id = request.form['bike_id']
        detailSQL = "Select T1.title, T1.color,T1.frame_size,T1.price,T1.owner_nickname,T1.city,T1.country," \
                    "T2.year,T2.bike_type,T2.frame_material,T1.bike_id from \"Bikes\" as T1 LEFT JOIN \"Model\" as T2 ON T1.model_id" \
                    " = T2.model_id WHERE T1.is_active ='yes' AND T1.bike_id = " + bike_id
        imagesSQL = "SELECT image_url FROM \"Bike_images\" WHERE bike_id = " + bike_id
        detail = executeSQL(detailSQL, "select")
        images = executeSQL(imagesSQL, "select")

        return render_template("bike_detail.html", detail = detail, images = images)


@app.route("/cities" , methods=['GET'])
def statistics_city():
    statistics = executeSQL("""SELECT * FROM \"City\"""","select")
    name = "city"
    return render_template("statistics.html", statistics = statistics, name = name)

@app.route("/countries" , methods=['GET'])
def statistics_country():
    statistics = executeSQL("""SELECT * FROM \"Country\"""","select")
    name = "country"
    return render_template("statistics.html", statistics = statistics, name = name)

@app.route("/brands" , methods=['GET'])
def statistics_brand():
    statistics = executeSQL("""SELECT * FROM \"Brand\"""","select")
    name = "brand"
    return render_template("statistics.html", statistics = statistics, name = name)

@app.route("/register", methods=['GET','POST'])
def signup_page():
    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        nickname = request.form['nickname']
        image_url = request.form['image_url']
        print(name,surname,nickname,image_url)
        query = "INSERT INTO \"Profil\" (\"name\", \"surname\", \"profil_nickname\", \"profil_image\", \"number_of_bikes\", \"number_of_deals\")VALUES ('" + name + "', '" + surname + "', '"+ nickname + "','" + image_url + "', '0', '0')"
        print(query)
        executeSQL(query,"insert")
        return redirect(url_for('home_page'))
        
    else:
         return render_template("register.html")

@app.route("/help", methods=['GET','POST'])
def support_page():
    if request.method == "POST":
        nickname = request.form['nickname']
        topic = request.form['topic']
        details = request.form['details']
        dateTimeObj = datetime.now()
        thedate = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        print(details,nickname,topic,thedate)
        query = "INSERT INTO \"SupportTickets\" (writer_nickname, writen_date, support_text, topic, satisfaction_score, is_answered, support_worker_id)VALUES ('" + nickname + "','" + thedate + "', '" + details + "', '"+ topic + "','0', '0', '1')"
        # print(query)
        executeSQL(query,"insert")
        # return redirect(url_for('home_page'))
        return redirect(url_for('home_page'))
        
    else:
         return render_template("support.html")

@app.route("/login", methods=['GET','POST'])
def signin_page():
    if request.method == "POST":
        surname = request.form['surname']
        nickname = request.form['nickname']
        query = executeSQL("SELECT profil_nickname from \"Profil\" where surname = '"+ surname+"'", "select")
        if(query[0][0] == nickname):
            #succesfullL this code is complated
            #login_system()
            print(query[0][0],nickname)
            return render_template("homepage.html")
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")

if __name__ == "__main__":
    app.run()



