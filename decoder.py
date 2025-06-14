# Remove inserted code chunks from the encoded content using the metadata
def decode_bytes(encoded: bytes, inserted: list):
    for pos, chunk_hex in sorted(inserted, reverse=True):
        chunk = bytes.fromhex(chunk_hex)
        encoded = encoded[:pos] + encoded[pos+len(chunk):]
    return encoded

# Perform multiple passes of decoding in reverse order to restore the original content
def multi_pass_decode(encoded: bytes, all_metadata: list):
    for meta in reversed(all_metadata):
        inserted = [(int(pos), chunk) for pos, chunk in meta["inserted"]]
        encoded = decode_bytes(encoded, inserted)
    return encoded