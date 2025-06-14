import random

# Insert code_chunks at specified positions in the content, tracking what was inserted and where
def encode_bytes(content: bytes, code_chunks: list, positions: list):
    encoded = content
    offset = 0
    inserted = []
    for pos, chunk in zip(positions, code_chunks):
        encoded = encoded[:pos+offset] + chunk + encoded[pos+offset:]
        inserted.append((pos+offset, chunk.hex()))
        offset += len(chunk)
    return encoded, inserted

# Perform multiple passes of encoding, each time with a different seed and random data
def multi_pass_encode(content: bytes, base_seed: int, passes: int = 5):
    encoded = content
    all_metadata = []
    for i in range(passes):
        seed = base_seed + i
        random.seed(seed)
        garbage_length = random.randint(6, 250)
        code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=garbage_length))
        positions = sorted(random.sample(range(len(encoded) + 1), k=min(10, len(encoded) + 1)))
        chunk_size = max(1, garbage_length // len(positions))
        code_chunks = [code[j:j+chunk_size].encode('latin1') for j in range(0, garbage_length, chunk_size)]
        while len(code_chunks) < len(positions):
            code_chunks.append(b'')
        encoded, inserted = encode_bytes(encoded, code_chunks, positions)
        all_metadata.append({
            "inserted": inserted,
            "seed": seed
        })
    return encoded, all_metadata