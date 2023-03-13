import requests
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__, template_folder='templates')

#ACCESS_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiOTUzYmFlYjdlNzZmZTM3ZTdmN2EwYjRlNzA5ZmIwYjQ0NTY2ODZlM2MyNWVhNzczMGRkZmRhYmQzMzg5MTBiYTcxZGQ5NmRiNGQ2N2Y2MzUiLCJpYXQiOjE2Nzg1ODA1MzQsIm5iZiI6MTY3ODU4MDUzNCwiZXhwIjoxNzEwMjAyOTM0LCJzdWIiOiIyMDQyMyIsInNjb3BlcyI6W119.KNPlME2xni0aTFx4gInGaHIQBBsWszGNr8RIHbWBr83C2ekTWaIXWrarXyhSPSNoIcWmElUbUoJxDKZPJwCxDQ'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search-flights', methods=['GET', 'POST'])
def search_flights():
    # get query string parameters from request.args
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    departureDate = request.args.get('departureDate')
    returnDate = request.args.get('returnDate')
    adults = request.args.get('adults')

    # set the request parameters
    params = {
        #'access_key': ACCESS_KEY,
        'origin': origin.upper(),
        'destination': destination.upper(),
        'departureDate': departureDate,
        'returnDate': returnDate,
        'adults': adults,
        'currency': 'USD'
    }

    # send API request
    headers = {
        "X-RapidAPI-Key": "02ba8894e0msh39e4584d49e4b52p1dc2cajsn2f1ba40ea936",
        "X-RapidAPI-Host": "skyscanner44.p.rapidapi.com"
    }
    url = "https://skyscanner44.p.rapidapi.com/search"
    response = requests.get(url, headers=headers, params=params)
    #response = requests.get('https://app.goflightlabs.com/search-best-flights', params=params)
    data = response.json() # this data is dict for now

    # Create a dataframe from the JSON data
    buckets = data['itineraries']['buckets']
    #buckets = data['data']['buckets']
    items = []
    for bucket in buckets:
        quality = bucket['name']
        for item in bucket['items']:
            for i, leg in enumerate(item['legs']):
                # start_time = leg['departure'].replace('T', ' ')
                # end_time = leg['arrival'].replace('T', ' ')
                start_time = datetime.strptime(leg['departure'], '%Y-%m-%dT%H:%M:%S').strftime("%H:%M %m/%d/%Y")
                end_time = datetime.strptime(leg['arrival'], '%Y-%m-%dT%H:%M:%S').strftime("%H:%M %m/%d/%Y")
                total_hour = f"{leg['durationInMinutes'] // 60}h {leg['durationInMinutes'] % 60}m"
                stop_count = leg['stopCount']
                stop_airport = []
                flight_number = []
                for num in range(stop_count):
                    stop_airport.append(leg['segments'][num]['destination']['flightPlaceId'])
                for segment in leg['segments']:
                    flight_number.append(segment['marketingCarrier']['alternateId'] + '' +
                                         segment['flightNumber'])
                if len(item['legs']) == 1:
                    way = 'One Way'
                else:
                    if i == 0:
                        way = 'Outbound'
                    else:
                        way = 'Return'
                items.append({
                    'quality': quality,
                    'trip type': way,
                    # 'id': leg['id'],
                    'price': item['price']['formatted'],
                    'origin': leg['origin']['id'],
                    'destination': leg['destination']['id'],
                    'stop count': stop_count,
                    'stop airport': stop_airport,
                    'total time': total_hour,
                    'departure': start_time,
                    'arrival': end_time,
                    'carrier': leg['segments'][0]['marketingCarrier']['name'],
                    'flightNumber': flight_number,
                    'link': item['deeplink']
                })

    # render results.html template
    return render_template('results.html', items=items)


if __name__ == '__main__':
    app.run(debug=True)
