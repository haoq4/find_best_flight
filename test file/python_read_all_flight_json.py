import pandas as pd
import json
from datetime import datetime
import jsonpath

# load JSON data
with open('all_flights_example2.json', 'r') as f:
    data = json.load(f)

# create DataFrame
#flights = pd.DataFrame()
# json_data = json.dumps(data)
# ret = jsonpath.jsonpath(data, '$..origin.name')
#
# # print DataFrame
# print(ret)



# this function will return the total hour between start time and end time
def get_total_hours(start_time, end_time):
    duration = end_time - start_time
    total_seconds = duration.total_seconds()
    total_hours = total_seconds / 3600
    return round(total_hours, 2)


# Extract the relevant data from the JSON object
results = data['data']['results']
items = []

for result in results:
    start_time = result['legs'][0]['departure']
    end_time = result['legs'][0]['arrival']
    total_hour = get_total_hours(datetime.fromisoformat(start_time),
                                 datetime.fromisoformat(end_time))
    stop_count = result['legs'][0]['stopCount']
    stop_airport = []

    for num in range(stop_count):
        stop_airport.append(result['legs'][0]['segments'][num]['destination']['flightPlaceId'])
    items.append({
        'id': result['id'],
        #'price options': result['pricing_options'],
        'origin': result['legs'][0]['origin']['displayCode'],
        'destination': result['legs'][0]['destination']['displayCode'],
        'stop count': stop_count,
        'stop airport': stop_airport,
        'total time(hr)': total_hour,
        'departure': start_time,
        'arrival': end_time,
        'carrier': result['legs'][0]['carriers']['marketing'][0]['name'],
        'flightNumber': result['legs'][0]['segments'][0]['marketingCarrier']['alternate_di'] + '' +
                        result['legs'][0]['segments'][0]['flightNumber'],
        'price options': result['pricing_options']
        #'link': result['deeplink']
    })

# Create a dataframe from the extracted data
df = pd.DataFrame(items)



# Print the dataframe as a table
print(df.to_string())

# save as csv file
df.to_csv('all_flight.csv')