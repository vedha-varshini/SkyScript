# api/app.py
import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder='../templates')  # Adjust template path

# API configuration
API_KEY = os.getenv("API_KEY", "207847adb8msh94744171f8832d6p1cba76jsn720da22eb090")  # Fallback for local testing
BASE_URL = "https://open-weather13.p.rapidapi.com/city/"
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "open-weather13.p.rapidapi.com"
}

def get_weather(city):
    url = f"{BASE_URL}{city}/EN"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'main' not in data:
            return {"error": "Invalid response format from API"}
        return data
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP Error {e.response.status_code}: {e.response.reason}"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather_data = get_weather(city)
            if "error" in weather_data:
                error = weather_data["error"]
        else:
            error = "Please enter a city name"
    
    return render_template('index.html', 
                         weather_data=weather_data, 
                         error=error)

# Vercel serverless entry point
def handler(event, context):
    from wsgi import wsgi_handler
    return wsgi_handler(app, event, context)

if __name__ == '__main__':
    app.run(debug=True)  # For local testing
