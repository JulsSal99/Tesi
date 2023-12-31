import sys
sys.path.insert(0, 'libs')
import libsinstall
libsinstall.install_libraries()

import os
import soundfile as sf
import numpy as np
import random
import logging
import logger
logger.logger()

'''

Should work on both Python 3.x (tested on Python 3.11.6)

This collection is based upon the following packages (auto-installation):
  - numpy
  - pysoundfile

------------------------
YOU CAN MODIFY THESE VALUES:
'''

__version__ = "0.01"
__author__  = "G.Salada"

# file name format: *IDname_SESSO_volume_tipo_ndomanda". The number identifies the position
name_format = {"person": 0, "gender": 1, "volume": 4, "type": 2, "question": 3}
# CORRETTO name_format = {"person": 0, "gender": 1, "volume": 2, "type": 3, "question": 4}
# master folder. Should NOT end with a "/"
dir_path = "C:/Users/giuli/Music/Edit" # default: os.path.dirname(os.path.realpath(__file__))
# input files folder inside master folder
input_folder = "INPUT" #should always be a folder inside the program' directory
# output files folder inside master folder
output_folder = "OUTPUT" #should always be a folder inside the program' directory
# background noise for silences and pauses
enable_noise = True
noise_file = "noise.wav"
# silences values
s_min = 0.05
s_max = 0.120
# long pauses (a pause between a question and another question without any initial question) values
lp_min = 0.9
lp_max = 1.2
# pauses values
p_min = 0.7
p_max = 0.9
# channels and sample rate of the project
sample_rate = 0 # if 0, get sample_rate from the first file
channels = 0    # if 0, get channels from the first file
# sounds quantity. This float value goes from 0 to 1. If 1, uses all sounds, if 0, none
s_quantity = 1
# minimum distance between one sound and another
min_s_distance = 5
# decide if sounds can come from people not asking or answering questions 
'''
------------------------
'''
# if True, question order is random
random_question = True
# number of questions. positive or "-1" if random
n_questions = -1
# number of answers. positive or "-1" if random
n_answers = -1
# enable initial questions. "-1" if random, "0" if disabled, "1" if enabled
enable_init_question = -1
# volume of answers. "ND" if NOT DEFINED, "H" if LOW volume, "L" if HIGH volume
volume = "ND"

pop_tollerance = sample_rate * 1

def audio_file(path: str, data: bin, name: str, person: str, duplicated: bool):
    file = {}
    file['path'] = path
    file['data'] = data
    file['name'] = name
    file['person'] = person
    file['duplicated'] = duplicated
    logging.info(f"audio_file \t\t - SUCCESS for: {path}: {type(file)}")
    return file

def get_person(filename: str):
    filename_without_extension = os.path.splitext(os.path.basename(filename))[0]
    logging.info(f"get_person \t\t - SUCCESS for: {filename}")
    return filename_without_extension.split("_")[name_format['person']]

def get_gender(filename: str):
    filename_without_extension = os.path.splitext(os.path.basename(filename))[0]
    logging.info(f"get_gender \t\t - SUCCESS for: {filename}")
    return filename_without_extension.split("_")[name_format['gender']]

def get_type(filename: str):
    filename_without_extension = os.path.splitext(os.path.basename(filename))[0]
    logging.info(f"get_type \t\t - SUCCESS for: {filename}")
    return filename_without_extension.split("_")[name_format['type']]

def get_nquestion(filename: str):
    filename_without_extension = os.path.splitext(os.path.basename(filename))[0]
    nquestion = int(filename_without_extension.split("_")[name_format['question']])
    logging.info(f"get_type \t\t - SUCCESS for: {filename}")
    return nquestion

def get_volume(filename: str):
    filename_without_extension = os.path.splitext(os.path.basename(filename))[0]
    logging.info(f"get_volume \t\t - SUCCESS for: {filename}")
    return filename_without_extension.split("_")[name_format['volume']]

