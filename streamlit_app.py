import requests
import csv
import streamlit as st
import pandas as pd
from io import StringIO

# Your Discogs API key
API_KEY = 'any_is_OK'
BASE_URL = 'https://api.discogs.com/releases/'

def fetch_barcode(discogs_id):
    headers = {
        'User-Agent': 'YourAppName/1.0',
        'Authorization': f'Discogs key={API_KEY}'
    }
    response = requests.get(f"{BASE_URL}{discogs_id}", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # Extract barcode from identifiers
        barcodes = [identifier['value'] for identifier in data.get('identifiers', []) if identifier['type'] == 'Barcode']
        return barcodes
    else:
        print(f"Error fetching ID {discogs_id}: {response.status_code}")
        return []

def main():
    st.title("Discogs Barcode Fetcher")
    st.write("Upload a CSV file containing Discogs IDs (one ID per line), with the 1st row be reserved as field name; data start from 2nd row.")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Read the file
        file_content = uploaded_file.getvalue().decode("utf-8")
        discogs_ids = file_content.splitlines()

        # Prepare results
        results = []

        for discogs_id in discogs_ids:
            discogs_id = discogs_id.strip()
            if discogs_id:  # Ensure it's not empty
                barcodes = fetch_barcode(discogs_id)
                barcode_str = ', '.join(barcodes)
                results.append([discogs_id, barcode_str])

        # Display results as a DataFrame
        if results:
            df = pd.DataFrame(results, columns=['Discogs ID', 'Barcodes'])
            st.write("Fetched Barcodes:")
            st.dataframe(df)

            # Provide download link for the results
            csv = df.to_csv(index=False)
            st.download_button("Download Barcodes CSV", csv, "barcodes.csv", "text/csv")

if __name__ == "__main__":
    main()
