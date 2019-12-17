
from flask import Flask,render_template,request, redirect, url_for, session,flash
import psycopg2 as dbapi2
from datetime import datetime
import os


def executeSQL(sqlCode,operation):
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        url = os.getenv("DATABASE_URL")
        connection = dbapi2.connect(url)
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
app.secret_key = "super secret key"

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("homepage.html")

@app.route("/bikes", methods=['GET','POST'])
def bike_page():
    if request.method == "GET":
        bikesSQL ="Select T1.title, T1.color,T1.owner_nickname, T3.image_url, T1.bike_id from \"Bikes\" as T1 LEFT JOIN \"Model\" as T2 ON T1.model_id = T2.model_id " \
                 "LEFT JOIN( select bike_id, MIN(image_url) as image_url from \"Bike_images\" GROUP BY bike_id )T3 ON T1.bike_id = T3.bike_id WHERE T1.is_active ='yes'"
        brandSQL = "Select brand_name from \"Brand\""
        citySQL = "Select city_name from \"City\""
        colorSQL = "Select color from \"Bikes\""
        bikes = executeSQL(bikesSQL, "select")
        brands = executeSQL(brandSQL, "select")
        cities = executeSQL(citySQL, "select")
        colors = executeSQL(colorSQL, "select")

        return render_template("bikes.html", bikes = bikes, brands=brands, cities=cities, colors=colors)

    if request.method == "POST":
        bike_id = request.form['bike_id']

        if bike_id[-2:] != "up" and bike_id[-4:] != "down" and bike_id[-4:] != "rent" and bike_id[-4:] != "fltr" and bike_id[-4:] != "brnd" and bike_id[-4:] != "city" and bike_id[-4:] != "clor" and bike_id[-4:] != "deal":
            detailSQL = "Select T1.title, T1.color,T1.frame_size,T1.price,T1.owner_nickname,T1.city,T1.country," \
                        "T2.year,T2.bike_type,T2.frame_material,T1.bike_id from \"Bikes\" as T1 LEFT JOIN \"Model\" as T2 ON T1.model_id" \
                        " = T2.model_id WHERE T1.is_active ='yes' AND T1.bike_id = " + bike_id
            imagesSQL = "SELECT image_url FROM \"Bike_images\" WHERE bike_id = " + bike_id
            commentsSQL = "SELECT  image_url, title,  comment , writer_nickname,  written_date, up_vote, down_vote, comment_id FROM \"Comments\" WHERE bike_id = " + bike_id
            detail = executeSQL(detailSQL, "select")
            images = executeSQL(imagesSQL, "select")
            comments = executeSQL(commentsSQL, "select")

            return render_template("bike_detail.html", detail= detail, images=images, comments= comments)

        elif bike_id[-2:] == "up" or bike_id[-4:] == "down":
            if bike_id[-2:] == "up":
                voteSQL = "UPDATE \"Comments\" SET up_vote = up_vote + 1 WHERE comment_id =" + bike_id[:-2]
            if bike_id[-4:] == "down":
                voteSQL = "UPDATE \"Comments\" SET down_vote = down_vote + 1 WHERE comment_id =" + bike_id[:-4]
            executeSQL(voteSQL, "insert")

            return redirect(url_for('bike_page'))

        elif bike_id[-4:] == "deal":
            print("================")
            split_id = bike_id.split('*')
            rented_bike_id = split_id[0]
            print("rented bike ",rented_bike_id)
            renting_user = session.
            print("user",renting_user)
            dealSQL = "INSERT INTO \"Deals\" Select price,'NULL' As payment_method,NOW() As date_taken,NOW() As date_return,0 As duration_as_hour,'t' As " \
                      "is_active,owner_nickname,(select profil_nickname from \"Profil\" where profil_id = " + renting_user + " ) as " \
                      "renter_nickname,(select phone_num from \"Contact\" where profil = (select profil_id from  \"Profil\" where profil_nickname = owner_nickname )) " \
                      "as owner_phone,(select phone_num from \"Contact\" where profil = (select profil_id from  \"Profil\" where profil_nickname = " \
                      "(select profil_nickname from \"Profil\" where profil_id = " + renting_user + " ) )) as renter_phone, bike_id, city, country " \
                      "from \"Bikes\" where bike_id = " + rented_bike_id
            executeSQL(dealSQL, "insert")

            return redirect(url_for('bike_page'))

        #elif bike_id[-4:] == "fltr":
        #    filter_id = bike_id[:-4]
        #    filterSQL = ""
        #    filter = executeSQL(filterSQL, 'select')
        #
        #    return render_template("bikes_filter.html" , filter= filter)

        elif bike_id[-4:] == "brnd":
            filter_id = bike_id[:-4]

            filterSQL = "Select T1.title, T1.color,T1.owner_nickname, T3.image_url, T1.bike_id from \"Bikes\" as T1 LEFT JOIN \"Model\" as T2 ON T1.model_id = T2.model_id " \
                        "LEFT JOIN( select bike_id, MIN(image_url) as image_url from \"Bike_images\" GROUP BY bike_id )T3 ON T1.bike_id = T3.bike_id WHERE T1.is_active ='yes' AND T2.brand ='" + filter_id +"'"
            filter = executeSQL(filterSQL, 'select')

            return render_template("bikes_filter.html", filter=filter)

        elif bike_id[-4:] == "city":
            filter_id = bike_id[:-4]
            filterSQL = "Select T1.title, T1.color,T1.owner_nickname, T3.image_url, T1.bike_id from \"Bikes\" as T1 LEFT JOIN \"Model\" as T2 ON T1.model_id = T2.model_id " \
                        "LEFT JOIN( select bike_id, MIN(image_url) as image_url from \"Bike_images\" GROUP BY bike_id )T3 ON T1.bike_id = T3.bike_id WHERE T1.is_active ='yes' AND T1.city = '"  + filter_id + "'"
            filter = executeSQL(filterSQL, 'select')

            return render_template("bikes_filter.html", filter=filter)

        elif bike_id[-4:] == "clor":
            filter_id = bike_id[:-4]
            filterSQL = "Select T1.title, T1.color,T1.owner_nickname, T3.image_url, T1.bike_id from \"Bikes\" as T1 LEFT JOIN \"Model\" as T2 ON T1.model_id = T2.model_id " \
                        "LEFT JOIN( select bike_id, MIN(image_url) as image_url from \"Bike_images\" GROUP BY bike_id )T3 ON T1.bike_id = T3.bike_id WHERE T1.is_active ='yes' AND T1.color = '"  + filter_id + "'"
            filter = executeSQL(filterSQL, 'select')

            return render_template("bikes_filter.html", filter=filter)


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
    session['logged_in'] = False
    if request.method == "POST":
        surname = request.form['surname']
        nickname = request.form['nickname']
        query = executeSQL("SELECT profil_nickname from \"Profil\" where surname = '"+ surname+"'", "select")
        if(query[0][0] == nickname):
            #succesfullL this code is complated
            #login_system()
            session['logged_in'] = True
            session['nickname'] = nickname
            print(query[0][0],nickname)
            return render_template("homepage.html")
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/logout", methods=['GET'])
def logout_page():
    if(session['logged_in']):
        session['logged_in'] = False
        session.pop('nickname', None)
        flash('You were logged out')
        return redirect(url_for('signin_page'))
    else:
        return redirect(url_for(home_page))        


@app.route("/mybikes", methods=['GET','POST'])
def mybikes_page():
    if(session['logged_in']):
        if request.method == "GET":
            sqlCode ="Select T1.title, T1.color,T1.owner_nickname, T3.image_url, T1.bike_id from \"Bikes\" as T1 LEFT JOIN \"Model\" as T2 ON T1.model_id = T2.model_id LEFT JOIN( select bike_id, MIN(image_url) as image_url from \"Bike_images\" GROUP BY bike_id )T3 ON T1.bike_id = T3.bike_id WHERE T1.owner_nickname ='" + session['nickname'] + "'"           
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


@app.route("/mydeals", methods=['GET'])
def mydeals_page():
    if(session['logged_in']):
        session['logged_in'] = False
        session.pop('nickname', None)
        flash('You were logged out')
        return redirect(url_for('signin_page'))
    else:
        return redirect(url_for(home_page))

@app.route("/settings", methods=['GET','POST'])
def settings_page():
    if(session['logged_in']):
        if request.method == "GET":
            return render_template("settings.html")
        if request.method == "POST":
            return redirect(url_for(home_page))

if __name__ == "__main__":
    app.run()