def get_channels(data):
    '''Get the number of channels in an audio file'''
    if len(np.shape(data)) == 1:
        logging.info(f"get_channels \t\t - SUCCESS: {1}")
        return 1
    else:
        logging.info(f"get_channels \t\t - SUCCESS: {np.shape(data)[1]}")
        return np.shape(data)[1]

def add_file(file_names, file):
    '''add file to file_names array and use audio_file() function'''
    person = get_person(file)
    duplicated = False
    if person in [file_names[i]['person'] for i in range(len(file_names))]:
        duplicated = True
    file_names.append(audio_file(file, 0, os.path.splitext(os.path.basename(file))[0], person, duplicated))
    logging.info(f"add_file \t\t - SUCCESS for: {file}")
    return file_names

def find_file(name, path):
    '''Search for the file by its name with and without the extension'''
    '''and return the first file found with the exact path of the file.'''
    for root, dirs, files in os.walk(path):
        for file in files:
            if name in file and (file.lower().endswith(".wav")):
                logging.info(f"find_file \t\t - SUCCESS.")
                return os.path.join(root, file)
    raise Exception(f"File {name}.wav not found in {path}")

def folder_info(folder_path):
    '''count the number of audio files in a folder and split questions from answers'''
    max_files = 0
    count_q = [] #array with all questions
    count_a = [] #array with all answers
    count_iq = [] #array with all initial answer
    count_s = [] #array with all sounds
    q_letters = {} #count questions persons
    a_letters = {} #count answers persons
    for filename in os.listdir(folder_path):
        if filename.endswith('.wav'):
            if len(filename.split('_')) > len(name_format):
                logging.info(f"folder_info \t\t - ABORT: {filename} name format is NOT correct. See manual for correct file naming.\n")
            else: 
                file_type = get_type(filename)
                if file_type == "S":
                    count_s.append(filename)
                elif volume == "ND" or get_volume(filename) == volume:
                    if file_type == "Q":
                        count_q.append(filename)
                        person = get_person(filename)
                        q_letters[person] = get_nquestion(filename)
                    elif file_type == "A":
                        count_a.append(filename)
                        person = get_person(filename)
                        a_letters[person] = get_nquestion(filename)
                    elif file_type == "I":
                        count_iq.append(filename)
                max_files += 1
    if count_q == []:
        logging.info(f"folder_info \t\t - No Initial Questions.")
        raise Exception(f"\n No questions in the folder.")
    if count_a == []:
        logging.info(f"folder_info \t\t - No Initial Questions.")
        raise Exception(f"\n No answers in the folder.")
    if count_iq == []:
        logging.info(f"folder_info \t\t - No Initial Questions.")
        raise Exception(f"\n No Initial Questions in the folder.")
    logging.info(f"folder_info \t\t - SUCCESS: max_files: {max_files}, \tcount_a: {count_a}, \tcount_q: {count_q}, \tcount_iq: {count_iq}, \tcount_s: {count_s}, \ta_letters: {a_letters}, \tq_letters: {q_letters}")
    return max_files, count_a, count_q, count_iq, count_s, a_letters, q_letters

def check_SR_CH(name, rate_temp, channels_temp):
    '''handle SampleRate and Channels Exceptions'''
    '''To avoid unuseful file reads,'''
    '''this function handle only Exceptions'''
    if sample_rate != rate_temp:
        raise Exception(f"\nIl file audio n{name} ha frequenza di campionamento diversa ({rate_temp} hz).")
    elif channels != channels_temp:
        raise Exception(f"\n Il file audio n{name} ha numero di canali diverso ({channels_temp} ch).")
    else:
        logging.info(f"check_SR_CH \t\t - SUCCESS for {name}")

def ceil(value) -> int:
    if isinstance(value, int):
        integer = int(value)
    elif isinstance(value, float):
        integer, decimal = str(value).split(".")
        if int(decimal) != "0":
            integer = int(integer) + 1
    return integer

