import pandas as pd
import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Define the base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS_DIR = os.path.join(BASE_DIR, '..', 'datasets')

def load_local_train_data():
    """Loads the Mumbai Local Train dataset."""
    file_path = os.path.join(DATASETS_DIR, 'mumbai-local', 'Mumbai_Local_Train_Dataset.csv') # Update filename as needed
    try:
        df = pd.read_csv(file_path, encoding='latin1')
        print(f"Successfully loaded Mumbai Local data: {df.shape[0]} rows.")
        return df
    except FileNotFoundError:
        print("Error: Mumbai Local dataset not found. Please check the directory.")
        return None

def load_delay_data():
    """Loads the Train Delay dataset."""
    file_path = os.path.join(DATASETS_DIR, 'train-delays', 'train_delay.csv') # Update filename as needed
    try:
        df = pd.read_csv(file_path, encoding='latin1')
        print(f"Successfully loaded Train Delay data: {df.shape[0]} rows.")
        return df
    except FileNotFoundError:
        print("Error: Train Delay dataset not found.")
        return None

def fetch_weather_data(city="Mumbai"):
    """Fetches real-time weather data from OpenWeather API using secured .env key."""
    # Retrieve the key securely from the environment
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        print("Error: OPENWEATHER_API_KEY not found. Please check your .env file.")
        return None

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Successfully fetched weather data: {data['weather'][0]['description']}, {data['main']['temp']}°C")
        return data
    else:
        print(f"Failed to fetch weather data. Status Code: {response.status_code}")
        return None

if __name__ == "__main__":
    print("--- Starting Data Ingestion ---")
    
    # Test local static datasets
    train_df = load_local_train_data()
    
    # Test dynamic API fetch
    weather_data = fetch_weather_data()