from flask import Flask,render_template,request,url_for,redirect,make_response,session,url_for,flash,jsonify
import mysql.connector
import openai
import stripe
# from werkzeug import secure_filename
from werkzeug.utils import secure_filename
import chat_bot
from flask_cors import CORS

from flask import flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

import datetime

app = Flask(__name__)
CORS(app)
app.secret_key = "flash message"
app.config['SECRET_KEY'] = 'DECORATORS'

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/offers")
def offers():
    return render_template("offers.html")

@app.route("/aboutus")
def aboutus():
    return render_template("about.html")

@app.route("/contactus")
def contactus():
    return render_template("contactus.html")

@app.route("/Bus",methods=["GET","POST"])
def bus():
    if(request.method=="GET"):
        return render_template("Bus.html")
    else:
        From = request.form["From"]
        To = request.form["To"]
        Date = request.form["date"]
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
        try:       
            mycursor = con.cursor()
            sql = "insert into busdata values (%s,%s,%s)"
            val = (From,To,Date)
            mycursor.execute(sql,val)
            return redirect("ShowProducts/1")
        finally:
            con.close()

@app.route("/seatbooking",methods=["GET","POST"])
def seatbooking():
    if(request.method=="GET"):
        return render_template("/seatbooking.html")
    else:
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak") 
        try:
            mycursor = con.cursor()
            seatno = request.form.getlist("A")
            size=len(seatno)
            for i in range(size):
                str=seatno[i]+''+str

            sql = "insert into seatbook (seatno) values (%s)"
            val = (str)
            mycursor.execute(sql,val)
            return redirect("/user/ViewDetails/1")
        finally:
            con.close()


@app.route("/Trains",methods=["GET","POST"])
def train():
    if (request.method=="GET"):
        return render_template("Trains.html")
    else:
        From = request.form["From"]
        To = request.form["To"]
        Date = request.form["date"] 
        Classes = request.form["classes"]
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")
        try:
            mycursor = con.cursor()
            sql = "insert into traindata values (%s,%s,%s,%s)"
            val = (From,To,Date,Classes)
            mycursor.execute(sql,val)
            return redirect("ShowProducts/2")
        finally:
            con.close()

@app.route("/Flights",methods=["GET","POST"])
def flights():
    if (request.method=="GET"):
        return render_template("Flights.html")
    else:
        From = request.form["from"]
        To = request.form["to"]
        DepatureDate = request.form["date1"] 
        ReturnDate = request.form["date2"]
        Travellers = request.form["travellers"]
        Class = request.form["class"]
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")
        try:
            mycursor = con.cursor()
            sql = "insert into flightdata values (%s,%s,%s,%s,%s,%s)"
            val = (From,To,DepatureDate,ReturnDate,Travellers,Class)
            mycursor.execute(sql,val)
            return redirect("ShowProducts/3")
        finally:
            
            con.close()

@app.route("/Hotels",methods=["GET","POST"])
def hotels():
    if (request.method=="GET"):
        return render_template("Hotels.html")
    else:
        Destination = request.form["destination"]
        CheckIn = request.form["date1"]
        CheckOut = request.form["date2"] 
        Rooms = request.form["rooms"]
        Adults = request.form["adults"]
        Children = request.form["children"]
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")
        try:
            mycursor = con.cursor()
            sql = "insert into hoteldata values (%s,%s,%s,%s,%s,%s)"
            val = (Destination,CheckIn,CheckOut,Rooms,Adults,Children)
            mycursor.execute(sql,val)
            return redirect("ShowProducts/4")
        finally:
            con.close()


@app.route("/cookies",methods=["GET","POST"])
def cookieDemo():
    if(request.method=="GET"):
        return render_template("cookie.html")
    else:
        fname = request.form["email"]
        lname = request.form["pwd"]
        uname = fname+" "+lname 
        resp = make_response(render_template("cookie.html"))
        resp.set_cookie("uname", uname,
                    expires=datetime.datetime.now() + datetime.timedelta(days=30))
        return resp