def raw_to_seconds(audio):
    '''audio data to lenght. Works with STEREO and MONO'''
    duration = len(audio) / sample_rate
    logging.info(f"raw_to_seconds \t\t - SUCCESS")
    return duration

def shape_fixer(mono_array, shape):
    if shape > 1:
        stereo_array = np.empty((mono_array.shape[0], channels), dtype=mono_array.dtype)
        for i in range(channels):
            stereo_array[:, i] = mono_array
    else:
        stereo_array = mono_array.reshape(-1)
    return stereo_array

# /////////////////////////////////// NOISE //////////////////////////////////

def noise(raw_file):
    raw_noise, sample_rate = sf.read(dir_path + "/" + noise_file)
    temp_channels = get_channels(raw_noise)
    check_SR_CH(noise_file, sample_rate, temp_channels)
    raw_length = len(raw_file)
    noise_length = len(raw_noise)
    if noise_length < raw_length:
        n_repeats = int(raw_length/noise_length)+1
        tmp_noise = raw_noise
        for _ in range(n_repeats):
            raw_noise = concatenate_noise(raw_noise, tmp_noise, len(raw_noise.shape))
    sum = np.add(raw_noise[:raw_length], raw_file)
    if len(raw_noise[:raw_length]) != len(raw_file) or len(raw_file) != len(sum):
        raise Exception("INTERNAL ERROR: function 'noise'")
    logging.info(f"noise \t\t\t - SUCCESS.")
    return sum

def concatenate_noise(audio1, audio2, shape):
    '''Concatenate two audio files using a noise as a bandade (two fade-in, fade-out)'''
    len_fade = 0.05 #in seconds, if noise is <, value is half noise
    len_fade = int(len_fade * sample_rate)
    noise = sf.read(dir_path + "/" + noise_file)[0]
    if len(noise) < (len_fade * 2):
        len_fade = int(len(noise) / 2)
        logging.info(f"concatenate_noise \t\t - NOTE: len_fade = {len_fade}")
    if len(audio1) == 0:
        logging.info(f"concatenate_noise \t\t - WARNING: audio1 is empty")
        return audio2
    elif len(audio2) == 0:
        logging.info(f"concatenate_noise \t\t - WARNING: audio2 is empty")
        return audio1
    elif len(audio1) < (len_fade):
        raise Exception(f"audio1 ({len(audio1)} samples) smaller than fade ({len_fade} samples)!!")
    elif len(audio2) < (len_fade):
        raise Exception(f"audio2 ({len(audio2)} samples) smaller than fade ({len_fade} samples)!!")
    # applica il fade-out al primo file audio
    fade_out = np.logspace(np.log10(0.15), np.log10(1.05), len_fade)
    #fade_out = np.linspace(0.15, 1.05, len_fade)
    fade_out = shape_fixer(np.subtract(1.1, fade_out), shape)
    fade_in = np.flip(fade_out)
    FO_audio1 = audio1[-len_fade:] * fade_out
    FI_audio2 = audio2[:len_fade] *fade_in
    noise = noise[:(len_fade*2)]
    FI_rumore = noise[:len_fade]*fade_in
    FO_rumore = noise[-len_fade:]*fade_out
    # Unisci i file audio
    mixed_audio1 = np.add(FO_audio1, FI_rumore)
    mixed_audio2 = np.add(FI_audio2, FO_rumore)
    audio1[-len_fade:] = mixed_audio1
    audio2[:len_fade] = mixed_audio2
    #concatena i files audio
    if channels > 1:
        OUTPUT = np.concatenate((audio1, audio2), axis=0)
    else:
        OUTPUT = np.concatenate((audio1, audio2))
    if len(audio1) + len(audio2) != len(OUTPUT):
        raise Exception("INTERNAL ERROR: concatenate_noise function")
    logging.info(f"concatenate_noise \t - SUCCESS")
    return OUTPUT

