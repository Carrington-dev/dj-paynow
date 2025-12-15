
# ============================================================================
# paynow/utils.py
# ============================================================================
import hashlib
import random
import string
from urllib.parse import urlencode


def generate_payment_id(prefix="PN", length=12):
    """Generate unique payment ID like PN18K07G4P9XY"""
    remaining = length - len(prefix)
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choice(chars) for _ in range(remaining))
    return prefix + random_part


def generate_hash(data_dict, integration_key):
    """
    Generate PayNow security hash
    
    Args:
        data_dict: Dictionary of payment data (sorted by keys)
        integration_key: PayNow integration key
    
    Returns:
        SHA512 hash string
    """
    # Sort data by keys
    sorted_data = sorted(data_dict.items())
    
    # Create string from sorted data
    values_string = ''.join([str(value) for key, value in sorted_data])
    
    # Append integration key
    hash_string = values_string + integration_key
    
    # Generate SHA512 hash
    return hashlib.sha512(hash_string.encode('utf-8')).hexdigest().upper()


def verify_hash(data_dict, received_hash, integration_key):
    """
    Verify PayNow hash
    
    Args:
        data_dict: Dictionary of received data
        received_hash: Hash received from PayNow
        integration_key: PayNow integration key
    
    Returns:
        Boolean indicating if hash is valid
    """
    calculated_hash = generate_hash(data_dict, integration_key)
    return calculated_hash == received_hash.upper()


def parse_paynow_response(response_text):
    """
    Parse PayNow response string
    
    Args:
        response_text: Response string from PayNow (key=value pairs)
    
    Returns:
        Dictionary of parsed values
    """
    result = {}
    for line in response_text.strip().split('\n'):
        if '=' in line:
            key, value = line.split('=', 1)
            result[key.strip()] = value.strip()
    return result