@app.route("/ShowCookie")
def displayCookie():
    uname = request.cookies["uname"]
    return "Hello "+uname

#login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login/login.html")
    else:
        email = request.form["email"]  # Changed from username to email
        password = request.form["password"]
        
        con = mysql.connector.connect(host="localhost", user="root", passwd="Shradha720@", database="deepak")
        try:
            mycursor = con.cursor()
            mycursor.execute("SELECT password, username FROM account WHERE email = %s", (email,))
            myresult = mycursor.fetchone()
            
            if myresult and myresult[0] == password:
                session["login"] = True
                session["username"] = myresult[1]
                flash("Logged in successfully!", "success")
                return redirect(url_for('home'))
            else:
                session["login"] = False
                session["username"] = ''
                flash("Invalid email or password!", "danger")
                return redirect(url_for('login'))
        
        finally:
            con.close()




@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("/login/register.html")
    else:
        username = request.form["username"]
        email = request.form["email"]
        MobileNumber = request.form["MobileNumber"]
        Sex = request.form["sex"]
        password = request.form["password"]  # Hashing password
        con = mysql.connector.connect(host="localhost", user="root", passwd="Shradha720@", database="deepak")
        try:
            mycursor = con.cursor()
            sql = "INSERT INTO account (username, email, MobileNumber, sex, password) VALUES (%s, %s, %s, %s, %s)"
            val = (username, email, MobileNumber, Sex, password)
            mycursor.execute(sql, val)
            con.commit()
            flash("Registered Successfully", "success")
            return redirect(url_for("login"))
        finally:
            con.close()


@app.route("/adregister", methods=["GET", "POST"])
def adregister():
    if request.method == "GET":
        return render_template("/admin/adregister.html")
    else:
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]  # Optionally hash the password for security

        # Connect to the database and add the new admin
        con = mysql.connector.connect(host="localhost", user="root", passwd="Shradha720@", database="deepak")
        try:
            mycursor = con.cursor()
            sql = "INSERT INTO admin_account (username, email, password) VALUES (%s, %s, %s)"
            val = (username, email, password)
            mycursor.execute(sql, val)
            con.commit()
            flash("Admin Registered Successfully", "success")
            return redirect(url_for("adlogin"))
        finally:
            con.close()
            
# from werkzeug.security import check_password_hash

@app.route("/adlogin", methods=["GET", "POST"])
def adlogin():
    if request.method == "GET":
        return render_template("/admin/adlogin.html")
    else:
        email = request.form["email"]  # Use email for login
        password = request.form["password"]
        
        con = mysql.connector.connect(host="localhost", user="root", passwd="Shradha720@", database="deepak")
        try:
            mycursor = con.cursor()
            sql = "SELECT password FROM admin_account WHERE email = %s" # Check against email
            val = (email,)  # Use the email value for query
            mycursor.execute(sql, val)
            myresult = mycursor.fetchone()
            
            if myresult and myresult[0] == password:
                # Verify the hashed password
                session["adlogin"] = True
                session["email"] = email  # Store email instead of username
                flash("Admin logged in Successfully", "success")
                return redirect(url_for('home'))
            else:
                flash("Invalid Admin email or password!", "danger")
                return redirect(url_for('adlogin'))
        finally:
            con.close()


@app.route("/Users")
def Users():
    con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
    try: 
        mycursor = con.cursor()
        mycursor.execute("SELECT * FROM account")
        myresult = mycursor.fetchall()
        return render_template("/admin/Users.html",users = myresult)
    finally:
        con.close()

# @app.route("/RemoveUser/<Email>",methods=["GET","POST"])
# def RemoveUser(Email):
#     if(request.method=="GET"):
#         return render_template("/admin/RemoveUser.html")
#     else:
#         action = request.form["action"]
#         if(action == "Yes"):
#             con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
#             try: 
#                 flash("User Deleted Successfully",'success')
#                 mycursor = con.cursor()
#                 sql = "delete from account where email=%s"
#                 val = (Email,)
#                 mycursor.execute(sql,val)
#             finally:
#                 con.close()
#         return redirect(url_for("Users"))



