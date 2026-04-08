from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

# 🔑 Put your OpenWeather API key here
API_KEY = "4fbc1b732bd0fdfc65baa0275f0e9ceb"


# 🌦️ Get weather data
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    return response.json()


# 👕 Outfit recommendation logic (UPDATED with mood)
def recommend_outfit(temp, weather, mood):
    weather = weather.lower()
    mood = mood.lower()

    # 🌧️ Rain priority
    if "rain" in weather:
        return "🌧️ Bring an umbrella, wear waterproof jacket"

    # 🧠 Combine weather + mood
    if temp < 5:
        if mood == "cozy":
            return "🧥 Warm coat + scarf + cozy sweater"
        elif mood == "chic":
            return "🧥 Stylish coat + boots"
        else:
            return "🧥 Heavy coat, gloves, scarf"

    elif temp < 15:
        if mood == "sporty":
            return "🏃 Hoodie + joggers + sneakers"
        elif mood == "cozy":
            return "🧥 Hoodie + comfy pants"
        else:
            return "🧥 Jacket or hoodie"

    elif temp < 25:
        if mood == "chic":
            return "👗 Light dress or stylish outfit"
        else:
            return "👕 T-shirt and jeans"

    else:
        if mood == "sporty":
            return "🏃 Tank top + shorts"
        else:
            return "🩳 Shorts, light clothes, stay cool"


# 🏠 Home page UI
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Outfit Recommender</title>
        </head>
        <body style="font-family: Arial; text-align:center; margin-top:50px;">
            <h1>👕 Outfit Recommender</h1>
            <form action="/recommend" method="post">
                
                <input type="text" name="city" placeholder="Enter city" required style="padding:10px;"/>
                <br><br>

                <select name="mood" style="padding:10px;">
                    <option value="cozy">Cozy / Lazy</option>
                    <option value="productive">Productive / Working</option>
                    <option value="sporty">Active / Sporty</option>
                    <option value="chic">Going Out / Chic</option>
                </select>

                <br><br>
                <button type="submit" style="padding:10px 20px;">Get Outfit</button>
            </form>
        </body>
    </html>
    """


# 📊 Result page
@app.post("/recommend", response_class=HTMLResponse)
def get_recommendation(city: str = Form(...), mood: str = Form(...)):
    data = get_weather(city)

    if not data:
        return f"""
        <h2>❌ City not found</h2>
        <a href="/">Go back</a>
        """

    temp = data["main"]["temp"]
    weather = data["weather"][0]["description"]

    outfit = recommend_outfit(temp, weather, mood)

    return f"""
    <html>
        <body style="font-family: Arial; text-align:center; margin-top:50px;">
            <h1>📍 {city.title()}</h1>
            <h2>🌡️ Temperature: {temp}°C</h2>
            <h3>🌤️ Weather: {weather}</h3>
            <h3>😊 Mood: {mood}</h3>

            <h2>👗 Recommended Outfit:</h2>
            <p style="font-size:20px;">{outfit}</p>

            <br><br>
            <a href="/">🔙 Try another city</a>
        </body>
    </html>
    """