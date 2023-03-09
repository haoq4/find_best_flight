import pandas as pd
import requests
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

ACCESS_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiYzgyMjE5ZWJlNG' \
             'YxMzZlMGIwZTBhZDU2MThkODEzNDJmZmZkZDI5Y2E5YzNmZDY5NzYyZmViZTllNDAxM2QyMzRlZ' \
             'jRhMDNkMzcxNjAyNWMiLCJpYXQiOjE2NzgxNTEyMjQsIm5iZiI6MTY3ODE1MTIyNCwiZXhwIjox' \
             'NzA5NzczNjI0LCJzdWIiOiIyMDM2OCIsInNjb3BlcyI6W119.hwkEH5xoJgK9cLCscfK3I9L94Ww' \
             'EEgnuiRCqmIpeSmSYrgsDh6RLDWCukXFOIzX8Ym6odxMMkW2EdJSq9ZpSyQ'

def get_total_hours(start_time, end_time):
    duration = end_time - start_time
    total_seconds = duration.total_seconds()
    total_hours = total_seconds / 3600
    return round(total_hours, 2)

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
        'access_key': ACCESS_KEY,
        'origin': origin,
        'destination': destination,
        'departureDate': departureDate,
        'returnDate': returnDate,
        'adults': adults,
        'currency': 'USD'
    }

    # send API request
    response = requests.get('https://app.goflightlabs.com/search-best-flights', params=params)
    data = response.json() # this data is dict for now

    # Create a dataframe from the JSON data
    buckets = data['data']['buckets']
    items = []
    for bucket in buckets:
        quality = bucket['name']
        for item in bucket['items']:
            start_time = item['legs'][0]['departure'].replace('T', ' ')
            end_time = item['legs'][0]['arrival'].replace('T', ' ')
            total_hour = get_total_hours(datetime.fromisoformat(start_time),
                                         datetime.fromisoformat(end_time))
            stop_count = item['legs'][0]['stopCount']
            stop_airport = []
            for num in range(stop_count):
                stop_airport.append(item['legs'][0]['segments'][num]['destination']['flightPlaceId'])
            items.append({
                'quality': quality,
                'price': item['price']['formatted'],
                'origin': item['legs'][0]['origin']['id'],
                'destination': item['legs'][0]['destination']['id'],
                'stop count': stop_count,
                'stop airport': stop_airport,
                'total time(hr)': total_hour,
                'departure': start_time,
                'arrival': end_time,
                'carrier': item['legs'][0]['segments'][0]['marketingCarrier']['name'],
                'flightNumber': item['legs'][0]['segments'][0]['marketingCarrier']['alternateId'] + '' +
                            item['legs'][0]['segments'][0]['flightNumber'],
                'link': item['deeplink']
            })

    # Create a dataframe from the extracted data
    df = pd.DataFrame(items)
    #save as csv file
    df.to_csv('best_flights.csv')

    # render results_test.html template
    return render_template('results_test.html', items=items)


if __name__ == '__main__':
    app.run(debug=True)
