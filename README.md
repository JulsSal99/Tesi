# Procedural Dialogue Generation

This is a thesis project carried out at the **Laboratory of Musical Informatics (LIM)**. The purpose of the thesis is to create an audio dataset from various participants in a soundproof room and then have these individual dialogues interact to construct a discourse involving multiple people. 

## Documentation
[Document](TESI.MD)

[Test Protocol](PROTOCOLLO.MD)

## The Program

In the following repository, you'll find a program for procedural dialogue generation. The program takes a series of input files and concatenates them. The user can then decide various parameters such as the presence of burst, the number of questions, which values should be random, etc.

[Python Pseudo-Realistic Dialogue Generator](PYGenerator.py)

The **input file** types include:
- Question (e.g., "How was your day?")
- Response (e.g., "Not much, it was okay.")
- Prompt (e.g., "And you?")
- Burst (e.g., cough)

The **output file** types are:
- Individual audio files for each speaker
- A combined file summarizing the previous tracks

## Settings

Users can declare various values for dialogue generation. The settings file contains comments for each user-declarable value. If absent, default values are used.

[Settings](PYGenerator.cfg)