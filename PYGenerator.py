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
dir_path = "C:/Users/giuli/Documents/GitHub/Tesi" # default: os.path.dirname(os.path.realpath(__file__))
# input files folder inside master folder
input_folder = "INPUT" #should always be a folder inside the program' directory
# output files folder inside master folder
output_folder = "OUTPUT" #should always be a folder inside the program' directory
# background noise for silences and pauses
enable_noise = True
noise_file = "noise.wav" #should always be a folder inside the program' directory
# silences values
s_min = 0.05
s_max = 0.120
# pauses values
p_min = 0.7
p_max = 0.9
# channels and sample rate of the project
sample_rate = 0 # if 0, get sample_rate from the first file
channels = 0    # if 0, get channels from the first file
# sounds quantity. This float value goes from 0 to 1. If 1, uses all sounds, if 0, none
s_quantity = 0
'''
------------------------
'''
# if True, question order is random
random_question = True
# number of questions. positive or "-1" if random
n_questions = -1
# number of answers. positive or "-1" if random
n_answers = -1

def audio_file(path_file, data_file, name_file, person, duplicated: bool):
    file = {}
    file['path'] = path_file
    file['data'] = data_file
    file['name'] = name_file
    file['person'] = person
    file['duplicated'] = duplicated
    logging.info(f"audio_file \t\t - SUCCESS for: {path_file}")
    return file

def get_person(filename):
    filename_without_extension = os.path.splitext(os.path.basename(filename))[0]
    logging.info(f"get_person \t\t - SUCCESS for: {filename}")
    return filename_without_extension.split("_")[name_format['person']]

def get_gender(filename):
    filename_without_extension = os.path.splitext(os.path.basename(filename))[0]
    logging.info(f"get_gender \t\t - SUCCESS for: {filename}")
    return filename_without_extension.split("_")[name_format['gender']]

def get_type(filename):
    filename_without_extension = os.path.splitext(os.path.basename(filename))[0]
    logging.info(f"get_type \t\t - SUCCESS for: {filename}")
    return filename_without_extension.split("_")[name_format['type']]

def get_nquestion(filename):
    filename_without_extension = os.path.splitext(os.path.basename(filename))[0]
    nquestion = int(filename_without_extension.split("_")[name_format['question']])
    logging.info(f"get_type \t\t - SUCCESS for: {filename}")
    return nquestion

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
    max_participants = 0
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
                elif file_type == "S":
                    count_s.append(filename)
                max_participants += 1
    if count_q == []:
        logging.info(f"folder_info \t\t - No Initial Questions.")
        raise Exception(f"\n No questions in the folder.")
    if count_a == []:
        logging.info(f"folder_info \t\t - No Initial Questions.")
        raise Exception(f"\n No answers in the folder.")
    if count_iq == []:
        logging.info(f"folder_info \t\t - No Initial Questions.")
        raise Exception(f"\n No Initial Questions in the folder.")
    logging.info(f"folder_info \t\t - SUCCESS.")
    return max_participants, count_a, count_q, count_iq, count_s, a_letters, q_letters

def get_channels(data):
    '''Get the number of channels in an audio file'''
    if len(np.shape(data)) == 1:
        logging.info(f"get_channels \t\t - SUCCESS: {1}")
        return 1
    else:
        logging.info(f"get_channels \t\t - SUCCESS: {np.shape(data)[1]}")
        return np.shape(data)[1]

def check_SR_CH(name, rate_temp, channels_temp):
    '''handle SampleRate and Channels Exceptions'''
    '''To avoid unuseful file reads,'''
    '''this function handle only Exceptions'''
    if sample_rate != rate_temp:
        raise Exception(f"\nIl file audio n{name} ha frequenza di campionamento diversa ({rate_temp} hz).")
    elif channels != channels_temp:
        raise Exception(f"\n Il file audio n{name} ha numero di canali diverso ({channels_temp} ch).")
    else:
        logging.info(f"check_SR_CH \t\t - SUCCESS")
    
def raw_to_seconds(audio):
    '''audio data to lenght. Works with STEREO and MONO'''
    duration = len(audio) / sample_rate
    logging.info(f"raw_to_seconds \t\t - SUCCESS")
    return duration