# /////////////////////////////////////////////////////////////////////////////

def concatenate(data1, data2, pause_length):
    '''generate 2 audio files, one with the first audio muted,'''
    ''' the second with the second audio muted.'''
    n_sample_silence = int(sample_rate * pause_length)
    shape = len(data1.shape)

    if shape > 1: #stereo
        silence = np.zeros((n_sample_silence, channels))
    else: #mono
        silence = np.zeros((n_sample_silence,))
    if enable_noise:
        silence = noise(silence)
        OUTPUT = concatenate_noise(data1, silence, shape)
        OUTPUT = concatenate_noise(OUTPUT, data2, shape)
    elif shape > 1: #stereo
        OUTPUT = np.concatenate((data1, silence, data2), axis=0)
    else: #mono
        OUTPUT = np.concatenate((data1, silence, data2))
    logging.info(f"concatenate \t\t - SUCCESS")
    return OUTPUT

def silence_generator(file_names):
    '''Generate long pause, short pause or silence in seconds'''
    silences = []
    length = len(file_names) - 1
    for i in range(length):
        if get_type(file_names[i]['name']) == "I":
            # if the pause is a SILENCE
            pause_length = random.uniform(s_min, s_max)
        elif get_type(file_names[i]['name']) == "A" and i != length:
            if get_nquestion(file_names[i]['name']) and get_nquestion(file_names[i+1]['name']):
                pause_length = random.uniform(lp_min, lp_max)  # seconds
            else:
                pause_length = random.uniform(p_min, p_max)  # seconds
        else:
            pause_length = random.uniform(p_min, p_max)  # seconds
        silences.append(pause_length)
    logging.info(f"silence_generator \t - SUCCESS.")
    return silences

def file_complete(file_names, silences):
    for j in range(len(file_names)):
        if j == 0:
            OUTPUT = file_names[0]['data']
        else:
            # aggiunge pausa e concatena elementi pieni o vuoti in base al valore di i.
            OUTPUT = concatenate(OUTPUT, file_names[j]['data'], silences[j - 1])
    logging.info(f"file_complete \t\t - SUCCESS.")
    return OUTPUT

def data_creator(file_names):
    '''Read each single file and add raw data to file_names'''
    '''and check sample rate and channels with check_SR_CH'''
    global channels, sample_rate
    if channels == 0 or sample_rate == 0:
        # Get sample rate
        data_temp, temp_rate = sf.read(file_names[0]['path'])
        # Get channels number
        channels += get_channels(data_temp)
        sample_rate += temp_rate

    for i in range(len(file_names)):
        file_names[i]['data'], rate_temp = sf.read(file_names[i]['path'])
        channels_temp = get_channels(file_names[i]['data'])
        check_SR_CH(file_names[i]['name'], rate_temp, channels_temp)
    logging.info(f"data_creator \t\t - SUCCESS.")

