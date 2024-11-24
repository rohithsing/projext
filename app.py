from flask import Flask, render_template, request, redirect


import sqlite3



app = Flask(__name__)



# Create connection to SQLite database


def create_connection():


    conn = sqlite3.connect("users.db")
    return conn



# Create table to store users


def create_table():
    conn = create_connection()
    cur = conn.cursor()


    cur.execute('''


       CREATE TABLE IF NOT EXISTS users2 (


        id INTEGER PRIMARY KEY AUTOINCREMENT,


        first_name TEXT NOT NULL,


        last_name TEXT NOT NULL,


        email TEXT UNIQUE NOT NULL,


        phone_number TEXT NOT NULL,


        password TEXT NOT NULL
        )


    ''')
    conn.commit()
    conn.close()



# Home route


@app.route("/")


def home():

    return render_template("home.html")



@app.route("/thankyou")


def thankyou():


    return render_template("thankyou.html")




# Registration route


@app.route("/registration", methods=["GET", "POST"])


def registration():


    if request.method == "POST":


        first_name = request.form.get("firstN")


        last_name = request.form.get("lastN")


        email = request.form.get("email")


        phone = request.form.get("phone")


        password = request.form.get("password")


        confirm_password = request.form.get("confirmPassword")



        # Check if passwords match


        if password != confirm_password:


            return "Passwords do not match. Please <a href='/registration'>try again</a>."



        # Insert data into the database
        conn = create_connection()
        cur = conn.cursor()


        try:

            cur.execute("INSERT INTO users2 (first_name, last_name, email, phone_number, password) VALUES (?, ?, ?, ?, ?)",


                        (firstN,lastN, email, phone, password))
            conn.commit()
            conn.close()


            return redirect("/login")


        except sqlite3.IntegrityError:
            conn.close()


            return "Email already registered. Please <a href='/registration'>try again</a>."



    return render_template("registration.html")



# Login route


@app.route("/login", methods=["GET", "POST"])


def login():


    if request.method == "POST":


        email = request.form.get("emailOrPhone")


        password = request.form.get("password")



        # Check if the user exists
        conn = create_connection()
        cur = conn.cursor()


        cur.execute("SELECT * FROM users2 WHERE email = ? AND password = ?", (email, password))

        user = cur.fetchone()



        if user:


            return redirect("/thankyou")


        else:


            return "Invalid credentials! <a href='/login'>Try again</a>"



    return render_template("login.html")




if __name__ == "__main__":


    create_table()


    app.run(debug=True)


