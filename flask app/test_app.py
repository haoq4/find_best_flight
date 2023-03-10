import pandas as pd
import json
from flask import Flask, render_template

# This test_app is used for testing the results.html, it was given a
# best_flights.json file and to test the result table
app = Flask(__name__)

# Load the JSON data into a Python object
with open('best_flights.json', encoding='utf-8') as f:
    data = json.load(f)

# Extract the relevant data from the JSON object
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

# Create a dataframe from the extracted data
df = pd.DataFrame(items)

@app.route('/')
def results():
    return render_template('results.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)