def read_write_file(file_names):
    ''' MAIN FUNCTION: create the ending file'''
    ''' create the class inside file_names and return to concatenate()'''
    ''' check channels, sample_rate'''

    # Get sampled data from files and check sample rate and channels
    data_creator(file_names)
    
    # create an array of pause_length for each (between) file
    silences = silence_generator(file_names)
    
    OUTPUT2 = []
    # i è l'elemento da stampare con i dati, mentre j è l'elemento attuale
    for i in range(len(file_names)):
        print_person = file_names[i]['person']
        if not file_names[i]['duplicated']:
            print_name = file_names[i]['person']
            for j in range(len(file_names)):
                if j == 0:
                    # gestisce il primo elemento e lo mette vuoto se non è lui
                    if file_names[j]['person'] == print_person:
                        OUTPUT = file_names[0]['data']
                    else:
                        if channels > 1:
                            OUTPUT = np.zeros((int(len(file_names[0]['data'])), channels))
                        else:
                            OUTPUT = np.zeros((int(len(file_names[0]['data'])),))
                        if enable_noise:
                            OUTPUT = noise(OUTPUT)
                else:
                    # aggiunge pausa e concatena elementi pieni o vuoti in base al valore di i.
                    if file_names[j]['person'] == print_person:
                        OUTPUT = concatenate(OUTPUT, file_names[j]['data'], silences[j - 1])
                    else:
                        if channels > 1:
                            file_silence = np.zeros((int(len(file_names[j]['data'])), channels))
                        else:
                            file_silence = np.zeros((int(len(file_names[j]['data'])),))
                        if enable_noise:
                            file_silence = noise(file_silence)
                        OUTPUT = concatenate(OUTPUT, file_silence, silences[j - 1])
            OUTPUT2.append([OUTPUT, print_name])
            logging.info(f"read_write_file \t - SUCCESS for: {print_name}")
    OUTPUT = file_complete(file_names, silences)
    OUTPUT2.append([OUTPUT, "COMPLETE"])
    return OUTPUT2, silences


# /////////////////////////////////// SOUNDS //////////////////////////////////

def filenames_lenghts(file_names, silences):
    '''Create array for each output file with path, person, start and end'''
    '''also handle silences'''
    arr = []
    lengh_end, length_start = 0, 0
    i = 0
    for filename in file_names:
        len_file = raw_to_seconds(filename["data"])
        lengh_end = len_file + lengh_end
        arr.append([filename["path"], filename["person"], length_start, lengh_end])
        length_start = lengh_end
        if i != (len(file_names)-1):
            length_start = length_start + silences[i]
            lengh_end = lengh_end + silences[i]
            i += 1
    logging.info(f"filenames_lenghts \t - SUCCESS: {arr}")
    return arr

def handle_sounds(sound_files, file_names, max_duration, silences):
    '''create 2D list of sounds. Each sound has a random position in seconds'''
    '''There are various values to setup the randomness'''
    cut_redundancy = 1.5  # in seconds
    length_sounds = 2 # lenght is fixed to not cause unuseful reads
    end_tollerance = 3 # in seconds, gap at the end to avoid different lenghts in the final audio file
    cycle_limit = 10 # how many times does the random function search for an empty space. Bigger values get better results, but a slower code
    OUTPUT = []
    tmp_arr = []
    count_sounds = 0
    audio = filenames_lenghts(file_names, silences)
    for _ in range(ceil(s_quantity)):
        random.shuffle(sound_files)
        for filename in sound_files:
            count_sounds += 1
            tmp_limit = 0
            person = get_person(filename)
            while True:
                correct = True
                delay = random.uniform(0, max_duration-end_tollerance)
                if tmp_limit <= cycle_limit:
                    for i in tmp_arr:
                        if abs(i-delay) < min_s_distance:
                            correct = False
                            tmp_limit += 1
                            break
                        # WHAT-IF: The sound is near the same sound?
                    if correct != False:
                        for i_a in range(len(audio)):
                            start_NO_zone = audio[i_a][2]-cut_redundancy-length_sounds
                            start_NO_zone2 = audio[i_a][2]-cut_redundancy
                            end_NO_zone = audio[i_a][3]+cut_redundancy
                            # REMOVE if sound is inside an audio of the same person
                            if audio[i_a][1] == person and delay > (start_NO_zone) and delay < (end_NO_zone):
                                correct = False
                                tmp_limit += 1
                                break
                            # REMOVE if sound is near the start of any sound
                            elif delay > (start_NO_zone2) and delay < (end_NO_zone):
                                correct = False
                                tmp_limit += 1
                                break
                else:
                    logging.info(f"handle_sounds \t\t - WARNING: no more space for new sounds with cycle repeated {tmp_limit}")
                    return OUTPUT
                if correct:
                    tmp_arr.append(delay)
                    OUTPUT.append([os.path.join(dir_path, input_folder+"/"+filename), person, delay])
                    logging.info(f"handle_sounds \t\t - NOTE: appended {filename} on position {delay} with cycle repeated {tmp_limit}")
                    tmp_limit = 0
                    break
        logging.info(f"handle_sounds \t\t - NOTE: arr expanded with {count_sounds} sounds")
    logging.info(f"handle_sounds \t\t - SUCCESS")
    # ho in uscita un array di tutti i file audio che vanno sovrapposti con il nome di ogni persona
    return OUTPUT

