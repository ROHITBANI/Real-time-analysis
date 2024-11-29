import requests
import streamlit as st

# Function to fetch current weather data
def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
    else:
        return {"error": f"Unable to fetch weather data: {response.json().get('message', 'Unknown error')}"}

# Function to fetch currency exchange rate
def get_exchange_rate(from_currency, to_currency, api_key):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "rate": data["conversion_rate"],
            "time": data["time_last_update_utc"]
        }
    else:
        return {"error": f"Unable to fetch exchange rate: {response.json().get('message', 'Unknown error')}"}

# Streamlit application
def app():
    st.title("Real-Time Data Application")
    st.markdown("Fetch current weather information or live currency exchange rates.")

    # User inputs for API keys
    weather_api_key = st.text_input("Enter your OpenWeatherMap API Key:", type="password")
    exchange_api_key = st.text_input("Enter your ExchangeRate-API Key:", type="password")

    if not weather_api_key or not exchange_api_key:
        st.warning("Please enter both API keys to proceed.")
        return

    # Tabs for weather and exchange rate
    tab1, tab2 = st.tabs(["🌦 Weather", "💱 Currency Exchange Rates"])
    
    with tab1:
        st.header("Weather Information")
        city = st.text_input("Enter a city name:")
        if st.button("Get Weather"):
            if city:
                weather_data = get_weather(city, weather_api_key)
                if "error" in weather_data:
                    st.error(weather_data["error"])
                else:
                    st.write(f"### Weather in {city.title()}")
                    st.write(f"**Temperature:** {weather_data['temperature']}°C")
                    st.write(f"**Description:** {weather_data['description'].capitalize()}")
                    st.write(f"**Humidity:** {weather_data['humidity']}%")
                    st.write(f"**Wind Speed:** {weather_data['wind_speed']} m/s")
            else:
                st.error("Please enter a city name.")

    with tab2:
        st.header("Currency Exchange Rates")
        from_currency = st.text_input("From Currency (e.g., USD):")
        to_currency = st.text_input("To Currency (e.g., EUR):")
        if st.button("Get Exchange Rate"):
            if from_currency and to_currency:
                exchange_data = get_exchange_rate(from_currency.upper(), to_currency.upper(), exchange_api_key)
                if "error" in exchange_data:
                    st.error(exchange_data["error"])
                else:
                    st.write(f"### Exchange Rate: {from_currency.upper()} to {to_currency.upper()}")
                    st.write(f"**Rate:** {exchange_data['rate']}")
                    st.write(f"**Last Updated:** {exchange_data['time']}")
            else:
                st.error("Please enter both currencies.")

if __name__ == "__main__":
    app()