def noise(raw_file):
    raw_noise, sample_rate = sf.read(dir_path + "/" + noise_file)
    temp_channels = get_channels(raw_noise)
    check_SR_CH(noise_file, sample_rate, temp_channels)
    raw_length = len(raw_file)
    noise_length = len(raw_noise)
    if noise_length < raw_length:
        n_repeats = int(raw_length/noise_length)+1
        raw_noise = np.concatenate([raw_noise] * n_repeats)
    sum = np.add(raw_noise[:raw_length], raw_file)
    if len(raw_noise[:raw_length]) != len(raw_file) or len(raw_file) != len(sum):
        raise Exception("Internal Error in function 'noise'")
    logging.info(f"noise \t\t\t - SUCCESS.")
    return sum
 
def concatenate(data1, data2, pause_length, channels):
    '''generate 2 audio files, one with the first audio muted,'''
    ''' the second with the second audio muted.'''
    n_sample_silence = int(sample_rate * pause_length)
    #stereo
    if len(data1.shape) > 1 or len(data2.shape) > 1:
        silence = np.zeros((n_sample_silence, channels))
        if enable_noise:
            silence = noise(silence)
        OUTPUT = np.concatenate((data1, silence, data2), axis=0)
    #mono
    else:
        silence = np.zeros((n_sample_silence,))
        if enable_noise:
            silence = noise(silence)
        OUTPUT = np.concatenate((data1, silence, data2))
    logging.info(f"concatenate \t\t - SUCCESS")
    return OUTPUT

def silence_generator(file_names):
    silences = []
    for i in range(len(file_names) - 1):
        if get_type(file_names[i]['name']) == "I":
            # if the pause is a SILENCE
            pause_length = random.uniform(s_min, s_max)
        else:
            pause_length = random.uniform(p_min, p_max)  # seconds
        silences.append(pause_length)
    logging.info(f"silence_generator \t - SUCCESS.")
    return silences

def file_complete(file_names, channels, silences):
    for j in range(len(file_names)):
        if j == 0:
            OUTPUT = file_names[0]['data']
        else:
            # aggiunge pausa e concatena elementi pieni o vuoti in base al valore di i.
            OUTPUT = concatenate(OUTPUT, file_names[j]['data'], silences[j - 1], channels)
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
                        OUTPUT = np.zeros((int(len(file_names[0]['data'])),))
                        if enable_noise:
                            OUTPUT = noise(OUTPUT)
                else:
                    # aggiunge pausa e concatena elementi pieni o vuoti in base al valore di i.
                    if file_names[j]['person'] == print_person:
                        OUTPUT = concatenate(OUTPUT, file_names[j]['data'], silences[j - 1], channels)
                    else:
                        file_silence = np.zeros((int(len(file_names[j]['data'])),))
                        if enable_noise:
                            file_silence = noise(file_silence)
                        OUTPUT = concatenate(OUTPUT, file_silence, silences[j - 1], channels)
            OUTPUT2.append([OUTPUT, print_name])
            logging.info(f"read_write_file \t - SUCCESS for: {print_name}")
    OUTPUT = file_complete(file_names, channels, silences)
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
        lengh_end = raw_to_seconds(filename) + lengh_end
        arr.append([filename["path"], filename["person"], length_start, lengh_end])
        length_start = raw_to_seconds(filename) + length_start
        if i != (len(file_names)-1):
            lengh_end, length_start = lengh_end + silences[i], length_start + silences[i]
            i += 1
    logging.info(f"filenames_lenghts \t - SUCCESS")
    return arr

def sounds_to_3dlist(sounds, max_duration):
    arr = []
    for filename in sounds:
        person = get_person(filename)
        delay = random.uniform(0, max_duration)
        arr.append([os.path.join(dir_path, input_folder+"/"+filename), person, delay])
    logging.info(f"sounds_to_3dlist \t - SUCCESS")
    return arr

