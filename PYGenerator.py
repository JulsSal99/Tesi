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

__version__ = "0.02"
__author__  = "G.Salada"

'''
------------------------
'''

def audioread(filename, frames=-1, start=0, fill_val=None):
    '''Returns audio data in range -1:1 together with sample rate'''
    '''Additional params: start, frames, fill_value'''
    data, Fs = sf.read(filename, frames, start, fill_value=fill_val)
    return data, Fs

def audio_file(path_file, data_file, name_file, person_file, duplicated: bool):
    file = {}
    file['path'] = path_file
    file['data'] = data_file
    file['name'] = name_file
    file['person'] = person_file
    file['duplicated'] = duplicated
    return file

def find_file(name, path):
    '''Search for the file by its name with and without the extension'''
    '''and return the first file found with the exact path of the file.'''
    for root, dirs, files in os.walk(path):
        for file in files:
            if name in file and (file.lower().endswith(".wav")):
                return os.path.join(root, file)
    raise Exception(f"File {name}.wav not found in {path}")

def folder_info(folder_path):
    '''count the number of audio files in a folder'''
    count = 0
    for filename in os.listdir(folder_path):
        if filename.endswith('.wav'):
            count += 1
    return count

def get_channels(data):
    '''Get the number of channels in an audio file'''
    if len(np.shape(data)) == 1:
        return 1
    else:
        return np.shape(data)[1]

def concatenate(data1, data2, pause_length, sample_rate, channels):
    '''generate 2 audio files, one with the first audio muted,'''
    ''' the second with the second audio muted.'''
    n_sample_silence = sample_rate * pause_length
    silence = np.zeros((int(n_sample_silence), channels))
    if len(data1.shape) > 1 or len(data2.shape) > 1:
        OUTPUT = np.concatenate((data1, silence, data2), axis=0)
    else:
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
                        OUTPUT = np.zeros((int(len(file_names[0]['data'])), channels))
                else:
                    # aggiunge pausa e concatena elementi pieni o vuoti in base al valore di i.
                    if file_names[j]['person'] == print_person:
                        OUTPUT = concatenate(OUTPUT, file_names[j]['data'], silences[j - 1], sample_rate, channels)
                    else:
                        file_silence = np.zeros((int(len(file_names[j]['data'])), channels))
                        OUTPUT = concatenate(OUTPUT, file_silence, silences[j - 1], sample_rate, channels)
            sf.write(f'OUTPUT/merged{i}{print_name}.wav', OUTPUT, sample_rate)
    
    read_write_complete(file_names, sample_rate, channels, silences)

def user_input(dir_path, max_participants):
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
                filename_without_extension = os.path.splitext(os.path.basename(file))[0]
                person = filename_without_extension.split("_")[1]
                duplicated = False
                if person in [file_names[i]['person'] for i in range(len(file_names))]:
                    duplicated = True
                file_names.append(audio_file(file, 0, filename_without_extension, person, duplicated))
                print(f'\tAggiunto "{file}" con successo.')
                break
            except EOFError:
                print("\n\tProgramma terminato senza successo. Chiusura del programma.")
                exit()
            except Exception as e:
                print(f"\tERRORE: {e}")

if __name__ == '__main__':
    '''Important path of input files'''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    max_participants = folder_info(os.path.join(dir_path, "INPUT"))

    print("\nGeneratore di dialoghi realistici.\n")

    try:
        '''ask for user input, if more than one file with same name, return the first file'''
        file_names = user_input(dir_path, max_participants)
        '''Run concatenate (file1, file2) and open the folder'''
        read_write_file(file_names)
        print("\n COMPLETED! (folder opened)")
        os.startfile(os.path.join(dir_path, "output"))
    except Exception as e:
        print("\n ! ERRORE: \n\tOperazione interrotta per un errore interno: {}".format(e))
        exit()

# manca il controllo che nella cartella non ci siano più files con lo stesso nome (posso dichiarare che prende il primo file)