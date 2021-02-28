from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/nasa_app")


@app.route('/')
def index():
    mars = mongo.db.nasa_app.find_one()
    return render_template('index.html', mars=mars)


@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    data = scrape_mars.scrape()

return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
