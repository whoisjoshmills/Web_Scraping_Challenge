# Dependencies
from flask import Flask, render_template, redirect, Markup
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

# create route that rendrs index.html template
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    #news_p = mongo.db.s
    
    # Scrape mars data and store dictionary in variable
    mars_html =  scrape_mars.mars_html()

    # Scrape mars data and store dictionary in variable
    hemispheres =  scrape_mars.hemispheres()

    return render_template("index.html", mars=mars, mars_html=mars_html, hemispheres=hemispheres)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Delete old mars collection
    mongo.db.mars.drop()

   # Define mars collection
    mars = mongo.db.mars

    # Scrape mars data and store dictionary in variable
    mars_data =  scrape_mars.scrape_mars()

    # Insert dictionary into mars collection
    mars.insert_one(mars_data)
    
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)