@app.route("/RemoveUser/<Email>", methods=["GET", "POST"])
def RemoveUser(Email):
    if request.method == "GET":
        return render_template("/admin/RemoveUser.html")
    else:
        action = request.form["action"]
        if action == "Yes":
            con = mysql.connector.connect(host="localhost", user="root", passwd="Shradha720@", database="deepak")
            try:
                mycursor = con.cursor()
                sql = "DELETE FROM account WHERE email = %s"
                val = (Email,)
                mycursor.execute(sql, val)
                con.commit()  # Ensure changes are committed to the database
                flash("User Deleted Successfully", 'success')
            except mysql.connector.Error as err:
                flash(f"Error: {err}", 'danger')  # Flash an error if something goes wrong
            finally:
                con.close()
        return redirect(url_for("Users"))


@app.route("/adlogout")
def adlogout():
    session["adlogin"] = False
    flash(" Admin Logged out Successfully!!","success")
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session["login"] = False
    session['Bookings'] = {}
    session.clear()
    flash("User Logged out Successfully!!","success")
    return redirect(url_for("home"))


@app.route("/")
def main(): 
    con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
    try: 
        mycursor = con.cursor()
        mycursor.execute("SELECT * FROM category")
        myresult = mycursor.fetchall()
        session["cats"] = myresult       
    finally:
        con.close()
        return render_template("index.html")



@app.route("/Categories")
def showAllCategories():
    con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
    try: 
        mycursor = con.cursor()
        mycursor.execute("SELECT * FROM category")
        myresult = mycursor.fetchall()
        return render_template("/admin/category.html",cats = myresult)
    finally:
        con.close()


@app.route("/AddNewCategory",methods=["GET","POST"])
def AddNewDept():
    if(request.method=="GET"):
        return render_template("/admin/AddCategory.html")
    else:
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
        try: 
            flash("New Category Inserted Successfully",'success')
            mycursor = con.cursor()            
            cname = request.form["cname"]            
            sql = "insert into category (cname) values(%s)"
            val = (cname,)
            mycursor.execute(sql,val)            
            return redirect(url_for("showAllCategories"))
        finally:
            con.close()


# @app.route("/AddCategory",methods=["GET","POST"])
# def AddCategory():
#     if(request.method=="GET"):
#         return render_template("/admin/AddCategory.html")
#     else:
#         con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
#         try: 
#             flash("New Category Inserted Successfully",'success')
#             mycursor = con.cursor()
#             sql = "insert into category (cid,cname) values (%s)"
#             val = (request.form["cid"],["cname"],)
#             mycursor.execute(sql,val)            
#             return redirect(url_for("Category"))
#         finally:
#             con.close()

@app.route("/AddCategory", methods=["GET", "POST"])
def AddCategory():
    if request.method == "GET":
        return render_template("/admin/AddCategory.html")
    else:
        con = mysql.connector.connect(host="localhost", user="root", passwd="Shradha720@", database="deepak")    
        try:
            mycursor = con.cursor()
            sql = "INSERT INTO category (cid, cname) VALUES (%s, %s)"
            val = (request.form["cid"], request.form["cname"])
            mycursor.execute(sql, val)
            con.commit()  # Commit the transaction to save changes
            flash("New Category Inserted Successfully", 'success')
            return redirect(url_for("Category"))
        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
        finally:
            con.close()



# @app.route("/EditCategory/<id>",methods=["GET","POST"])
# def EditCategory(id):
#     if(request.method=="GET"):
#         flash("Category Updated Successfully")
#         con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
#         try: 
#             mycursor = con.cursor()
#             sql = "select * from category where cid=%s"
#             val = (id,)
#             mycursor.execute(sql,val)
#             result = myresult = mycursor.fetchone()
#             return render_template("/admin/EditCategory.html",cat=result)
#         finally:
#             con.close()
    
#     else:
#         con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
#         try: 
#             mycursor = con.cursor()
#             sql = "update category set cname = %s where cid=%s"
#             val = (request.form["cname"],id,)
#             mycursor.execute(sql,val)
#         finally:
#             con.close()
#         return redirect(url_for("Category"))


