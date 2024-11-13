# NFT Listings Snapshot

This script fetches active NFT listings from the Reservoir API and saves them in both JSON and CSV formats.

## Setup

1. Clone the repository
2. Copy `.env.template` to `.env`:
   ```bash
   cp .env.template .env
   ```
3. Edit `.env` and add your Reservoir API key and default contract address

## Usage

You can run the script in several ways:

1. Using the default contract from .env:
   ```bash
   python snapshotActiveListings.py
   ```

2. Specifying a contract address:
   ```bash
   python snapshotActiveListings.py --contract 0xb3443b6bd585ba4118cae2bedb61c7ec4a8281df
   ```
   or
   ```bash
   python snapshotActiveListings.py -c 0xb3443b6bd585ba4118cae2bedb61c7ec4a8281df
   ```

## Environment Variables

- `RESERVOIR_API_KEY`: Your Reservoir API key
- `DEFAULT_CONTRACT_ADDRESS`: Default NFT contract address to fetch listings for

## Output

Files are saved in the `data` directory with the following naming pattern:
- `data/active_listings_[timestamp]_[contract_address].json`: Raw JSON data
- `data/active_listings_[timestamp]_[contract_address].csv`: Flattened CSV data 