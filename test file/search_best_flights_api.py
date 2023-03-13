import requests
import json

#ACCESS_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiOTUzYmFlYjdlNzZmZTM3ZTdmN2EwYjRlNzA5ZmIwYjQ0NTY2ODZlM2MyNWVhNzczMGRkZmRhYmQzMzg5MTBiYTcxZGQ5NmRiNGQ2N2Y2MzUiLCJpYXQiOjE2Nzg1ODA1MzQsIm5iZiI6MTY3ODU4MDUzNCwiZXhwIjoxNzEwMjAyOTM0LCJzdWIiOiIyMDQyMyIsInNjb3BlcyI6W119.KNPlME2xni0aTFx4gInGaHIQBBsWszGNr8RIHbWBr83C2ekTWaIXWrarXyhSPSNoIcWmElUbUoJxDKZPJwCxDQ'

#url = "https://app.goflightlabs.com/search-best-flights"
url = "https://skyscanner44.p.rapidapi.com/search"


# Set the request parameters
params = {
    #'access_key': ACCESS_KEY,
    'adults': 1,
    'origin': 'CKG',
    'destination': 'PEK',
    'departureDate': '2023-03-18',
    'returnDate': '2023-03-19',
    #'returnDate': None,
    'cabinClass': None,
    'currency': 'USD',
    'childAge1': None,
    'childAge2': None,
    'childAge3': None
}


headers = {
	"X-RapidAPI-Key": "02ba8894e0msh39e4584d49e4b52p1dc2cajsn2f1ba40ea936",
	"X-RapidAPI-Host": "skyscanner44.p.rapidapi.com"
}

# Make API request
#response = requests.get('https://app.goflightlabs.com/search-best-flights', params=params)

response = requests.get(url, headers=headers, params=params)

# parse the response data into a Python object
data = response.json()

# write the data to a file
with open("best_flights.json", "w") as f:
    json.dump(data, f, indent=4)

print('Finish search!')