@app.route("/EditCategory/<id>", methods=["GET", "POST"])
def EditCategory(id):
    con = mysql.connector.connect(host="localhost", user="root", passwd="Shradha720@", database="deepak")    
    try:
        mycursor = con.cursor()
        if request.method == "GET":
            sql = "SELECT * FROM category WHERE cid = %s"
            val = (id,)
            mycursor.execute(sql, val)
            result = mycursor.fetchone()
            return render_template("/admin/EditCategory.html", cat=result)
        
        elif request.method == "POST":
            sql = "UPDATE category SET cname = %s WHERE cid = %s"
            val = (request.form["cname"], id)
            mycursor.execute(sql, val)
            con.commit()  # Commit the transaction to save changes
            flash("Category Updated Successfully", 'success')
            return redirect(url_for("Category"))
    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')
    finally:
        con.close()


# @app.route("/DeleteCategory/<id>",methods=["GET","POST"])
# def DeleteCategory(id):
#     if(request.method=="GET"):
#         return render_template("/admin/DeleteCategory.html")
#     else:
#         action = request.form["action"]
#         if(action == "Yes"):
#             con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
#             try: 
#                 flash("Category Deleted Successfully",'success')
#                 mycursor = con.cursor()
#                 sql = "delete from category where cid=%s"
#                 val = (id,)
#                 mycursor.execute(sql,val)
#             finally:
#                 con.close()
#         return redirect(url_for("Category"))


@app.route("/DeleteCategory/<id>", methods=["GET", "POST"])
def DeleteCategory(id):
    if request.method == "GET":
        return render_template("/admin/DeleteCategory.html")
    else:
        action = request.form["action"]
        if action == "Yes":
            con = mysql.connector.connect(host="localhost", user="root", passwd="Shradha720@", database="deepak")    
            try: 
                mycursor = con.cursor()
                sql = "DELETE FROM category WHERE cid = %s"
                val = (id,)
                mycursor.execute(sql, val)
                con.commit()  # Commit the transaction to save changes
                flash("Category Deleted Successfully", 'success')
            except mysql.connector.Error as err:
                flash(f"Error: {err}", 'danger')
            finally:
                con.close()
        return redirect(url_for("Category"))


@app.route("/Category")
def Category():
    con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
    try: 
        mycursor = con.cursor()
        mycursor.execute("SELECT * FROM category")
        myresult = mycursor.fetchall()
        return render_template("/admin/Categories.html",cats = myresult)
    finally:
        con.close()



@app.route("/Products")
def showAllProducts():
    con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
    try: 
        mycursor = con.cursor()
        mycursor.execute("select p.pid,p.pname,p.price,c.cname from product p inner join  category c on p.cid = c.cid;")
        myresult = mycursor.fetchall()
        return render_template("/admin/Products.html",prds = myresult)
    finally:
        con.close()

@app.route("/EditProduct/<id>",methods=["GET","POST"])
def EditProduct(id):
    if(request.method=="GET"):
        flash("Product Updated Successfully",'success')
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
        try: 
            mycursor = con.cursor()
            sql = "select * from product where pid=%s"
            val = (id,)
            mycursor.execute(sql,val)
            result = myresult = mycursor.fetchone()
            return render_template("/admin/EditProduct.html",prd =result)
        finally:
            con.close()
    
    else:
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
        try: 
            mycursor = con.cursor()
            sql = "update product set pname = %s where pid=%s"
            val = (request.form["pname"],id,)
            mycursor.execute(sql,val)
            con.commit()
        finally:
            con.close()
        return redirect(url_for("showAllProducts"))

@app.route("/DeleteProduct/<id>",methods=["GET","POST"])
def DeleteProduct(id):
    if(request.method=="GET"):
        return render_template("/admin/DeleteProduct.html")
    else:
        action = request.form["action"]
        if(action == "Yes"):
            con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
            try: 
                flash("Product Deleted Successfully",'success')
                mycursor = con.cursor()
                sql = "delete from product where pid=%s"
                val = (id,)
                mycursor.execute(sql,val)
                con.commit()
            finally:
                con.close()
        return redirect(url_for("showAllProducts"))

