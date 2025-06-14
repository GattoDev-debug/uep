import argparse
import sys
import json
import random

from encoder import multi_pass_encode
from decoder import multi_pass_decode

def main():
    parser = argparse.ArgumentParser(description="Encode or decode a file.")
    parser.add_argument('-enc', action='store_true', help='Encode the file')
    parser.add_argument('-dec', action='store_true', help='Decode the file')
    parser.add_argument('-repeat', type=int, default=5, help='Number of encode/decode passes (default: 5)')
    parser.add_argument('-seed', type=int, default=None, help='Base seed for encoding (default: random)')
    parser.add_argument('infile', type=str, help='Input file path')
    parser.add_argument('outfile', type=str, help='Output file path')
    args = parser.parse_args()

    if args.enc == args.dec:
        print("Specify either -encode or -decode, not both.", file=sys.stderr)
        sys.exit(1)

    marker = b'\n---ENCODED-METADATA---\n'

    if args.enc:
        with open(args.infile, 'rb') as f:
            content = f.read()
        base_seed = args.seed if args.seed is not None else random.randint(1, 1000000)
        encoded, all_metadata = multi_pass_encode(content, base_seed, passes=args.repeat)
        metadata = {
            "all_metadata": all_metadata,
            "base_seed": base_seed,
            "repeat": args.repeat
        }
        with open(args.outfile, 'wb') as f:
            f.write(encoded + marker + json.dumps(metadata).encode('utf-8'))
        print(f"Encoding complete. Seed used: {base_seed}")

    elif args.dec:
        with open(args.infile, 'rb') as f:
            filedata = f.read()
        if marker not in filedata:
            print("Invalid encoded file format.", file=sys.stderr)
            sys.exit(1)
        encoded, metadata_bytes = filedata.split(marker, 1)
        try:
            metadata = json.loads(metadata_bytes.decode('utf-8'))
            all_metadata = metadata["all_metadata"]
        except Exception:
            print("Invalid encoded file format.", file=sys.stderr)
            sys.exit(1)
        decoded = multi_pass_decode(encoded, all_metadata)
        with open(args.outfile, 'wb') as f:
            f.write(decoded)
        print("Decoding complete.")

if __name__ == "__main__":
    main()
