import hashlib

def md5(input_string):
    # Convert the input string to bytes (required for hashlib functions)
    input_bytes = input_string.encode('utf-8')

    # Create an MD5 hash object
    md5_hash = hashlib.md5()

    # Update the hash object with the input bytes
    md5_hash.update(input_bytes)

    # Get the hexadecimal representation of the MD5 hash
    md5_hex_digest = md5_hash.hexdigest()

    return md5_hex_digest


