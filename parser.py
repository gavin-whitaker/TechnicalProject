import json
import sys

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