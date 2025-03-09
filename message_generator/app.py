
from utils.tire_scraper import TireScraper
from utils.tire import Tire

from flask import Flask, request, render_template_string

app = Flask(__name__)

WIDTH_OPTIONS = ["11", "31", "33", "35", "175", "185", "195", "205", "215", "225", "235", "235", "245", "255", "265", "275", "285", "295"]
PROFILE_OPTIONS = ["12.5", "30", "35", "40", "50", "55", "60", "65", "70", "75", "80", "85"]
SIZE_OPTIONS = ["14", "15", "16", "17", "17.5", "18", "19", "19.5", "20", "21", "22", "22.5", "24.5"]

@app.route("/", methods=["GET", "POST"])
def home():
    stock_data = []
    
    if request.method == "POST":
        width = request.form.get("width")
        profile = request.form.get("profile")
        size = request.form.get("size")
        
        if width and profile and size:
            scraper = TireScraper(width, profile, size)
            stock_data = scraper.scrape_tire_stock()
    
    html_form = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tire Stock Checker</title>
    </head>
    <body>
        <h2>Select Your Tire Size</h2>
        <form method="POST">
            <label for="width">Width:</label>
            <select name="width" required>
                <option value="" selected disabled>-</option>
                {% for option in width_options %}
                    <option value="{{ option }}">{{ option }}</option>
                {% endfor %}
            </select>
            
            <label for="profile">Profile:</label>
            <select name="profile" required>
                <option value="" selected disabled>-</option>
                {% for option in profile_options %}
                    <option value="{{ option }}">{{ option }}</option>
                {% endfor %}
            </select>
            
            <label for="size">Size:</label>
            <select name="size" required>
                <option value="" selected disabled>-</option>
                {% for option in size_options %}
                    <option value="{{ option }}">{{ option }}</option>
                {% endfor %}
            </select>
            
            <button type="submit">Search</button>
            <button type="reset">Reset</button>
        </form>
        
        <br>
        
        <h3>Messsage:</h3>
        <p>Hi, thank you for reaching out. We currently the following tires available for this size</p>
        <ul>
            {% for tire in stock_data %}
                <li>{{ tire.name }} - {{ tire.price }} - {{ "(Low Stock - check with Zak)" if tire.low_stock}}</li>
            {% endfor %}
        </ul>
        
    
    </body>
    </html>
    '''
    return render_template_string(html_form, stock_data=stock_data, width_options=WIDTH_OPTIONS, profile_options=PROFILE_OPTIONS, size_options=SIZE_OPTIONS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
