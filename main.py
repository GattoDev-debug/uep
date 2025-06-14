import argparse
import sys
import json
import random
import base64

from encoder import multi_pass_encode
from decoder import multi_pass_decode

# Encode data in base64 multiple times
def multi_b64encode(data: bytes, times: int = 5) -> bytes:
    for _ in range(times):
        data = base64.b64encode(data)
    return data

# Decode data from base64 multiple times
def multi_b64decode(data: bytes, times: int = 5) -> bytes:
    for _ in range(times):
        data = base64.b64decode(data)
    return data

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Encode or decode a file.")
    parser.add_argument('-enc', action='store_true', help='Encode the file')
    parser.add_argument('-dec', action='store_true', help='Decode the file')
    parser.add_argument('-repeat', type=int, default=5, help='Number of encode/decode passes (default: 5)')
    parser.add_argument('-seed', type=int, default=None, help='Base seed for encoding (default: random)')
    parser.add_argument('infile', type=str, help='Input file path')
    parser.add_argument('outfile', type=str, help='Output file path')
    args = parser.parse_args()

    # Ensure only one of -enc or -dec is specified
    if args.enc == args.dec:
        print("Specify either -encode or -decode, not both.", file=sys.stderr)
        sys.exit(1)

    # Marker to separate file content from metadata
    marker = b'\n---ENCODED-METADATA---\n'

    if args.enc:
        # Read input file as bytes
        with open(args.infile, 'rb') as f:
            content = f.read()
        # Use provided seed or generate a random one
        base_seed = args.seed if args.seed is not None else random.randint(1, 1000000)
        # Encode the file content with multi-pass encoding
        encoded, all_metadata = multi_pass_encode(content, base_seed, passes=args.repeat)
        # Prepare metadata for decoding
        metadata = {
            "all_metadata": all_metadata,
            "base_seed": base_seed,
            "repeat": args.repeat
        }
        # Serialize metadata to JSON and encode it in base64 five times
        metadata_bytes = json.dumps(metadata).encode('utf-8')
        metadata_b64 = multi_b64encode(metadata_bytes, times=5)
        # Write encoded content and encoded metadata to output file
        with open(args.outfile, 'wb') as f:
            f.write(encoded + marker + metadata_b64)
        print(f"Encoding complete. Seed used: {base_seed}")

    elif args.dec:
        # Read the encoded file as bytes
        with open(args.infile, 'rb') as f:
            filedata = f.read()
        # Check for the metadata marker
        if marker not in filedata:
            print("Invalid encoded file format.", file=sys.stderr)
            sys.exit(1)
        # Split the file into encoded content and metadata
        encoded, metadata_b64 = filedata.split(marker, 1)
        try:
            # Decode metadata from base64 five times and parse JSON
            metadata_bytes = multi_b64decode(metadata_b64, times=5)
            metadata = json.loads(metadata_bytes.decode('utf-8'))
            all_metadata = metadata["all_metadata"]
        except Exception:
            print("Invalid encoded file format.", file=sys.stderr)
            sys.exit(1)
        # Decode the file content using the metadata
        decoded = multi_pass_decode(encoded, all_metadata)
        # Write the restored content to the output file
        with open(args.outfile, 'wb') as f:
            f.write(decoded)
        print("Decoding complete.")

if __name__ == "__main__":
    main()