@app.route("/AddProduct",methods=["GET","POST"])
def AddProduct():
    if(request.method=="GET"):
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
        try: 
            mycursor = con.cursor()
            mycursor.execute("SELECT * FROM category")
            myresult = mycursor.fetchall()
            return render_template("/admin/AddNewProduct.html",cats = myresult)
        finally:
            con.close()
    else:
        pid = request.form["pid"]        
        pname = request.form["pname"]
        price = request.form["price"]
        catid = request.form["catid"]
       
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
        try: 
            flash("New Product Inserted Successfully",'success')
            mycursor = con.cursor()
            sql = "insert into product (pid,pname,price,cid) values(%s,%s,%s,%s)"
            val = (pid,pname,price,catid,)
            mycursor.execute(sql,val)  
            con.commit()          
            return redirect(url_for("showAllProducts"))
        finally:
            con.close()


@app.route("/ViewDetails/<id>")
def ViewDetails(id): 
    con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
    try: 
        mycursor = con.cursor()
        sql = "SELECT * FROM product where pid=%s";
        val = (id,)
        mycursor.execute(sql,val)
        myresult = mycursor.fetchone()
        return render_template("/user/ViewDetails.html",prd = myresult)
    finally:
        con.close()



@app.route("/ShowProducts/<id>")
def ShowProducts(id):
    con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
    try: 
        mycursor = con.cursor()
        sql = "SELECT pid,pname,price FROM product where cid=%s";
        val = (id,)
        mycursor.execute(sql,val)
        myresult = mycursor.fetchall()
        return render_template("/user/ShowProducts.html",prds = myresult)
    finally:
        con.close()


@app.route("/AddToCart",methods=["GET","POST"])
def AddToCart():
    
    # login check
    if not session.get("login"):
        flash("You need to log in to add items to your cart.", "danger")
        return redirect(url_for('login'))
    
    if(request.method=="POST"):
        pid=request.form["pid"]
        pname=request.form["pname"]
        price=request.form["price"]
        qty=request.form["qty"]
        item=[pid,pname,price,qty]
        #If Session is not created
        if("MyBooking" not in session):
            Bookings={}
        else:
            Bookings=session["MyBooking"]
        Bookings[pid]=item
        #for updating the session
        session["MyBooking"]=Bookings
        return redirect("bookings")

@app.route("/bookings")
def bookings():
    
    # Check if the user is logged in
    if not session.get("login"):
        flash("You need to log in to view your cart.", "danger")
        return redirect(url_for('login'))
    
    if("MyBooking" not in session):
        return "No items in MyBooking"
    else:
        total = 0
        for prd in session["MyBooking"].values():
            total  =  total + float(prd[2])*float(prd[3])
        session["total"] = total
       
        return render_template("/user/bookings.html", total=total, bookings=session["MyBooking"])


@app.route("/RemoveFromCart",methods=["GET","POST"])
def RemoveFromCart():
    # Check if the user is logged in
    if not session.get("login"):
        flash("You need to log in to modify your cart.", "danger")
        return redirect(url_for('login'))
    
    # if(request.method=="POST"):
    #     pid = str(request.form["pid"])
    #     Bookings = session["MyBooking"]
    #     del Bookings[pid]
    #     session["MyBooking"] = Bookings
    #     return redirect("bookings")
    
    if request.method == "POST":
        pid = str(request.form["pid"])
        if "MyBooking" in session:
            Bookings = session["MyBooking"]
            if pid in Bookings:
                del Bookings[pid]
                session["MyBooking"] = Bookings
                flash("Item removed from cart successfully!", "success")
            else:
                flash("Item not found in cart.", "warning")
        else:
            flash("Your cart is empty.", "warning")
        return redirect(url_for("bookings"))
            
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/chat", methods=["GET"])
def ChatWithLLM():
    return render_template('chat.html')
        