def sounds(sound_files, file_names, audio_no_s, silences):
    output = []
    if s_quantity == 0:
        logging.info(f"sounds \t\t\t - ABORT: s_quantity = 0")
        for i in audio_no_s:
            output.append([i[0], i[1]])
    else:
        # -1 takes the last file (COMPLETE)
        max_duration = raw_to_seconds(audio_no_s[-1][0])
        sounds = handle_sounds(sound_files, file_names, max_duration, silences)
        for i in audio_no_s:
            if i[1] != "COMPLETE":
                sum = i[0]
                for j in sounds:
                    # if the person is the same
                    if i[1] == j[1]:
                        sound =sf.read(j[0])[0]
                        start_sound = sample_rate*int(j[2])
                        end_sound = len(sound)+start_sound
                        shape = len(sum.shape)
                        if enable_noise:
                            sum_tmp = concatenate_noise(sum[:start_sound], sound, shape)
                            sum = concatenate_noise(sum_tmp, sum[end_sound:], shape)
                        #else:
                        #    sum[start_sound:end_sound] += sound
                        elif channels > 1:
                            sum = np.concatenate((sum[:start_sound-1], sound, sum[end_sound-1:]), axis=0)
                        else:
                            sum = np.concatenate((sum[:start_sound-1], sound, sum[end_sound-1:]))
                limit = ceil(max_duration*sample_rate)
                if len(sum) > limit or len(sum) < limit-2:
                    raise Exception (f"INTERNAL ERROR: {i[1]} (with lenght: {len(sum)}) does not match {ceil(max_duration*sample_rate)} length")
                output.append([sum, i[1]])
            elif i[1] == "COMPLETE":
                for j in output:
                    if j[1] != "COMPLETE":
                        if 'summed_data' not in locals():
                            summed_data = j[0]
                        else:
                            summed_data = np.add(summed_data, j[0])
                output.append([summed_data, "COMPLETE"])
            logging.info(f"sounds \t\t\t - SUCCESS for: {i[1]}")
    return output

# /////////////////////////////////// SOUNDS //////////////////////////////////

def participants_lists(q_letters, a_letters):
    q_participants = list(q_letters.keys())
    a_participants = list(a_letters.keys())
    logging.info(f"participants_lists \t - SUCCESS")
    return q_participants, a_participants

def list_to_3Dlist(dict):
    # create 3D list for dicts
    arr = []
    for filename in dict:
        person = get_person(filename)
        n_question = get_nquestion(filename)
        arr.append([os.path.join(dir_path, input_folder+"/"+filename), person, n_question])
    logging.info(f"list_to_3Dlist \t\t - SUCCESS")
    return arr

