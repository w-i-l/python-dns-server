def convert_bytes_to_int(data: bytes) -> int:
    '''
    Returns the integer representation of the bytes with big endian byte order
    '''
    return int.from_bytes(data, byteorder='big')