@app.route("/chat/query", methods=["POST"])
def Chatwithllmnow():
    data = request.json["ques"]
    ans = chat_bot.ChatWIthLLM(data)
    return jsonify({"answer": ans})

# bus details  
@app.route("/ShowProducts/1", methods=["POST"])
def show_products_bus():
    # Sample product data
    products = [
        (1, 'HSR-BNW', 100),
        (2, 'BNW-KKR', 200),
        (3, 'KARNAL-PANIPAT', 300),
        (4, 'PANIPAT-SONIPAT ', 300),
        (5, 'SONIPAT-BNW', 300),
        (6, 'ROK-BNW', 300),
        (7, 'CDG-BNW', 300),
        (8, 'SSR-BNW', 300),
        (9, 'KKR-SSR', 300),
        (10, 'KRK-SRK', 300),
        # Add more products as needed
    ]
    return render_template('/user/ShowProducts.html', prds=products)


# train details
@app.route("/ShowProducts/2", methods=["POST"])
def show_products_train():
    # Sample product data
    products = [
        (121, 'Kisan Express', 200),
        (122, 'Gorakhdham Express', 200),
        (123, 'Kalindi Express', 300),
        (124, 'Sirsa Express', 300),
        (125, 'Garibrath Express', 900),
        (126, 'Ekta Express', 150),
        (127, 'Rajdhani Express', 4000),
        (128, 'Vande Bharat', 1100),
        (129, 'Abdullah Express', 2500),
        (130, 'Rehman Express', 100),
        (131, 'Maharaja Express', 30000),
        # Add more products as needed
    ]
    return render_template('/user/ShowProducts.html', prds=products)


# Flights details
@app.route("/ShowProducts/3", methods=["POST"])
def show_products_flight():
    # Sample product data
    products = [
        (221, 'Indigo', 2000),
        (222, 'Spice jet', 4000),
        (223, 'Air India', 10000),
        (224, 'British Airways', 3999),
        (225, 'Emirates', 5990),
        (226, 'American Express', 1000),
        (227, 'Jet Airways', 21000),
        (228, 'Airways', 10000),
        (229, 'Flights', 20000),
        # Add more products as needed
    ]
    return render_template('/user/ShowProducts.html', prds=products)


# Hotels
@app.route("/ShowProducts/4", methods=["POST"])
def show_products_hotels():
    # Sample product data
    products = [
        (331, 'Noor Mahal, Karnal', 4000),
        (332, 'HSB Grand, Bhiwani', 5500),
        (333, 'Baya Guest house, Bhiwani', 10499),
        (334, 'HSB Grand, Bhiwani', 10499),
        (335, 'Taj, Chandigarh', 10499),
        (336, 'Oyo , Kurukshetra', 10499),
        (337, 'Oberoi, Chandigarh', 10499),
        (338, 'Black Lotus, Chandigarh', 10499),
        # Add more products as needed
    ]
    return render_template('/user/ShowProducts.html', prds=products)