def handle_auto_files(dir_path):
    '''CREATE FILE_NAMES'''
    _, answers, questions, initial_questions, _, a_letters, q_letters = folder_info(os.path.join(dir_path, input_folder))
    logging.info(f"{answers, questions, initial_questions}")
    # create 3D array for questions
    matr_questions = list_to_3Dlist(questions)
    matr_answers = list_to_3Dlist(answers)
    matr_initquest = list_to_3Dlist(initial_questions)

    q_participants, a_participants = participants_lists(q_letters, a_letters)
    file_names = []

    # handle 1 element arrays
    if len(a_participants) == len(q_participants) == 1 and a_participants[0] == q_participants[0]:
        raise Exception("More than 1 participant are required for the experiment!!")
    if len(a_participants) == 1:
        answerer = a_participants[0]
        # first interrogator must be != answerer
        if answerer in q_participants:
            q_participants.remove(answerer)
    if len(q_participants) == 1:
        interrogator = q_participants[0]
        # first answerer must be != interrogator
        if interrogator in a_participants:
            a_participants.remove(interrogator)

    tmp_n_answers = 0
    if n_questions < 0:
        tmp_n_questions = random.randint(1, (n_questions*(-1)))
    else:
        tmp_n_questions = n_questions
    ran_n_que = list(range(tmp_n_questions))
    # shuffle if question order should be randomized
    if random_question:
        random.shuffle(ran_n_que)
    for j in ran_n_que:
        # choose random interrogator
        interrogator = random.choice(q_participants)
        # add first person to ask X each question
        for i in matr_questions:
            if str(interrogator) == str(i[1]) and int(j+1) == int(i[2]):
                file_names = add_file(file_names, i[0])
                break
        
        # handle number of answers also if negative 
        if n_answers < 0:
            tmp_n_answers = random.randint(1, (n_answers*(-1)))
        else:
            tmp_n_answers = n_answers
        # shuffle answerers 
        while True:
            random.shuffle(a_participants)
            if a_participants[0] != interrogator:
                break

        # add first person to answer X each question
        for i_a in range(tmp_n_answers):
            if i_a != 0:
                for i in matr_initquest:
                    if str(responder) == str(i[1]) and int(j+1) == int(i[2]):
                        file_names = add_file(file_names, i[0])
                        break
                if (enable_init_question == 1) or (enable_init_question == -1 and bool(random.getrandbits(1)) == True):
                    for i in matr_questions:
                        if str(responder) == str(i[1]) and int(j+1) == int(i[2]):
                            file_names = add_file(file_names, i[0])
                            break
            responder = a_participants[i_a]
            i_a += 1
            for i in matr_answers:
                if str(responder) == str(i[1]) and int(j+1) == int(i[2]):
                    file_names = add_file(file_names, i[0])
                    break
    logging.info(f"handle_auto_files \t - SUCCESS: {file_names}")
    return file_names


def user_auto_files(count_answers, count_questions):
    global n_answers, n_questions, random_question, volume
    while True:
       tmp_input = input(f"Vuoi specificare un numero massimo di persone che rispondono alla domanda (max: {count_answers})? [NO/n] ")
       if str(tmp_input).lower() == "no":
           n_answers = count_answers * (-1)
           break
       elif str(tmp_input).isnumeric() and int(tmp_input)<=count_answers and int(tmp_input)>0:
           n_answers = int(tmp_input)
           break
       elif str(tmp_input).isnumeric() and int(tmp_input)>count_answers:
           print(f"Il numero deve essere <= {count_answers}")
       else:
           print("Il valore inserito non è corretto. Riprova.")
    while True:
       tmp_input = input(f"Vuoi specificare un numero massimo di domande (max: {count_questions})? [NO/n] ")
       if str(tmp_input).lower() == "no":
           n_questions = count_questions * (-1)
           break
       elif str(tmp_input).isnumeric() and int(tmp_input)<=count_questions and int(tmp_input)>0:
           n_questions = int(tmp_input)
           break
       elif str(tmp_input).isnumeric() and int(tmp_input)>count_questions:
           print(f"Il numero deve essere <= {count_questions}")
       else:
           print("Il valore inserito non è corretto. Riprova.")
    while True:
       tmp_input = input(f"L'ordine delle domande è casuale? [SI/NO] ")
       if str(tmp_input).lower() == "no":
           random_question = False
           break
       elif str(tmp_input).lower() == "si":
           random_question = True
           break
       else:
           print("Il valore inserito non è corretto. Riprova.")
    while True:
       tmp_input = input(f"Portamento? [HIGH/LOW/MIX] ")
       if str(tmp_input).lower() == "high":
           volume = "H"
           break
       elif str(tmp_input).lower() == "low":
           volume = "L"
           break
       elif str(tmp_input).lower() == "mix":
           volume = "ND"
           break
       else:
           print("Il valore inserito non è corretto. Riprova.")
    logging.info(f"user_auto_files \t - SUCCESS")

