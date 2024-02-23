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

Users can declare various values for dialogue generation. If absent, default values are used.

[Settings](PYGenerator.cfg)


Below is an example of the configuration file code.
Comments provide explanations for each parameter.
Commands, when uncommented and marked with "Example:", represent the program's default values.

```cfg
[global]
# if True, question order is random
random_q_order = True
# number of questions. positive number, negative act as a threshold for random, 0 is just random QUANTITY
n_questions = 0
# number of answers. positive number, negative act as a threshold for random, 0 is just random
n_answers = 0
# Percentage initial question presence. 1 always, 0 never
prob_init_question = 0.5
# Percentage question presence. 1 always, 0 never
prob_question = 0.5
# probability an initial question will be followed by a new question
prob_i_q = 0.8
# volume of answers. "ND" if NOT DEFINED, "L" if LOW volume, "H" if HIGH volume
volume = ND

[files]
# file name format: *IDname_SESSO_volume_tipo_ndomanda". eg. 01_M_H_A_01 The number identifies the position
name_format = person_gender_volume_type_question
# master folder. Should NOT end with a "/"
# Example: dir_path = C:/Users/giuli/Music/Edit
# input files folder inside master folder
# Example: input_folder = INPUT
# output files folder inside master folder
# Example: output_folder = OUTPUT 
# if custom_file is not specified, it will only take as an input  ["03_M_Q_01_L.wav", "01_M_A_01_L", "03_M_Q_02_L", "01_M_A_02_L", "01_M_Q_02_L"]
custom_path = output_files.json

# silences values
[silences]
min = 0.05
max = 0.120

# long pauses (a pause between a question and another question without any initial question) values
[long pauses]
min = 0.9
max = 1.2

[pauses]
# pauses values
min = 0.7
max = 0.9

[sounds]
# This float value goes from 0 to 1. If 1, uses all sounds, if 0, none
s_quantity = 1
# minimum distance between one sound and another in seconds
min_s_distance = 5
# redundancy before and after to avoid overlap sounds in seconds
cut_redundancy = 1.5
# lenght is fixed to not cause unuseful reads in seconds, but you can specify any value if you want to
length_sounds = 2
# you can also specify how loud a sound should be if you want to
sound_amp_fact = 1
# placing gap at the end of the final file to avoid different lenghts in the final audio file in seconds
end_tollerance = 3
# how many times does the random function search for an empty space. Bigger values get better results, but a slower code
cycle_limit = 10
# background noise for silences and pauses

[fade]
# apply fade in- and fade-out to each sample. Value is in seconds
fade_length = 0

[noise]
# You can add a background noise to the audio file that will be overlaid
enable_noise = False
# Example: noise_file = noise.wav

```