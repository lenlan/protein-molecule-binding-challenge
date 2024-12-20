import requests
import concurrent.futures
import time
import pandas as pd
from threading import Semaphore

# Function to fetch SMILES for a list of CIDs (bulk request)
def fetch_smiles_bulk(cids, retries=3, timeout=10):
    """
    Fetch SMILES for a list of CIDs in a single request with retry mechanism.
    """
    # Create a comma-separated list of CIDs
    cid_list = ",".join(map(str, cids))
    
    # API URL for bulk retrieval of SMILES
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid_list}/property/CanonicalSMILES/JSON"

    rate_limiter = Semaphore(5)  # Limit to 5 requests at a time
    
    for attempt in range(retries):
        try:
            # Use the rate limiter to ensure the limit of 5 requests per second
            with rate_limiter:
                response = requests.get(url, timeout=timeout)
                response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
                if response.status_code == 200:
                    # Extract SMILES from the response
                    smarts_data = response.json()
                    smarts = {str(item['CID']): item['CanonicalSMILES'] for item in smarts_data["PropertyTable"]["Properties"]}
                    return smarts, True
                else:
                    print(f"Unexpected response code: {response.status_code} for CIDs {cid_list}")
                    return {}, False
        except requests.exceptions.Timeout:
            print(f"Request timed out for CIDs {cid_list}. Retrying ({attempt + 1}/{retries})...")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for CIDs {cid_list}. Error: {e}. Retrying ({attempt + 1}/{retries})...")
        time.sleep(2 ** attempt)  # Exponential backoff for retries
    
    print(f"Failed to fetch SMILES for CIDs {cid_list} after {retries} retries.")
    return {}, False

# Function to fetch SMILES in parallel with caching and rate limiting
def fetch_smiles_parallel(cids, batch_size=100, retries=3, timeout=10):
    """
    Fetch SMILES for a list of CIDs using parallel requests with caching.
    """
    all_smiles = {}
    failed_cids = []  # List to track failed CIDs
    REQUEST_INTERVAL = 1 / 5  # Time between requests (5 per second)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:  # Limit concurrency to 5 threads
        # Split the CIDs into batches of 'batch_size' (100 CIDs per batch)
        batches = [cids[i:i+batch_size] for i in range(0, len(cids), batch_size)]
        
        # Use ThreadPoolExecutor to fetch SMILES in parallel
        future_to_batch = {executor.submit(fetch_smiles_bulk, batch, retries, timeout): batch for batch in batches}
        
        for future in concurrent.futures.as_completed(future_to_batch):
            batch = future_to_batch[future]
            try:
                result, success = future.result()
                if result:
                    all_smiles.update(result)
                else:
                    if not success:
                        failed_cids.extend(batch)
            except Exception as e:
                print(f"Error processing batch {batch}: {e}")
                failed_cids.extend(batch)
            time.sleep(REQUEST_INTERVAL)  # Ensure requests are spaced out

    print(f"Failed to retrieve SMILES for {len(failed_cids)} CIDs.")
    return all_smiles, failed_cids