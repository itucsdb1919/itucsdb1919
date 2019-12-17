
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
        if(operation == "insert" or "update"):
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
            rented_bike_id = bike_id[:-4]
            renting_user = session['my_profile_id']
            dealSQL = "INSERT INTO \"Deals\" Select price,'NULL' As payment_method,NOW() As date_taken,NOW() As date_return,0 As duration_as_hour,'t' As " \
                      "is_active,owner_nickname,(select profil_nickname from \"Profil\" where profil_id = " + str(renting_user) + " ) as " \
                      "renter_nickname,(select phone_num from \"Contact\" where profil = (select profil_id from  \"Profil\" where profil_nickname = owner_nickname )) " \
                      "as owner_phone,(select phone_num from \"Contact\" where profil = (select profil_id from  \"Profil\" where profil_nickname = " \
                      "(select profil_nickname from \"Profil\" where profil_id = " + str(renting_user) + " ) )) as renter_phone, bike_id, city, country " \
                      "from \"Bikes\" where bike_id = '" + rented_bike_id + "'"
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
        query = "INSERT INTO \"Profil\" (\"name\", \"surname\", \"profil_nickname\", \"profil_image\", \"number_of_bikes\", \"number_of_deals\")VALUES ('" + name + "', '" + surname + "', '"+ nickname + "','" + '' + "', '0', '0')"
        executeSQL(query,"insert")
        query = "SELECT profil_id from \"Profil\" WHERE profil_nickname = '" + nickname +"'"
        query = executeSQL(query,"select")
        print(query)
        sqldelete = "INSERT INTO  \"Contact\" (is_active, profil)VALUES('t','"+ str(query[0][0]) +"')"
        executeSQL(sqldelete,"update")
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
        query = executeSQL("SELECT T1.profil_nickname,T1.profil_id from \"Profil\" as T1 LEFT JOIN \"Contact\"  AS T2 ON T1.profil_id = T2.profil where T1.surname ='" + surname + "'AND T2.is_active = 't'","select")
        if(query[0][0] == nickname):
            #succesfullL this code is complated
            #login_system()
            session['my_profile_id'] = query[0][1]
            session['logged_in'] = True
            session['nickname'] = nickname
            print(query[0][0],nickname,query[0][1])
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
        session.pop('my_profile_id', None)
        flash('You were logged out')
        return redirect(url_for("signin_page"))
    else:
        return redirect(url_for("home_page"))        


@app.route("/mybikes", methods=['GET','POST'])
def mybikes_page():
    if(session['logged_in']):
        if request.method == "GET":
            sqlCode ="Select T1.title, T1.color,T1.owner_nickname, T3.image_url, T1.bike_id from \"Bikes\" as T1 LEFT JOIN \"Model\" as T2 ON T1.model_id = T2.model_id LEFT JOIN( select bike_id, MIN(image_url) as image_url from \"Bike_images\" GROUP BY bike_id )T3 ON T1.bike_id = T3.bike_id WHERE T1.owner_nickname ='" + session['nickname'] + "'"           
            bikes = executeSQL(sqlCode, "select")
            return render_template("mybikes.html", bikes = bikes)
        if request.method == "POST":
            bike_id = request.form['bike_id']
            if bike_id[-3:] != "del":
                detailSQL = "Select T1.title, T1.color,T1.frame_size,T1.price,T1.owner_nickname,T1.city,T1.country," \
                            "T2.year,T2.bike_type,T2.frame_material,T1.bike_id from \"Bikes\" as T1 LEFT JOIN \"Model\" as T2 ON T1.model_id" \
                            " = T2.model_id WHERE T1.is_active ='yes' AND T1.bike_id = " + bike_id
                imagesSQL = "SELECT image_url FROM \"Bike_images\" WHERE bike_id = " + bike_id
                detail = executeSQL(detailSQL, "select")
                images = executeSQL(imagesSQL, "select")

                return render_template("bike_detail.html", detail=detail, images=images)

            if bike_id[-3:] == "del":

                delSQL = "Delete from \"Bikes\" where bike_id = " + bike_id[:-3]
                executeSQL(delSQL, "insert")

                return redirect(url_for('mybikes_page'))


