import libsinstall
libsinstall.install_libraries()

import os
import soundfile as sf
import numpy as np
import random

'''

Should work on both Python 3.x (tested on Python 3.11.6)
Look at the test() function for some examples...

This collection is based upon the following packages (auto-installation):
  - numpy
  - pysoundfile

'''

__version__ = "0.01"
__author__  = "G.Salada"

'''
------------------------
'''

def audioread(filename, frames=-1, start=0, fill_val=None):
    '''Returns audio data in range -1:1 together with sample rate'''
    '''Additional params: start, frames, fill_value'''
    input = "input/"
    #AGGIUSTA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #AGGIUSTA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #AGGIUSTA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #AGGIUSTA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #AGGIUSTA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    data, Fs = sf.read(input+filename, frames, start, fill_value=fill_val)
    return data, Fs

def audio_file(path_file, data_file, name_file, person_file, duplicated: bool):
    file = {}
    file['path'] = path_file
    file['data'] = data_file
    file['name'] = name_file
    file['person'] = person_file
    file['duplicated'] = duplicated
    return file

def add_file(file_names, file):
    '''add file to file_names array and use audio_file() function'''
    filename_without_extension = os.path.splitext(os.path.basename(file))[0]
    person = filename_without_extension.split("_")[1]
    duplicated = False
    if person in [file_names[i]['person'] for i in range(len(file_names))]:
        duplicated = True
    file_names.append(audio_file(file, 0, filename_without_extension, person, duplicated))
    return file_names

def find_file(name, path):
    '''Search for the file by its name with and without the extension'''
    '''and return the first file found with the exact path of the file.'''
    for root, dirs, files in os.walk(path):
        for file in files:
            if name in file and (file.lower().endswith(".wav")):
                return os.path.join(root, file)
    raise Exception(f"File {name}.wav not found in {path}")

def folder_info(folder_path):
    '''count the number of audio files in a folder and split questions from answers'''
    count_wrong_name = 0
    max_files = 0
    count_q = [] #questions
    count_a = [] #answers
    count_iq = [] #initial answer
    q_letters = {} #questions persons
    a_letters = {} #answers persons
    iq_letters = {} #initial questions persons
    for filename in os.listdir(folder_path):
        if filename.endswith('.wav'):
            if len(filename.split('_')) < 3:
                count_wrong_name += 1
            else:
                if filename.startswith('Q'):
                    count_q.append(filename)
                    filename = os.path.splitext(os.path.basename(filename))[0]
                    second_value = filename.split('_')[1]
                    q_letters[second_value] = (filename.split('_')[2])
                elif filename.startswith('A'):
                    count_a.append(filename)
                    filename = os.path.splitext(os.path.basename(filename))[0]
                    second_value = filename.split('_')[1]
                    a_letters[second_value] = (filename.split('_')[2])
                elif filename.startswith('IQ'):
                    count_iq.append(filename)
                    filename = os.path.splitext(os.path.basename(filename))[0]
                    second_value = filename.split('_')[1]
                    iq_letters[second_value] = (filename.split('_')[2])           
                max_files += 1
    return count_wrong_name, max_files, count_a, count_q, count_iq, a_letters, q_letters, iq_letters

def get_channels(data):
    '''Get the number of channels in an audio file'''
    if len(np.shape(data)) == 1:
        return 1
    else:
        return np.shape(data)[1]

def concatenate(data1, data2, pause_length, sample_rate, channels):
    '''generate 2 audio files, one with the first audio muted,'''
    ''' the second with the second audio muted.'''
    n_sample_silence = int(sample_rate * pause_length)
    #stereo
    if len(data1.shape) > 1 or len(data2.shape) > 1:
        silence = np.zeros((n_sample_silence, channels))
        OUTPUT = np.concatenate((data1, silence, data2), axis=0)
    #mono
    else:
        silence = np.zeros((n_sample_silence,))
        OUTPUT = np.concatenate((data1, silence, data2))
    return OUTPUT

