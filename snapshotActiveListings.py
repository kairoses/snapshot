import requests
import json
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
import argparse

# Load environment variables
load_dotenv()

def fetch_all_listings(base_url, headers):
    all_listings = []
    continuation = None
    
    while True:
        # Construct URL with continuation token if it exists
        current_url = base_url
        if continuation:
            current_url += f"&continuation={continuation}"
            
        # Make API request
        response = requests.get(current_url, headers=headers)
        
        # Check if request was successful
        if response.status_code != 200:
            print(f"Error: API request failed with status code {response.status_code}")
            break
            
        # Parse response
        data = response.json()
        
        # Add orders to our collection
        if 'orders' in data:
            all_listings.extend(data['orders'])
        
        # Check if there's more data to fetch
        continuation = data.get('continuation')
        print(f"Fetched {len(data['orders'])} listings...")
        
        if not continuation:
            break
    
    return all_listings

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Fetch NFT listings from Reservoir API')
    parser.add_argument('--contract', '-c', 
                       help='Contract address to fetch listings for',
                       default=os.getenv('DEFAULT_CONTRACT_ADDRESS'))
    args = parser.parse_args()
    
    # Get contract address from args or env, with fallback
    contract_address = args.contract
    if not contract_address:
        contract_address = "0xb3443b6bd585ba4118cae2bedb61c7ec4a8281df"  # fallback default
        print(f"No contract address provided, using default: {contract_address}")
    
    base_url = f"https://api-apechain.reservoir.tools/orders/asks/v5?contracts={contract_address}&status=active&sortBy=updatedAt&limit=1000"
    headers = {
        "accept": "*/*",
        "x-api-key": os.getenv('RESERVOIR_API_KEY')
    }
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Fetch all listings
    print("Fetching listings...")
    all_listings = fetch_all_listings(base_url, headers)
    
    # Convert to DataFrame with explicit flattening
    df = pd.json_normalize(
        all_listings,
        sep='_',
        record_path=None,
        meta=[
            'id', 'kind', 'side', 'status', 'tokenSetId', 'tokenSetSchemaHash',
            'contract', 'contractKind', 'maker', 'taker',
            ['price', 'currency', 'contract'],
            ['price', 'currency', 'name'],
            ['price', 'currency', 'symbol'],
            ['price', 'currency', 'decimals'],
            ['price', 'amount', 'raw'],
            ['price', 'amount', 'decimal'],
            ['price', 'amount', 'usd'],
            ['price', 'amount', 'native'],
            ['price', 'netAmount', 'raw'],
            ['price', 'netAmount', 'decimal'],
            ['price', 'netAmount', 'usd'],
            ['price', 'netAmount', 'native'],
            'validFrom', 'validUntil',
            'quantityFilled', 'quantityRemaining',
            'dynamicPricing',
            ['criteria', 'kind'],
            ['criteria', 'data', 'token', 'tokenId'],
            ['source', 'id'],
            ['source', 'domain'],
            ['source', 'name'],
            ['source', 'icon']
        ]
    )
    
    # Rename columns to be more readable
    df.columns = df.columns.str.replace('.', '_')
    
    # Generate timestamp for file names
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Save to CSV
    csv_filename = f"data/active_listings_{timestamp}_{contract_address}.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Saved CSV file: {csv_filename}")
    
    # Save to JSON
    json_filename = f"data/active_listings_{timestamp}_{contract_address}.json"
    with open(json_filename, "w") as f:
        json.dump(all_listings, f)
    print(f"Saved JSON file: {json_filename}")

if __name__ == "__main__":
    main()
