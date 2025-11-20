from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import pandas as pd
import time

# creating global geolocator
geolocator = Nominatim(
    user_agent="Hospital_Finder",
    timeout=15
)

def geocode_address(address: str):
    """Convert address → latitude/longitude (optimized)."""
    try:
        location = geolocator.geocode(address)
        if not location:
            return {
                "status": "error",
                "message": "coordinates not found",
                "data": {
                    "address": address,
                    "lat": None,
                    "lng": None
                }
            }
        
        return {
            "status": "success",
            "message": "coordinates found",
            "data": {
                "address": address,
                "lat": location.latitude,
                "lng": location.longitude
            }
        }

    except (GeocoderTimedOut, GeocoderServiceError) as e:
        return {
            "status": "error",
            "message": "coordinates not found",
            "data": {
                "address": address,
                "lat": None,
                "lng": None
            }
        }

def process_hospital_data():
    """Read CSV file and geocode hospital addresses"""
    
    # Read the CSV file
    try:
        df = pd.read_csv('locate_hospital.csv')
        print(f"Successfully loaded CSV with {len(df)} rows")
        print("=" * 60)
    except FileNotFoundError:
        print("Error: 'locate_hospital.csv' file not found!")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    # Check if required columns exist
    required_columns = ['name', 'district', 'latitude', 'longitude']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: Missing required columns: {missing_columns}")
        return
    
    # Process each row and update coordinates in dataframe
    success_count = 0
    error_count = 0
    
    for index, row in df.iterrows():
        # Create address string
        address = f"{row['name']}, {row['district']}, Nepal"
        
        # Get coordinates
        result = geocode_address(address)
        
        if result['status'] == 'success':
            # Update the dataframe with coordinates
            df.at[index, 'latitude'] = result['data']['lat']
            df.at[index, 'longitude'] = result['data']['lng']
            success_count += 1
            
            # Display on screen
            print(f"Row {index + 1}:")
            print(f"  Hospital Name: {row['name']}")
            print(f"  District: {row['district']}")
            print(f"  Latitude: {result['data']['lat']}")
            print(f"  Longitude: {result['data']['lng']}")
            print("  Status: ✓ Coordinates found and written to CSV")
            
        else:
            # Update with None if coordinates not found
            df.at[index, 'latitude'] = None
            df.at[index, 'longitude'] = None
            error_count += 1
            
            # Display on screen
            print(f"Row {index + 1}:")
            print(f"  Hospital Name: {row['name']}")
            print(f"  District: {row['district']}")
            print(f"  Latitude: Not found")
            print(f"  Longitude: Not found")
            print("  Status: ✗ Coordinates not found")
        
        print()  # Empty line for separation
        
        # Add a small delay to be respectful to the geocoding service
        time.sleep(1)
    
    # Save the updated dataframe back to CSV
    try:
        df.to_csv('locate_hospital.csv', index=False)
        print("=" * 60)
        print(f"Processing completed!")
        print(f"Successfully geocoded: {success_count} hospitals")
        print(f"Failed to geocode: {error_count} hospitals")
        print(f"All data saved to 'locate_hospital.csv'")
    except Exception as e:
        print(f"Error saving CSV file: {e}")

# Run the processing
if __name__ == "__main__":
    process_hospital_data()