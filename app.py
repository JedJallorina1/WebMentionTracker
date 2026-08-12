from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("setup-page.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

connection1 = sqlite3.connect("database.db")
cursor1 = connection1.cursor()
cursor1.execute("""
CREATE TABLE IF NOT EXISTS userregistry(
id INTEGER PRIMARY KEY,
firstname TEXT,
lastname TEXT,
city TEXT,
school TEXT,
occupation TEXT,
age INTEGER
)""")

### CLEAR THE DB:
### cursor1.execute("DELETE FROM userregistry")
connection1.commit()
connection1.close()

@app.route("/createaccount", methods = ["POST"])
def createAccount():
    connection2 = sqlite3.connect("database.db")
    cursor2 = connection2.cursor()
    inputData = request.get_json()
    cursor2.execute("DELETE FROM userregistry")
    cursor2.execute("""
        INSERT INTO userregistry(firstname, lastname, city, school, occupation, age)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (inputData["firstname"], inputData["lastname"], inputData["city"], inputData["school"], inputData["occupation"], inputData["age"]))
    connection2.commit()
    connection2.close()
    return "Account created successfully!"

@app.route("/checkaccount")
def checkAccount():
    connection3 = sqlite3.connect("database.db")
    cursor3 = connection3.cursor()
    cursor3.execute("SELECT * FROM userregistry LIMIT 1")
    accountData = cursor3.fetchone()
    connection3.close()
    if accountData:
        return {
            "firstname": accountData[1],
            "lastname": accountData[2],
            "city": accountData[3],
            "school": accountData[4],
            "occupation": accountData[5],
            "age": accountData[6]
        }
    else:
        return {}

if __name__ == "__main__":
    app.run(debug=True)