def handle_sounds(sound_files, file_names, max_duration, silences):
    ''' deletes sounds in wrong position and concatenate silence with each sound '''
    logging.info(f"handle_sounds \t\t - {sound_files}")
    audio = filenames_lenghts(file_names, silences)

    sounds = sounds_to_3dlist(sound_files, max_duration)
    max_sounds = int(len(sounds) * s_quantity)
    sounds = sounds[:max_sounds]
    print(sounds)
    # this cycle only handles superposition sounds
    while True:
        popped = 0
        random.shuffle(sounds)
        for i_s in range(len(sounds)-1):
            for i_a in range(len(audio)-1):
                # if sound is inside an audio of the same person
                if audio[i_a][1] == sounds[i_s][1] and audio[i_a][2] > sounds[i_s][2] and audio[i_a][3] < sounds[i_s][2]:
                    sounds.pop(i_s)
                    popped += 1
        if float(popped) / float(max_sounds) < 0.3:
            break
        else:
            # repeat cycle only if popped sounds are less than 30% (0.3)
            logging.info(f"handle_sounds \t\t - ERROR!! - too many popped! Repeat cycle.")
            sounds = (sounds_to_3dlist(sound_files, max_duration))[:max_sounds]

    logging.info(f"handle_sounds \t\t - SUCCESS.")
    # ho in uscita un array di tutti i file audio che vanno sovrapposti con il nome di ogni persona
    return sounds

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
            sum = i[0]
            for j in sounds:
                # if the person is the same
                if i[1] == j[1]:
                    sound, temp_rate =sf.read(j[0])
                    temp_channels = get_channels(sound)
                    check_SR_CH(j[0], temp_rate, temp_channels)
                    start_sound = sample_rate*int(j[2])
                    end_sound = len(sound)+start_sound
                    if len(sound.shape) > 1 and len(sum.shape) > 1:
                        sum = np.concatenate((sum[:start_sound], sound, sum[end_sound:]), axis=0)
                    else:
                        sum = np.concatenate((sum[:start_sound], sound, sum[end_sound:]))
            output.append([sum, i[1]])
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
    global n_questions
    _, answers, questions, initial_questions, _, a_letters, q_letters = folder_info(os.path.join(dir_path, input_folder))
    logging.info(f"{answers, questions, initial_questions}")
    # create 3D array for questions
    matr_questions = list_to_3Dlist(questions)
    matr_answers = list_to_3Dlist(answers)
    matr_initquest = list_to_3Dlist(initial_questions)

    q_participants, a_participants = participants_lists(q_letters, a_letters)
    file_names = []

    # handle 1 element arrays
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
        n_questions = random.randint(1, (n_questions*(-1)))
    ran_n_que = list(range(n_questions))
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
    global n_answers, n_questions, random_question
    while True:
       tmp_n_answers = input(f"Vuoi specificare un numero massimo di persone che rispondono alla domanda (max: {count_answers})? [NO/n] ")
       if str(tmp_n_answers).lower() == "no":
           n_answers = count_answers * (-1)
           break
       elif str(tmp_n_answers).isnumeric() and int(tmp_n_answers)<=count_answers and int(tmp_n_answers)>0:
           n_answers = int(tmp_n_answers)
           break
       elif str(tmp_n_answers).isnumeric() and int(tmp_n_answers)>count_answers:
           print(f"Il numero deve essere <= {count_answers}")
       else:
           print("Il valore inserito non è corretto. Riprova.")
    while True:
       tmp_n_questions = input(f"Vuoi specificare un numero massimo di domande (max: {count_questions})? [NO/n] ")
       if str(tmp_n_questions).lower() == "no":
           n_questions = count_questions * (-1)
           break
       elif str(tmp_n_questions).isnumeric() and int(tmp_n_questions)<=count_questions and int(tmp_n_questions)>0:
           n_questions = int(tmp_n_questions)
           break
       elif str(tmp_n_questions).isnumeric() and int(tmp_n_questions)>count_questions:
           print(f"Il numero deve essere <= {count_questions}")
       else:
           print("Il valore inserito non è corretto. Riprova.")
    while True:
       tmp_random_order = input(f"L'ordine delle domande è casuale? [SI/NO] ")
       if str(tmp_random_order).lower() == "no":
           random_question = False
           break
       elif str(tmp_random_order).lower() == "si":
           random_question = True
           break
       else:
           print("Il valore inserito non è corretto. Riprova.")
    '''while True:
       participants = input(f"Hai una lunghezza massima? Se SI, quanto? ")
       if str(participants).lower() == "no":
           break
       elif str(participants).isnumeric():
           break
       else:
           print("Il valore inserito non è corretto. Riprova.")'''
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
        write_name = output_folder+f'/merged{i[1]}.wav'
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
    OUTPUT, silences = read_write_file(file_names)
    '''Create output array [data, person]: add silences/pauses to output data'''
    OUTPUT = sounds(counts_s, file_names, OUTPUT, silences)
    write_files(OUTPUT)
    print("\n COMPLETED! (folder opened)")
    os.startfile(os.path.join(dir_path, output_folder))
    '''except Exception as e:
        print(f"\n ! ERRORE: \n\tOperazione interrotta per un errore interno: {e}")
        exit()'''

# Il programma vede quali files ci sono nella cartella e chiede all'utente se vanno bene quegli interlocutori.
# chiede all'utente:
    # lunghezza massima