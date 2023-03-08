import requests
import json

ACCESS_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiYzgyMjE5ZWJlNG' \
			 'YxMzZlMGIwZTBhZDU2MThkODEzNDJmZmZkZDI5Y2E5YzNmZDY5NzYyZmViZTllNDAxM2QyMzRlZ' \
			 'jRhMDNkMzcxNjAyNWMiLCJpYXQiOjE2NzgxNTEyMjQsIm5iZiI6MTY3ODE1MTIyNCwiZXhwIjox' \
			 'NzA5NzczNjI0LCJzdWIiOiIyMDM2OCIsInNjb3BlcyI6W119.hwkEH5xoJgK9cLCscfK3I9L94Ww' \
			 'EEgnuiRCqmIpeSmSYrgsDh6RLDWCukXFOIzX8Ym6odxMMkW2EdJSq9ZpSyQ'

url = "https://app.goflightlabs.com/search-best-flights"

# Set the request parameters
params = {
    'access_key': ACCESS_KEY,
    'adults': 1,
    'origin': 'SEA',
    'destination': 'LAX',
    'departureDate': '2023-03-17'
}

# Make API request
response = requests.get('https://app.goflightlabs.com/search-best-flights', params=params)
# parse the response data into a Python object
data = response.json()

# write the data to a file
with open("best_flights.json", "w") as f:
    json.dump(data, f, indent=4)

print('end')