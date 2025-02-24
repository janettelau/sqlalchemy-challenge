# sqlalchemy-challenge
**Objective**: Using Python, SQLAlchemy, and Flask to conduct a climate analysis about Honolulu, Hawaii and design a Flask API.

## Tools and Libraries
- Visual Studio Code
- Python
- Pandas
- Matplotlib
- NumPy
- DateTime
- SQLAlchemy

## Setup and Usage
1. Clone this repository to your local machine using `git clone`.
2. Navigate to the cloned directory in Visual Studio Code.
3. Open the Jupyter Notebook `climate_starter.ipynb`.
4. Run each cell sequentially to load the data and perform queries for data analysis.
5. To run the Flask API, navigate to the directory that contains the Flask app using the terminal.
6. Run the command `python app.py`, then open the API URL (http://127.0.0.1:5000/) the terminal provides.
7. Access the API data in your browser using the available API routes, an example of the expected format is `http://127.0.0.1:5000/api/v1.0/precipitation`.
8. To access the `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>` routes, replace `<start>` and `<end>` with dates in the YYYY-MM-DD format, e.g. `http://127.0.0.1:5000/api/v1.0/2016-08-23/2016-10-23`.

## Project Breakdown
#### Part 1: Database Connection
* Connected to the SQLite database and reflect the tables into classes.
* Created a SQLAlchemy session to link Python to the database.

#### Part 2: Climate Analysis
* Precipitation Analysis:
  * Performed a query to retrieve data and precipitation scores over the past year.
  * Plotted a bar chart showing precipitation in inches over time.
* Station Analysis:
  * Queried the stations and found the minimum, average, and maximum temperatures for the most active station.

#### Part 3: Flask API
* Designed a Flask API with the following static and dynamic routes:
  * `/`: Homepage with a list of available routes.
  * `/api/v1.0/precipitation`: Returns a JSON dictionary of the precipitation data of the last 12 months.
  * `/api/v1.0/stations`: Returns a JSON list of stations.
  * `/api/v1.0/tobs`: Returns a JSON list of temperature observation data of the most active station for the previous year.
  * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`: Returns the minimum, average, and maximum temperatures for the specified start-end range.
 
