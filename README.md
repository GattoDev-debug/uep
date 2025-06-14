# UEP - Unethical Encryption Protocol
> [!TIP] 
> UEP (Unethical Encryption Protocol) is a playful, multi-pass file obfuscation tool that works with any file format. It repeatedly inserts random data ("garbage") into your files using a variable seed, then removes it in reverse order to restore the original file. UEP is not intended for serious cryptographic use, but can be used for simple file hiding, tamper-evident storage, or educational purposes.

---

## Features

- Works with any file type (binary or text)
- Multi-pass encoding/decoding with configurable repeat count (`-repeat`)
- Randomized "garbage" insertion based on a seed (`-seed`)
- All metadata required for decoding is embedded in the encoded file
- Modular codebase: `main.py`, `encoder.py`, `decoder.py` 
- Simple command-line interface with positional input/output arguments
- Requires no extra dependencies

---

## Usage

### "Encoding" a file

```sh
python main.py -enc [-repeat N] [-seed S] <infile> <outfile>
```

- `-enc` : Encode (scramble) the file
- `-repeat N` : (Optional) Number of encoding passes (default: 5)
- `-seed S` : (Optional) Base seed for encoding (default: random)
- `<infile>` : Path to the input file
- `<outfile>` : Path to the output (encoded) file

**Example:**
```sh
python main.py -enc -repeat 7 -seed 12345 secret.png scrambled.png
```

### "Decoding" a file

```sh
python main.py -dec <infile> <outfile>
```

- `-dec` : Decode (unscramble) the file
- `<infile>` : Path to the encoded file
- `<outfile>` : Path to the output (restored) file

**Example:**
```sh
python main.py -dec scrambled.png restored.png
```

> **Note:** The repeat count and seed are stored in the encoded file and do not need to be specified for decoding.

---

## How does it work?

UEP splits your file into pieces called "chunks" and inserts random “garbage” data at random spots, several times in a row. It keeps track of what it did and saves that info at the end of the scrambled file. When decoding, it reads that info and undoes every step, restoring your file exactly as it was.

---

## Project Structure

- `main.py` – The command-line tool and file handling
- `encoder.py` – Handles the scrambling (multi-pass encoding)
- `decoder.py` – Handles the unscrambling (multi-pass decoding)

---

## Why would I use this?

- To hide files in a silly way
- To learn about file manipulation and metadata
- To prank your friends (harmlessly!)
- For fun!

---

## What should I NOT use this for?
> [!CAUTION]
> **Do not use this for real security or encryption.**  
> It’s not cryptographically secure and is meant for fun and learning only.

> [!IMPORTANT] 
> This random tool is for educational purposes only.
> **Do NOT use this tool for ransomware, malware, or any malicious activity.**  
> Any misuse is strictly prohibited and I'll take no responsibility for unethical use.

---

Made for fun, again.