def check_SR_CH(file_names, sample_rate, channels):
    '''Check sample rate and channels of the audio files'''
    for i in range(len(file_names)):
        file_names[i]['data'], sample_rate_temp = audioread(file_names[i]['path'])
        channels_temp = get_channels(file_names[i]['data'])
        if i == 0:
            sample_rate = sample_rate_temp
        elif sample_rate != sample_rate_temp:
            raise Exception(f"\nIl file audio n{i+1} ha frequenza di campionamento diversa ({sample_rate_temp} hz).")
        elif channels != channels_temp:
            raise Exception(f"\n Il file audio n{i+1} ha numero di canali diverso ({channels_temp} ch).")

def read_write_complete(file_names, sample_rate, channels, silences):
    for j in range(len(file_names)):
        if j == 0:
            OUTPUT = file_names[0]['data']
        else:
            # aggiunge pausa e concatena elementi pieni o vuoti in base al valore di i.
            OUTPUT = concatenate(OUTPUT, file_names[j]['data'], silences[j - 1], sample_rate, channels)
    sf.write(f'OUTPUT/mergedCOMPLETE.wav', OUTPUT, sample_rate)

def read_write_file(file_names):
    ''' MAIN FUNCTION: create the ending file'''
    ''' create the class inside file_names and return to concatenate()'''
    ''' check channels, sample_rate'''
    # Get sample rate
    data_temp, sample_rate = audioread(file_names[0]['path'])
    # Get channels number
    channels = get_channels(data_temp)
    
    # Get sampled data from files and check sample rate and channels
    _, sample_rate = audioread(file_names[0]['path'])
    check_SR_CH(file_names, sample_rate, channels)
    
    # create an array of pause_length for each (between) file
    silences = []
    for i in range(len(file_names) - 1):
        pause_length = random.uniform(0.7, 0.9)  # seconds
        silences.append(pause_length)
    
    # i è l'elemento da stampare con i dati, mentre j è l'elemento attuale
    for i in range(len(file_names)):
        print_person = file_names[i]['person']
        if not file_names[i]['duplicated']:
            print_name = file_names[i]['name']
            for j in range(len(file_names)):
                if j == 0:
                    # gestisce il primo elemento e lo mette vuoto se non è lui
                    if file_names[j]['person'] == print_person:
                        OUTPUT = file_names[0]['data']
                    else:
                        OUTPUT = np.zeros((int(len(file_names[0]['data'])),))
                else:
                    # aggiunge pausa e concatena elementi pieni o vuoti in base al valore di i.
                    if file_names[j]['person'] == print_person:
                        OUTPUT = concatenate(OUTPUT, file_names[j]['data'], silences[j - 1], sample_rate, channels)
                    else:
                        file_silence = np.zeros((int(len(file_names[j]['data'])),))
                        OUTPUT = concatenate(OUTPUT, file_silence, silences[j - 1], sample_rate, channels)
            sf.write(f'OUTPUT/merged{i}{print_name}.wav', OUTPUT, sample_rate)
    
    read_write_complete(file_names, sample_rate, channels, silences)

def participants_lists(q_letters, a_letters):
    q_participants = list(q_letters.keys())
    a_participants = list(a_letters.keys())
    # Unisci i due dizionari
    #q_letters.update(a_letters)
    # Elimina i duplicati dalle chiavi e trasformale in lista
    #unique_keys = list(set(q_letters.keys()))
    return q_participants, a_participants

def calculator_NO_ask_files(dir_path, n_answers, n_questions):
    _, _, answers, questions, initial_questions, a_letters, q_letters, _ = folder_info(os.path.join(dir_path, "INPUT"))
    #q_participants, a_participants = random_choice(q_letters, a_letters, n_answers)
    # create 3D array for questions
    matr_questions = []
    for filename in questions:
        filename_noext = os.path.splitext(os.path.basename(filename))[0]
        matr_questions.append([filename, filename_noext.split('_')[1], int(filename_noext.split('_')[2])])

    # create 3D array for answers
    matr_answers = []
    for filename in answers:
        filename_noext = os.path.splitext(os.path.basename(filename))[0]
        matr_answers.append([filename, filename_noext.split('_')[1], int(filename_noext.split('_')[2])])

    # create 3D array for inizial questions
    matr_initquest = []
    for filename in initial_questions:
        filename_noext = os.path.splitext(os.path.basename(filename))[0]
        matr_initquest.append([filename, filename_noext.split('_')[1], int(filename_noext.split('_')[2])])

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

    for j in range(int(n_questions)):
        # choose random interrogator
        interrogator = random.choice(q_participants)
        
        # choose first person to ask X each question
        for i in matr_questions:
            if str(interrogator) == str(i[1]) and int(j+1) == int(i[2]):
                file_names = add_file(file_names, i[0])
                break

        random.shuffle(q_participants)
        # choose first person answer X each question
        for i_a in range(int(n_answers)-1):
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

    return file_names

