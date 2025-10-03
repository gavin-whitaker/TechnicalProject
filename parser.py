import json
import os
import sys
from itertools import combinations, product

def parse_json(filename):
    """
    Parse a JSON file containing a list of items and return a dictionary keyed by item ID.
    
    Args:
        filename (str): Path to the JSON file.
    
    Returns:
        dict: Dictionary with item 'id' as keys and item dictionaries as values.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the JSON is invalid.
        RuntimeError: If required fields are missing or duplicate IDs are found.
        ValueError: If numeric fields have invalid values.
    """
    # Initialize result dictionary
    items_dict = {}
    
    # Define required fields
    required = ("id", "location_id", "length", "width", "price_in_cents")
    
    try:
        with open(filename, "r") as file:
            # Load JSON data
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(f"Invalid JSON in {filename}: {str(e)}", e.doc, e.pos)
            
            # Ensure data is a list
            if not isinstance(data, list):
                raise RuntimeError(f"Invalid format in {filename}: Expected a list of items")
            
            # Process each item
            for i, item in enumerate(data, 1):
                # Check for required fields
                missing = [key for key in required if key not in item]
                if missing:
                    raise RuntimeError(f"Missing required fields at item #{i} in {filename}: {', '.join(missing)}")
                
                # Check for duplicate ID
                item_id = item["id"]
                if item_id in items_dict:
                    raise RuntimeError(f"Duplicate ID '{item_id}' at item #{i} in {filename}")
                
                # Validate numeric fields
                try:
                    length = int(item["length"])
                    width = int(item["width"])
                    price_in_cents = int(item["price_in_cents"])
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid numeric value at item #{i} in {filename} for length, width, or price_in_cents")
                
                # Validate positive values
                if length <= 0:
                    raise ValueError(f"length must be positive at item #{i} in {filename}")
                if width <= 0:
                    raise ValueError(f"width must be positive at item #{i} in {filename}")
                if price_in_cents <= 0:
                    raise ValueError(f"price_in_cents must be positive at item #{i} in {filename}")
                
                # Store item in dictionary
                items_dict[item_id] = item
    
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filename}")
    
    # Check if dictionary is empty
    if not items_dict:
        raise RuntimeError(f"No valid items found in {filename}")
    
    return items_dict

def load_listings():
    listings_path = os.path.join(os.path.dirname(__file__), "listings.json")
    with open(listings_path, "r") as f:
        return json.load(f)

def find_locations(vehicle_requirements):
    listings = load_listings()

    # Group listings by location_id
    locations = {}
    for listing in listings:
        loc_id = listing["location_id"]
        locations.setdefault(loc_id, []).append(listing)

    results = []

    for loc_id, loc_listings in locations.items():
        vehicle_options = []
        for vehicle in vehicle_requirements:
            length = vehicle["length"]
            quantity = vehicle["quantity"]
            suitable = [l for l in loc_listings if l["length"] >= length and l["width"] >= 10]
            if len(suitable) < quantity:
                break  
            vehicle_options.append(list(combinations(suitable, quantity)))
        else:
            cheapest = None
            cheapest_ids = None
            for combo in product(*vehicle_options):
                flat = [item for group in combo for item in group]
                ids = [l["id"] for l in flat]
                if len(set(ids)) != len(ids):
                    continue  
                total_price = sum(l["price_in_cents"] for l in flat)
                if cheapest is None or total_price < cheapest:
                    cheapest = total_price
                    cheapest_ids = ids
            if cheapest is not None:
                results.append({
                    "location_id": loc_id,
                    "listing_ids": cheapest_ids,
                    "total_price_in_cents": cheapest
                })
    results.sort(key=lambda x: x["total_price_in_cents"])
    return results