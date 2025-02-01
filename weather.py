import requests

def weather(city = 'gandhinagar'):
    API_KEY = "df65fcfc64115fbeb40a7488c4e95c83" 
    # city = 'gandhinagar'
    url = f"http://api.weatherstack.com/current?access_key={API_KEY}&query={city}"
    response = requests.get(url)
    data = response.json()
    if 'current' in data:
        temp = data["current"]["temperature"]
        desc = data["current"]["weather_descriptions"][0]
        return f"Weather in {city}: {temp}°C, {desc}"
    
# print(weather())
