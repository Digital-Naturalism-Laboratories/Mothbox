# Moon Phase Calculator
"""
INPUT - CSV with relevant columns

latitude: The latitude of the location.
longitude: The longitude of the location.
eventDate: The date of the event (ISO 8601 format).
eventTime: The time of the event (HH:MM:SS±HHMM format).
"""

# Define the input and output paths
import pandas as pd
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, get_body
from astropy.coordinates import get_sun
import numpy as np
from datetime import datetime

# Define the input and output paths
INPUT_PATH = r'E:\Panama\Boquete_Houseside_CuatroTopo _2025-01-03\2025-01-03\Boquete_Houseside_CuatroTopo _2025-01-03_2025-01-03_exportdate_2025-01-13.csv'
def calculate_moon_data(input_path):
    # Read the CSV
    data = pd.read_csv(input_path)

    # Prepare new columns
    moon_phases = []
    moon_altitudes = []
    moon_azimuths = []

    # Iterate over each row to calculate moon data
    for _, row in data.iterrows():
        try:
            # Extract necessary fields
            lat = row['latitude']
            lon = row['longitude']
            event_date = row['eventDate']
            event_time = row['eventTime']

            # Parse date and time
            event_datetime = datetime.strptime(event_date[:19], '%Y-%m-%dT%H:%M:%S')
            time = Time(event_datetime)

            # Create EarthLocation for the observer
            location = EarthLocation(lat=lat, lon=lon)

            # Calculate Moon position
            moon = get_body("moon", time, location)
            altaz = moon.transform_to(AltAz(obstime=time, location=location))

            # Moon phase calculation
            sun = get_sun(time)
            elongation = moon.separation(sun)  # Angle between the Moon and Sun
            illumination_fraction = 0.5 * (1 - np.cos(np.radians(elongation.deg)))

            # Append results
            moon_phases.append(illumination_fraction)
            moon_altitudes.append(altaz.alt.deg)
            moon_azimuths.append(altaz.az.deg)

        except Exception as e:
            print(f"Error processing row: {e}")
            moon_phases.append(None)
            moon_altitudes.append(None)
            moon_azimuths.append(None)

    # Add new columns to the DataFrame
    data['moon_illumination'] = moon_phases
    data['moon_altitude'] = moon_altitudes
    data['moon_azimuth'] = moon_azimuths

    # Save the updated CSV
    output_path = input_path.replace('.csv', '_moondata.csv')
    data.to_csv(output_path, index=False)
    print(f"Updated CSV saved to: {output_path}")

# Run the function
calculate_moon_data(INPUT_PATH)