# Procedural Dialogue Generation

## Documentation
[Document](TESI.MD)

[Test Protocol](PROTOCOLLO.MD)

## The Program

In the following repository, you'll find a program for procedural dialogue generation. The program takes a series of input files and concatenates them.

[Python Pseudo-Realistic Dialogue Generator](PYGenerator.py)

The input file types include:
- Question (e.g., "How was your day?")
- Response (e.g., "Not much, it was okay.")
- Prompt (e.g., "And you?")
- Burst (e.g., cough)

The output file types are:
- Individual audio files for each speaker
- A combined file summarizing the previous tracks

## Settings

Users can declare various values for dialogue generation. The settings file contains comments for each user-declarable value. If absent, default values are used.

[Settings](PYGenerator.cfg)
