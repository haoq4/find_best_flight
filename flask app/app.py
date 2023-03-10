import requests
import configparser
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')

# read the config.ini file to get the access key of the api
config = configparser.ConfigParser()
config.read('config.ini')
ACCESS_KEY = config.get('API', 'access_key')

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
            for i, leg in enumerate(item['legs']):
                start_time = leg['departure'].replace('T', ' ')
                end_time = leg['arrival'].replace('T', ' ')
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
