from flask import Flask, render_template, request
import sqlite3
import requests
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("setup-page.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/setup")
def setup():
    return render_template("setup-page.html")


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
    ### clear the db every time in order to provide most accurate, up-to-date webmentions. 
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


@app.route("/search")
def search():
    if (checkAccount()) == {}:
        return -1
    else:
        accountData = checkAccount()
        firstName = accountData["firstname"]
        lastName = accountData["lastname"]
        city = accountData["city"]
        school = accountData["school"]
        occupation = accountData["occupation"]
        age = accountData["age"]
        url = "https://api.search.brave.com/res/v1/web/search"

        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": "BSAONIqZTGvi7cF_pOC07tbUiSsygY4" ## api key
        }

        ## dict to hold all the result countsand highlight titles
        resultCounts = {"basicYear": {"count": 0, "title": "None"}, "basicMonth": {"count": 0, "title": "None"}, "basicWeek": {"count": 0, "title": "None"}, "basicDay": {"count": 0, "title": "None"}, "explicit": False} 

        ## PARAMETERS TO CUSTOMIZE DIFF. SEARCHES 

        ## basic search of simply the first and last name and city
        ## last 365 days or less
        paramsBasicYear = {
            "q": f'{firstName} {lastName} {city} {school} {occupation}',
            "freshness": "py",
            "safesearch": "off"
            ## pd == 24 hours or less, pw == 7 days or less, pm == 31 days or less, py 365 days or less
        }
        responseBasicYear = requests.get(url, headers=headers, params=paramsBasicYear)
        resultsBasicYear = responseBasicYear.json()
        resultCounts["basicYear"]["count"] = len(resultsBasicYear.get("web", {}).get("results", []))
        if (resultsBasicYear.get("web", {}).get("results", [])):
            resultCounts["basicYear"]["title"] = resultsBasicYear.get("web", {}).get("results", [])[0]["title"]
            if (resultsBasicYear.get("web", {}).get("family_friendly") == False):
                resultCounts["explicit"] = True
        else:
            resultCounts["basicYear"]["title"] = "None found."
        

        ## basic search of simply the first and last name and city
        ## last 31 days or less
        paramsBasicMonth = {
            "q": f'"{firstName} {lastName}" {city} {school} {occupation}',
            "freshness": "pm",
            "safesearch": "off"
            ## pd == 24 hours or less, pw == 7 days or less, pm == 31 days or less, py 365 days or less
        }
        responseBasicMonth = requests.get(url, headers=headers, params=paramsBasicMonth)
        resultsBasicMonth = responseBasicMonth.json()
        resultCounts["basicMonth"]["count"] = len(resultsBasicMonth.get("web", {}).get("results", []))
        if (resultsBasicMonth.get("web", {}).get("results", [])):
            resultCounts["basicMonth"]["title"] = resultsBasicMonth.get("web", {}).get("results", [])[0]["title"]
            if (resultsBasicMonth.get("web", {}).get("family_friendly") == False):
                resultCounts["explicit"] = True
        else:
            resultCounts["basicMonth"]["title"] = "None found."

        ## basic search of simply the first and last name and city
        ## last 7 days or less
        paramsBasicWeek = {
            "q": f'"{firstName} {lastName}" {city} {school} {occupation}',
            "freshness": "pw",
            "safesearch": "off"
            ## pd == 24 hours or less, pw == 7 days or less, pm == 31 days or less, py 365 days or less
        }
        responseBasicWeek = requests.get(url, headers=headers, params=paramsBasicWeek)
        resultsBasicWeek = responseBasicWeek.json()
        resultCounts["basicWeek"]["count"] = len(resultsBasicWeek.get("web", {}).get("results", []))
        if (resultsBasicWeek.get("web", {}).get("results", [])):
            resultCounts["basicWeek"]["title"] = resultsBasicWeek.get("web", {}).get("results", [])[0]["title"]
            if (resultsBasicWeek.get("web", {}).get("family_friendly") == False):
                resultCounts["explicit"] = True
        else:
            resultCounts["basicWeek"]["title"] = "None found."

        ## basic search of simply the first and last name and city
        ## last 24 hours or less
        print(f"{firstName} {lastName} {city}")
        paramsBasicDay = {
            "q": f'"{firstName} {lastName}" {city} {school} {occupation}',
            "freshness": "pd",
            "safesearch": "off"
            ## pd == 24 hours or less, pw == 7 days or less, pm == 31 days or less, py 365 days or less
        }
        responseBasicDay = requests.get(url, headers=headers, params=paramsBasicDay)
        resultsBasicDay = responseBasicDay.json()
        resultCounts["basicDay"]["count"] = len(resultsBasicDay.get("web", {}).get("results", []))
        if (resultsBasicDay.get("web", {}).get("results", [])):
            resultCounts["basicDay"]["title"] = resultsBasicDay.get("web", {}).get("results", [])[0]["title"]
            if (resultsBasicDay.get("web", {}).get("family_friendly") == False):
                resultCounts["explicit"] = True
        else:
            resultCounts["basicDay"]["title"] = "None found."

        
        ## return one of the actual results
        ## print(responseBasicYear.json()["web"]["results"][0]["description"])
        return resultCounts


if __name__ == "__main__":
    app.run(debug=True)