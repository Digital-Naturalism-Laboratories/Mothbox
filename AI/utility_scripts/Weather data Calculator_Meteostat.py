# Weather data Calculator
"""
INPUT - CSV with relevant columns

latitude: The latitude of the location.
longitude: The longitude of the location.
eventDate: The date of the event (ISO 8601 format).
eventTime: The time of the event (HH:MM:SS±HHMM format).
"""

# Define the input path
import pandas as pd
from meteostat import Point, Hourly
from datetime import datetime, timedelta, timezone
import pytz

# Define the input path
INPUT_PATH = r'E:\Panama\Boquete_Houseside_CuatroTopo _2025-01-03\2025-01-03\Boquete_Houseside_CuatroTopo _2025-01-03_2025-01-03_exportdate_2025-01-13.csv'

def parse_datetime_string(date_time_str):
  """
  Parses a datetime string in the format "YYYY-MM-DD HH:MM:SS" 
  and creates a datetime object.

  Args:
    date_time_str: The datetime string to parse.

  Returns:
    A datetime object.
  """
  try:
    year, month, day = map(int, date_time_str[:10].split('-'))
    hour, minute, second = map(int, date_time_str[11:].split(':'))
    return datetime(year, month, day, hour, minute, second)
  except ValueError:
    print("Invalid datetime string format. Expected 'YYYY-MM-DD HH:MM:SS'")
    return None


def calculate_weather_data(input_path):
    # Read the CSV
    data = pd.read_csv(input_path)

    # Prepare new columns
    temp_values = []
    dew_point_values = []
    wind_direction_values = []
    wind_speed_values = []
    wind_peak_gust_values = []
    relative_humidity_values = []
    pressure_values = []
    weather_code_values = []

    # Iterate over each row to fetch weather data
    for _, row in data.iterrows():
        try:
            # Extract necessary fields
            lat = row['latitude']
            lon = row['longitude']
            event_date = row['eventDate']  # Format: 2025-01-04T04:04:06-0500

            # Parse the event date with UTC offset
            event_datetime = datetime.strptime(event_date, '%Y-%m-%dT%H:%M:%S%z')

            # Convert to UTC timezone explicitly
            utc_datetime = event_datetime.astimezone(timezone.utc)

            # Add one hour to the UTC datetime 
            utc_datetime_plus1 = utc_datetime + timedelta(hours=1) 
            # Convert UTC datetime back to ISO 8601 string (including UTC offset)
            utc_datetime = datetime.strftime(datetime.fromisoformat(str(utc_datetime)),"%Y-%m-%d %H:%M:%S") 
            utc_datetime_plus1 = datetime.strftime(datetime.fromisoformat(str(utc_datetime_plus1)),"%Y-%m-%d %H:%M:%S") 

            print(utc_datetime)
            utc_datetime=parse_datetime_string(str(utc_datetime))
            utc_datetime_plus1=parse_datetime_string(str(utc_datetime_plus1))

            # Create Meteostat Point
            location = Point(lat, lon)
            location.radius=70000 #maximum distance
            #TODO - make calculation to also show distance to nearest station it reads data from
            # Fetch hourly weather data for the given time
            weather_data = Hourly(location, start=utc_datetime, end=utc_datetime_plus1 )
            weather_data = weather_data.fetch()

            # Check if data exists
            if not weather_data.empty:
                row_data = weather_data.iloc[0]  # Take the first (and only) row

                # Append results
                temp_values.append(row_data.get("temp", None))
                dew_point_values.append(row_data.get("dwpt", None))
                wind_direction_values.append(row_data.get("wdir", None))
                wind_speed_values.append(row_data.get("wspd", None))
                wind_peak_gust_values.append(row_data.get("wpgt", None))
                relative_humidity_values.append(row_data.get("rhum", None))
                pressure_values.append(row_data.get("pres", None))
                weather_code_values.append(row_data.get("coco", None))
            else:
                raise ValueError("No weather data available for this datetime and location")

        except Exception as e:
            print(f"Error processing row: {e}")
            temp_values.append(None)
            dew_point_values.append(None)
            wind_direction_values.append(None)
            wind_speed_values.append(None)
            wind_peak_gust_values.append(None)
            relative_humidity_values.append(None)
            pressure_values.append(None)
            weather_code_values.append(None)

    # Add new columns to the DataFrame
    data['TEMP'] = temp_values
    data['DWPT'] = dew_point_values
    data['WDIR'] = wind_direction_values
    data['WSPD'] = wind_speed_values
    data['WPGT'] = wind_peak_gust_values
    data['RHUM'] = relative_humidity_values
    data['PRES'] = pressure_values
    data['COCO'] = weather_code_values

    # Save the updated CSV
    output_path = input_path.replace('.csv', '_weatherdata.csv')
    data.to_csv(output_path, index=False)
    print(f"Updated CSV saved to: {output_path}")

# Run the function
calculate_weather_data(INPUT_PATH)
