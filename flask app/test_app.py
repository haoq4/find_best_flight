import pandas as pd
import json
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

# Load the JSON data into a Python object
with open('best_flights.json', encoding='utf-8') as f:
    data = json.load(f)

# Extract the relevant data from the JSON object
buckets = data['data']['buckets']
items = []

# this function will return the total hour between start time and end time
def get_total_hours(start_time, end_time):
    duration = end_time - start_time
    total_seconds = duration.total_seconds()
    total_hours = total_seconds / 3600
    return round(total_hours, 2)

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

@app.route('/')
def results():
    return render_template('results_test.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)