# product_data = {
#     1: {'pid': 1, 'pname': 'Sample Product', 'price': 100, 'details': 'This is a sample product description.', 'seats': 'Aisle 3, Row 5'},
#     2: {'pid': 2, 'pname': 'Another Product', 'price': 150, 'details': 'Another product description.', 'seats': 'Aisle 4, Row 6'}
# }
product_data = {
    # Bus routes
    1: {'pid': 1, 'pname': 'HSR-BNW', 'price': 100, 'details': 'Bus route from HSR to BNW', 'seats': 'Aisle 1, Row 3'},
    2: {'pid': 2, 'pname': 'BNW-KKR', 'price': 200, 'details': 'Bus route from BNW to KKR', 'seats': 'Aisle 1, Row 4'},
    3: {'pid': 3, 'pname': 'KARNAL-PANIPAT', 'price': 300, 'details': 'Bus route from Karnal to Panipat', 'seats': 'Aisle 2, Row 5'},
    4: {'pid': 4, 'pname': 'PANIPAT-SONIPAT', 'price': 300, 'details': 'Bus route from Panipat to Sonipat', 'seats': 'Aisle 2, Row 6'},
    5: {'pid': 5, 'pname': 'SONIPAT-BNW', 'price': 300, 'details': 'Bus route from Sonipat to BNW', 'seats': 'Aisle 3, Row 7'},
    6: {'pid': 6, 'pname': 'ROK-BNW', 'price': 300, 'details': 'Bus route from ROK to BNW', 'seats': 'Aisle 4, Row 8'},
    7: {'pid': 7, 'pname': 'CDG-BNW', 'price': 300, 'details': 'Bus route from CDG to BNW', 'seats': 'Aisle 5, Row 9'},
    8: {'pid': 8, 'pname': 'SSR-BNW', 'price': 300, 'details': 'Bus route from SSR to BNW', 'seats': 'Aisle 5, Row 10'},
    9: {'pid': 9, 'pname': 'KKR-SSR', 'price': 300, 'details': 'Bus route from KKR to SSR', 'seats': 'Aisle 6, Row 11'},
    10: {'pid': 10, 'pname': 'KRK-SRK', 'price': 300, 'details': 'Bus route from KRK to SRK', 'seats': 'Aisle 7, Row 12'},

    # Train routes
    121: {'pid': 121, 'pname': 'Kisan Express', 'price': 200, 'details': 'Train route from XYZ to ABC', 'seats': 'Compartment A, Seat 3'},
    122: {'pid': 122, 'pname': 'Gorakhdham Express', 'price': 200, 'details': 'Train route from DEF to GHI', 'seats': 'Compartment A, Seat 4'},
    123: {'pid': 123, 'pname': 'Kalindi Express', 'price': 300, 'details': 'Train route from JKL to MNO', 'seats': 'Compartment B, Seat 5'},
    124: {'pid': 124, 'pname': 'Sirsa Express', 'price': 300, 'details': 'Train route from PQR to STU', 'seats': 'Compartment B, Seat 6'},
    125: {'pid': 125, 'pname': 'Garibrath Express', 'price': 900, 'details': 'Train route from VWX to YZA', 'seats': 'Compartment C, Seat 7'},
    126: {'pid': 126, 'pname': 'Ekta Express', 'price': 150, 'details': 'Train route from BCD to EFG', 'seats': 'Compartment C, Seat 8'},
    127: {'pid': 127, 'pname': 'Rajdhani Express', 'price': 4000, 'details': 'Premium train route from HJK to LMN', 'seats': 'Compartment D, Seat 9'},
    128: {'pid': 128, 'pname': 'Vande Bharat', 'price': 1100, 'details': 'Premium train route from OPQ to RST', 'seats': 'Compartment E, Seat 10'},
    129: {'pid': 129, 'pname': 'Abdullah Express', 'price': 2500, 'details': 'Train route from UVW to XYZ', 'seats': 'Compartment F, Seat 11'},
    130: {'pid': 130, 'pname': 'Rehman Express', 'price': 100, 'details': 'Train route from ABC to DEF', 'seats': 'Compartment G, Seat 12'},
    131: {'pid': 131, 'pname': 'Maharaja Express', 'price': 30000, 'details': 'Luxury train route from GHI to JKL', 'seats': 'Compartment H, Suite'},

    # Flights
    221: {'pid': 221, 'pname': 'Indigo', 'price': 2000, 'details': 'Flight from City A to City B', 'seats': 'Window, Row 1'},
    222: {'pid': 222, 'pname': 'Spice Jet', 'price': 4000, 'details': 'Flight from City C to City D', 'seats': 'Aisle, Row 2'},
    223: {'pid': 223, 'pname': 'Air India', 'price': 10000, 'details': 'Flight from City E to City F', 'seats': 'Window, Row 3'},
    224: {'pid': 224, 'pname': 'British Airways', 'price': 3999, 'details': 'Flight from City G to City H', 'seats': 'Aisle, Row 4'},
    225: {'pid': 225, 'pname': 'Emirates', 'price': 5990, 'details': 'Flight from City I to City J', 'seats': 'Window, Row 5'},
    226: {'pid': 226, 'pname': 'American Express', 'price': 1000, 'details': 'Flight from City K to City L', 'seats': 'Middle, Row 6'},
    227: {'pid': 227, 'pname': 'Jet Airways', 'price': 21000, 'details': 'Flight from City M to City N', 'seats': 'Window, Row 7'},
    228: {'pid': 228, 'pname': 'Airways', 'price': 10000, 'details': 'Flight from City O to City P', 'seats': 'Aisle, Row 8'},
    229: {'pid': 229, 'pname': 'Flights', 'price': 20000, 'details': 'Flight from City Q to City R', 'seats': 'Middle, Row 9'},

    # Hotels
    331: {'pid': 331, 'pname': 'Noor Mahal, Karnal', 'price': 4000, 'details': 'Luxury hotel in Karnal', 'seats': 'Suite'},
    332: {'pid': 332, 'pname': 'HSB Grand, Bhiwani', 'price': 5500, 'details': 'Grand hotel in Bhiwani', 'seats': 'Deluxe'},
    333: {'pid': 333, 'pname': 'Baya Guest House, Bhiwani', 'price': 10499, 'details': 'Guest house in Bhiwani', 'seats': 'Private Room'},
    334: {'pid': 334, 'pname': 'HSB Grand, Bhiwani', 'price': 10499, 'details': 'Luxury hotel in Bhiwani', 'seats': 'Private Room'},
    335: {'pid': 335, 'pname': 'Taj, Chandigarh', 'price': 10499, 'details': 'Luxury hotel in Chandigarh', 'seats': 'Executive Suite'},
    336: {'pid': 336, 'pname': 'Oyo, Kurukshetra', 'price': 10499, 'details': 'Budget hotel in Kurukshetra', 'seats': 'Standard Room'},
    337: {'pid': 337, 'pname': 'Oberoi, Chandigarh', 'price': 10499, 'details': 'Luxury hotel in Chandigarh', 'seats': 'Deluxe Room'},
    338: {'pid': 338, 'pname': 'Black Lotus, Chandigarh', 'price': 10499, 'details': 'Premium hotel in Chandigarh', 'seats': 'King Suite'},
}