def user_ask_files(dir_path, max_participants):
    '''Ask file1, file2'''
    ''' and check/fix paths (file1, file2)'''
    ''' handle the errors'''
    file_names = []
    for i in range(max_participants):
        while True:
            try:
                file = input(f"Inserisci il nome del {i + 1}o audio (scrivi FINE per terminare, max {max_participants - i}): ")
                if file == "FINE" and i > 1:
                    return file_names
                elif file == "FINE" and i <= 1:
                    raise Exception("Non abbastanza files!!!")
                file = find_file(file, os.path.join(dir_path, input_folder))
                file_names = add_file(file, file_names) 
                print(f'\tAggiunto "{file}" con successo.')
                break
            except EOFError:
                print("\n\tProgramma terminato senza successo. Chiusura del programma.")
                exit()
            except Exception as e:
                print(f"\tERRORE: {e}")
    logging.info(f"user_ask_files \t - SUCCESS: {file_names}")

def user_input(dir_path, max_participants, a_letters, q_letters):
    if len(q_letters) == 1 and len(a_letters) == 1 and q_letters.keys() == a_letters.keys():
        raise Exception("Only one participant!!!")
    '''ask if wants each file or auto-mode'''
    while True:
        user_choice = input(f"Vuoi inserire manualmente i files? [SI/NO] ")
        if str(user_choice).lower() == "si":
            file_names = user_ask_files(dir_path, max_participants)
            logging.info(f"user_input \t\t - SUCCESS: {file_names}")
            return file_names
        elif str(user_choice).lower() == "no":
            min_max = min(max(q_letters.values()), max(a_letters.values()))
            user_auto_files(len(a_letters), int(min_max))
            file_names = handle_auto_files(dir_path)
            logging.info(f"user_input \t\t - SUCCESS: {file_names}")
            return file_names
        else:
            print("Il valore inserito non è corretto. Riprova.")

def write_files(OUTPUT):
    for i in OUTPUT:
        write_name = os.path.join(dir_path, output_folder+f'/merged{i[1]}.wav')
        sf.write(write_name, i[0], sample_rate)
        logging.info(f"write_files \t\t - SUCCESS: Created {write_name}")

if __name__ == '__main__':
    '''Important path of input files'''
    max_participants, count_a, count_q, count_iq, counts_s, a_letters, q_letters = folder_info(os.path.join(dir_path, input_folder))

    print("\n\tGeneratore di dialoghi realistici.\n")
    
    #try:
    '''ask for user input'''
    file_names = user_input(dir_path, max_participants, a_letters, q_letters)
    '''Create output array [data, person] and silences/pauses values'''
    print("\t chosing new files and pauses...")
    OUTPUT, silences = read_write_file(file_names)
    '''Create output array [data, person]: add silences/pauses to output data'''
    print("\t adding new sounds...")
    OUTPUT = sounds(counts_s, file_names, OUTPUT, silences)
    print("\t writing files into the hard drive...")
    write_files(OUTPUT)
    print("\n COMPLETED! (folder opened)")
    os.startfile(os.path.join(dir_path, output_folder))
    '''except Exception as e:
        print(f"\n ! ERRORE: \n\tOperazione interrotta per un errore interno: {e}")
        exit()'''

# Il programma vede quali files ci sono nella cartella e chiede all'utente se vanno bene quegli interlocutori.
# chiede all'utente:
    # lunghezza massima