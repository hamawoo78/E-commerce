# from flask import Flask, render_template, request, redirect, url_for, session
# import sqlite3
# sqlite3 Shopping.db

import tkinter.messagebox as messagebox

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import login_required

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///Shopping.db")

Types = ["Home", "Kitchen", "Hobby", "Office", "Others"]

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Show all items"""
    items_db = db.execute("SELECT * FROM items")
    itemTypeName = db.execute("SELECT * FROM itemTypes")
    return render_template("index.html", allItems=items_db, itemTypeName=itemTypeName)

@app.route("/ForSeller")
@login_required
def allItems_seller():
    """Show Users items"""
    items_db_seller = db.execute("SELECT * FROM items WHERE userId = ?", session["user_id"])
    show_confirmation=False
    return render_template("index_for_seller.html", allItems=items_db_seller, itemType=Types, show_confirmation=show_confirmation)

# Route for the item detail page
@app.route('/detail/<int:id>')
def item_detail(id):
    item = db.execute("SELECT * FROM items WHERE id = ?", id)
    print(item[0]['itemTypeKey'])
    Type_id = db.execute("SELECT * FROM itemTypes WHERE id = ?", item[0]['itemTypeKey'])
    Type = Type_id[0]["itemTypeName"]

    if item:
        return render_template('detail.html', item=item, Type=Type)
    else:
        return 'Item not found'

# Route to handle the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""

    messages = ""

    # Forget any user_id
    session.clear()

    if request.method == 'POST':
        # Query database for username
        username = request.form.get('username')
        rows = db.execute("SELECT * FROM users WHERE username = ?",username )

        if len(rows) == 0:
            messages = "invalid username"
            return render_template('login.html', messages=messages)
        else:
            # Ensure username exists and password is correct
            user_password = rows[0]['hash']
            password = request.form.get('password')

            if not check_password_hash(user_password,password):
                messages = "invalid password"
                return render_template('login.html', messages=messages)
            else:
                # Remember which user has logged in
                flash('Successfully Logged In ', 'alert')
                session["user_id"] = rows[0]["id"]
                return redirect('/ForSeller')

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')

# Route to handle the logout
@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    # Redirect user to login form
    flash('Successfully Logged Out', 'alert')
    print("log out")
    return redirect("/login")

# Route to handle the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get("confirmation")

        if password != confirmation:
            flash('Password is not much', 'alert')

        if username == db.execute("SELECT username FROM users WHERE username = ?", username):
            flash('This username is already taken', 'alert')

        password = generate_password_hash(password, method='scrypt')

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password)
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]

        return redirect('/ForSeller')
    else:
        return render_template('register.html')

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        picture = request.form.get('picture')
        type = request.form.get('type')
        cost = request.form.get('cost')
        description = request.form.get('description')
        URL = request.form.get('URL')
        id = session["user_id"]

        # print(type)

        type_row = db.execute("SELECT * FROM itemTypes WHERE itemTypeName = ?", type)
        typeId = type_row[0]["id"]
        # print(typeId)

        db.execute("INSERT INTO items (itemname, itemPictureURL,itemTypeKey,itemCost,itemDescription,itemURL,userId) VALUES(?,?,?,?,?,?,?)", title, picture, typeId,cost, description,URL,id)
        return redirect('/ForSeller')
    return render_template('add.html', itemType=Types)


@app.route('/delete',methods=['POST'])
@login_required
def delete():
    item_to_delete = request.form.get("id")
    print(item_to_delete)
    if item_to_delete:
        confirmation = request.form.get("confirmation")

    if confirmation == "yes":
        db.execute("DELETE FROM items WHERE id = ?", item_to_delete)
        flash('Item deleted!', 'alert')

    return redirect('/ForSeller')


# Route to handle the edit
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    item = db.execute("SELECT * FROM items WHERE id = ?", id)
    # print("Before if")
    # print(item)
    if request.method == 'POST':
        title = request.form.get('title')
        picture = request.form.get('picture')
        type = request.form.get('type')
        cost = request.form.get('cost')
        description = request.form.get('description')
        URL = request.form.get('URL')
        user_id = session["user_id"]
        # print("Inside if")
        # print(title)


        type_row = db.execute("SELECT * FROM itemTypes WHERE itemTypeName = ?", type)
        typeId = type_row[0]['id']

        db.execute("UPDATE items SET itemname = ?, itemPictureURL = ? ,itemTypeKey = ? ,itemCost = ?,itemDescription = ?,itemURL = ?, userId = ? WHERE id = ? ",title, picture, typeId, cost, description,URL,user_id, id )
        return redirect('/ForSeller')
        # return redirect('/')

    else:
        return render_template('edit.html', item=item, itemType=Types)

@app.route('/sort/<string:name>', methods=['POST'])
def sort(name):
    if request.method == 'POST':
        if name == 'cost':
            items = db.execute("SELECT * FROM items ORDER BY itemCost")

        itemTypeName = db.execute("SELECT * FROM itemTypes")
        return render_template("index.html", allItems=items, itemTypeName=itemTypeName)