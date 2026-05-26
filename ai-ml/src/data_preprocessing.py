import pandas as pd
import numpy as np

def preprocess_train_data(df):
    """Cleans and engineers spatial features for the Mumbai Local dataset."""
    print("--- Starting Preprocessing ---")
    
    # 1. Standardize column names (lowercase, replace spaces with underscores)
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.strip()
    print(f"Standardized columns: {df.columns.tolist()}")

    # 2. Handle missing values & engineer station features
    # Dynamically checking for 'station' or 'station_name'
    station_col = next((col for col in ['station', 'station_name'] if col in df.columns), None)
    
    if station_col:
        df[station_col] = df[station_col].fillna('Unknown_Station')
        # Convert text station names into numeric codes for Machine Learning models
        df['station_encoded'] = df[station_col].astype('category').cat.codes
        print(f"Encoded '{station_col}' into numeric feature: 'station_encoded'.")
    else:
        print("Note: Station column not found.")

    # 3. Engineer Railway Line features (Western, Central, Harbour)
    # Dynamically checking for 'line', 'route', or 'railway_line'
    line_col = next((col for col in ['line', 'route', 'railway_line'] if col in df.columns), None)
    
    if line_col:
        df[line_col] = df[line_col].fillna('Unknown_Line')
        # Convert text line names into numeric codes
        df['line_encoded'] = df[line_col].astype('category').cat.codes
        print(f"Encoded '{line_col}' into numeric feature: 'line_encoded'.")
    else:
        print("Note: Line/Route column not found.")
        
    # 4. Handle Distance column (if applicable, ensuring it is a float)
    distance_col = next((col for col in ['distance', 'km', 'distance_from_source'] if col in df.columns), None)
    
    if distance_col:
        # Strip any string characters (like 'km') and convert to float
        df[distance_col] = df[distance_col].astype(str).str.replace(r'[^\d.]', '', regex=True)
        df[distance_col] = pd.to_numeric(df[distance_col], errors='coerce').fillna(0.0)
        print(f"Cleaned and converted '{distance_col}' to numeric.")

    print("--- Preprocessing Complete ---")
    return df

if __name__ == "__main__":
    from data_ingestion import load_local_train_data
    
    raw_df = load_local_train_data()
    if raw_df is not None:
        processed_df = preprocess_train_data(raw_df)
        print("\nPreview of processed data:")
        print(processed_df.head())