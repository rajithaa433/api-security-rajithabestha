import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY not found. Please set it in your .env file.")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    # NOTE: Do NOT log user location data (city names).
    # Logging such data can violate privacy principles like GDPR's data minimization
    # and confidentiality requirements, as location can be considered sensitive data.

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)

        # Task 2 — Handle rate limiting and errors
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            print(f"Temperature: {temp}°C, Condition: {weather}")

        elif response.status_code == 429:
            print("Too many requests. Please wait a moment and try again.")

        elif response.status_code == 401:
            print("Invalid API key. Please check your configuration.")

        else:
            print(f"API error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")


if __name__ == "__main__":
    city = input("Enter city: ")
    get_weather(city)