@app.route("/addbike", methods=['GET','POST'])
def addbikes_page():
    if(session['logged_in']):
        if request.method == "GET":
            return render_template("addbike.html")
        if request.method == "POST":
            title = request.form['title']
            color = request.form['color']        
            image_url = request.form['image_url'] 
            frame_size = request.form['frame_size']
            price = request.form['price']         
            city = request.form['city']
            country = request.form['country'] 
            model_name = request.form['model_name']
            year = request.form['year']        
            bike_type = request.form['bike_type']
            frame_material = request.form['frame_material']
            target_customer = request.form['target_customer']
            brand = request.form['brand']         
            gidon = request.form['gidon']
            aktarici = request.form['aktarici'] 
            sele = request.form['sele'] 
            jant = request.form['jant'] 
            lastik = request.form['lastik'] 
            pedal = request.form['pedal'] 

            modelsql = "INSERT INTO \"Model\"(model_name, year, bike_type,frame_material, target_customer, brand, country)VALUES ('" + model_name + "','" + year + "', '" + bike_type + "', '" + frame_material + "', '" + target_customer + "', '" + brand + "', '" + country + "')"
            partssql = "INSERT INTO \"Parts\"(gidon, aktarici, sele,jant, lastik, pedal)VALUES ('" + gidon + "','" + aktarici + "', '" + sele + "', '"+ jant + "', '"+ lastik + "', '"+ pedal +"')"
            executeSQL(modelsql,"insert" )
            executeSQL(partssql,"insert" )

            
            model_id = executeSQL("SELECT MAX(model_id) from \"Model\"  ","select" )
            parts_id = executeSQL("SELECT MAX(parts_id) from \"Parts\"  ","select" )
            parts_id = parts_id[0][0]
            model_id = model_id[0][0]
            print (parts_id, model_id)
            bikesql = "INSERT INTO \"Bikes\"(is_active, title, color, frame_size, price, parts_id ,owner_nickname ,city, country,model_id)VALUES ('t','" + title + "','" + color + "', '" + frame_size + "', '"+ price + "', '"+ str(parts_id) + "', '"+ str(session['nickname']) + "', '"+ city + "', '"+ country + "', '"+ str(model_id) + "')"
            executeSQL(bikesql,"insert" )
            bike_id = executeSQL("SELECT MAX(bike_id) from \"Bikes\"  ","select")
            bike_id = bike_id[0][0]
            imagesql = "INSERT INTO \"Bike_images\"(bike_id,image_url)VALUES('"+str(bike_id)+"','"+str(image_url)+"')"
            executeSQL(imagesql,"insert" )
            
            return redirect(url_for("mybikes_page")) 


@app.route("/mydeals", methods=['GET'])
def mydeals_page():
    if(session['logged_in']):
        session['logged_in'] = False
        session.pop('nickname', None)
        flash('You were logged out')
        return redirect(url_for("signin_page"))
    else:
        return redirect(url_for("home_page"))

@app.route("/settings", methods=['GET','POST'])
def settings_page():
    if(session['logged_in']):
        if request.method == "GET":
            sqlprofile = executeSQL("SELECT name, surname, profil_nickname, profil_image, number_of_bikes, number_of_deals, profil_id from \"Profil\" WHERE profil_nickname = '" + session['nickname']+"'" ,"select")
            sqlcontact = executeSQL("SELECT contact_id, e_mail, is_active, instagram_url, facebook_url, twitter_url, country, profil, city, phone_num from \"Contact\" WHERE profil = " + str(session['my_profile_id']),"select")
            return render_template("settings.html",sqlprofile = sqlprofile, sqlcontact = sqlcontact)
        if request.method == "POST":
            name = request.form['name']
            surname = request.form['surname']
            profile_image = request.form['profile_image']
            email = request.form['email']
            instagram_url = request.form['instagram_url']
            facebook_url = request.form['facebook_url']
            twitter_url = request.form['twitter_url']
            country = request.form['country']
            city = request.form['city']
            phone_num = request.form['phone_num']
            sqlprofile = "UPDATE \"Profil\" SET name = '" + name + "', surname = '" + surname + "', profil_image = '" + profile_image + "' WHERE profil_id = " + str(session['my_profile_id'])
            sqlcontact = "UPDATE \"Contact\" SET e_mail = '" + email + "', instagram_url = '" + instagram_url + "', facebook_url = '" + facebook_url + "', twitter_url = '" + twitter_url + "', country = '" + country + "', city = '" + city + "', phone_num = '" + phone_num + "' WHERE profil = " + str(session['my_profile_id'])
            executeSQL(sqlprofile,"update")
            executeSQL(sqlcontact,"update")
            return redirect(url_for("settings_page"))

@app.route("/delete_account_28392", methods=['GET'])
def delete_page():
    if(session['logged_in']):
        if request.method == "GET":
            sqldelete = "UPDATE \"Contact\" SET is_active = 'f' WHERE profil = " + str(session['my_profile_id'])
            executeSQL(sqldelete,"update")
            return redirect(url_for("home_page"))


if __name__ == "__main__":
    app.run()



