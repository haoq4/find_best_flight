# Find Best Flight
The complete program is in the folder: (final search best flight app).  
Other folder is containing test file and small function.

Stats418 class in winter23

Name: Hao Qiu
UID: 406090766

## Describtion
This program is written in Python and uses the Skyscanner API to retrieve real-time flight and ticket information. Users can input their desired information, such as departure and arrival cities, dates, number of passengers, etc., to obtain a JSON format file. The program analyzes the flight data and lists the best, most direct, and cheapest flights for users to choose from.

## Features
* Connects to the Skyscanner API to retrieve real-time flight and ticket information.
* Allows users to input their desired information to search for flights.
* Automatically analyzes flight data and lists the best, most direct, and cheapest flights for users to choose from.
* Based on the Flask framework and deployed on AWS Elastic Beanstalk cloud servers.
* Users can access the main page by entering a URL in their browser, input their information, and receive their search results.
* Supports multiple languages, users can choose to use English or Chinese to conduct their search.

## Installation
1. Clone the program code
```
git clone https://github.com/haoq4/find_best_flight.git
```
2. Install the dependency libraries
```
pip install -r requirements.txt
```
3. Get the Skyscanner API Key
```
Register on the Skyscanner website and obtain an API Key, then configure it in the program.
Url: https://rapidapi.com/3b-data-3b-data-default/api/skyscanner44
```
4. Configure program parameters  
```
Set the headers X-RapidAPI-Key, X-RapidAPI-Host, in the program to your own values.
headers = {
    "X-RapidAPI-Key": "*************",
    "X-RapidAPI-Host": "*****************"
}
```
5. Run the program
```
In the terminal, go to the directory where the program is located and execute the command:
python app.py
Then enter the URL: http://localhost:5000 in your browser to enter the main page.
```

## Configuration
The .ebextensions folder contains the python.config file which is used for running in the AWS Elastic Beanstalk

## File Description
* app.py: Flask application code
* requirements.txt: Includes a list of all the Python packages that are required by your project to run.
* templates/index.html: Main page template file
* templates/results.html: Result page template file
* .ebextensions/python.config: Used for running in the AWS Elastic Beanstalk

## Author
This program is written by Hao Qiu, if you have any questions, please contact haoq4@ucla.edu.