@app.route('/ViewDetails')
def product():
    return render_template('/user/ViewDetails.html', prd=product_data[1])


@app.route('/ViewDetails/<int:pid>')
def view_details(pid):
    # Retrieve product information based on pid
    product = product_data.get(pid)
    if product:
        return render_template('/user/ViewDetails.html', prd=product)
    else:
        return "Product not found", 404


@app.route('/MakePayment')
def make_payment():
    if session.get('total', 0) > 0:
        # Render a page to show the "Proceeding to Payment" message
        return render_template("/user/ProceedingToPayment.html")
    else:
        return "No items in your booking."

# Example route for showing the booking details
@app.route('/')
def add_booking():
    # Sample function for adding bookings; implement your own logic here
    return redirect(url_for('show_bookings'))


stripe.api_key = "sk_test_51QJXNNKlP5tBMAytvdmPzbGyZZJxAykU2aUnqGh0RtQXelrA4zrrUasTyhdEBbM2CZNc9XLHyMrhd5MPsPyFn13900KiAgTz7g"

# Route for MakePayment2
@app.route("/MakePayment2", methods=["POST", "GET"])
def make_payment2():
    if request.method == "POST":
        # Extract form data (e.g., amount)
        amount = int(session.get("total", 100))  # Replace with actual amount
        
        # Create a Stripe PaymentIntent for the payment
        intent = stripe.PaymentIntent.create(
            amount=amount * 100,  # Stripe requires amounts in cents
            currency="usd",  # Adjust currency as needed
            payment_method_types=["card"]
        )

        # Return client secret to use in frontend JavaScript for secure payment
        return render_template("/user/MakePayment.html", client_secret=intent.client_secret)

    # Render the payment form for GET request
    return render_template("/user/MakePayment.html")




if(__name__ == "__main__"):
    app.run(debug=True)