def user_NO_ask_files(count_answers, count_questions):
    while True:
       tmp_n_answers = input(f"Vuoi specificare un numero massimo di persone che rispondono alla domanda (massimo: {count_answers})? Se SI, quante? ")
       if str(tmp_n_answers).lower() == "no":
           n_answers = -1
           break
       elif str(tmp_n_answers).isnumeric() and int(tmp_n_answers)<=count_answers:
           n_answers = tmp_n_answers
           break
       elif str(tmp_n_answers).isnumeric() and int(tmp_n_answers)>count_answers:
           print(f"Il numero deve essere <= {count_answers}")
       else:
           print("Il valore inserito non è corretto. Riprova.")
    while True:
       tmp_n_questions = input(f"Vuoi specificare un numero massimo di domande (massimo: {count_questions})? Se SI, quante? ")
       if str(tmp_n_questions).lower() == "no":
           n_questions = -1
           break
       elif str(tmp_n_questions).isnumeric() and int(tmp_n_questions)<=count_questions:
           n_questions = tmp_n_questions
           break
       elif str(tmp_n_questions).isnumeric() and int(tmp_n_questions)>count_questions:
           print(f"Il numero deve essere <= {count_questions}")
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
    return n_answers, n_questions

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
                file = find_file(file, os.path.join(dir_path, "INPUT"))
                file_names = add_file(file, file_names) 
                print(f'\tAggiunto "{file}" con successo.')
                break
            except EOFError:
                print("\n\tProgramma terminato senza successo. Chiusura del programma.")
                exit()
            except Exception as e:
                print(f"\tERRORE: {e}")

def user_input(dir_path, max_participants, count_persons, count_q):
    # count max number of questions per participant
    count_questions = 0
    for i in count_q:
        i = os.path.splitext(os.path.basename(i))[0]
        count_questions = max(count_questions, int(i.split("_")[2]))
    
    # choice manual files add
    while True:
        user_choice = input(f"Vuoi inserire manualmente i files? [SI/NO] ")
        if str(user_choice).lower() == "si":
            file_names = user_ask_files(dir_path, max_participants)
            return file_names
        elif str(user_choice).lower() == "no":
            n_answers, n_questions = user_NO_ask_files(len(count_persons), count_questions)
            file_names = calculator_NO_ask_files(dir_path, n_answers, n_questions)
            return file_names
        else:
            print("Il valore inserito non è corretto. Riprova.")

if __name__ == '__main__':
    '''Important path of input files'''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    count_wrong_name, max_input_files, count_a, count_q, count_iq, a_letters, q_letters, iq_letters = folder_info(os.path.join(dir_path, "INPUT"))

    print("\n\tGeneratore di dialoghi realistici.\n")
    if count_wrong_name >0:
        print("Found", count_wrong_name, "wav files with wrong file name. See manual for correct file names.\n")
    
    #try:
    '''ask for user input, if more than one file with same name, return the first file'''
    file_names = user_input(dir_path, max_input_files, q_letters, count_q)
    '''Run concatenate (file1, file2) and open the folder'''
    read_write_file(file_names)
    print("\n COMPLETED! (folder opened)")
    os.startfile(os.path.join(dir_path, "output"))
    '''except Exception as e:
        print("\n ! ERRORE: \n\tOperazione interrotta per un errore interno: {}".format(e))
        exit()'''

# Il programma vede quali files ci sono nella cartella e chiede all'utente se vanno bene quegli interlocutori.
# chiede all'utente:
    # lunghezza massima
        # 
    # quante persone parlano
        # se sì quali?