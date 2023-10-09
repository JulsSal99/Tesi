import libsinstall
libsinstall.install_libraries()

import re
import os
import subprocess
import soundfile as sf
import numpy as np
import random

'''

This library has some functions (audioread, mp32wav and audioinfo) from DSPfunc by G.Presti

Should work on both Python 3.x (tested on Python 3.11.6)
Look at the test() function for some examples...

This collection is based upon the following packages:
  - numpy
  - pysoundfile
  - spectrum

This collection also requires the following software:
  - ffmpeg (optional, for mp3 handling)
  
'''

__version__ = "0.01"
__author__  = "G.Salada"


'''
------------------------
'''


def audioread( filename, frames=-1, start=0, fill_val=None ):
    '''Returns audio data in range -1:1 together with sample rate'''
    '''Additional params: start, frames, fill_value'''
    '''WARNING: mp3 read may end in len(data)!=frames'''
    if (filename[-3:].lower() == 'mp3'):
        fileDoExist = True
        while fileDoExist:
            temp_id = str(np.random.randint(100000,999999))
            tempfile = filename[:-4] + '_' + temp_id + '.wav'
            fileDoExist = os.path.isfile(tempfile)
        mp32wav(filename, tempfile, frames, start)
        data, Fs = sf.read(tempfile)
        os.remove(tempfile)
    else:
        data, Fs = sf.read(filename, frames, start, fill_value = fill_val)
    return data, Fs

def mp32wav( infile, outfile, frames=-1, start=0 ):
    '''Convert an mp3 to a wav file using ffmpeg'''
    '''additional params let you choose the number of frames and starting offset'''
    '''WARNING: will overwrite existing files without asking!'''

    if not os.path.isfile( infile ):
        raise Exception("Cannot find {0}".format( infile ))
    
    if (frames+start <= 0):
        cmd = 'ffmpeg -nostdin -y -i "' + infile + '" "' + outfile + '"'
    else:        
        Fs = audioinfo(infile).Fs
        t = float(frames) / Fs
        ss = float(start) / Fs
        cmd = 'ffmpeg -nostdin -y -ss ' + str(ss) + ' -t ' + str(t) + ' -i "' + infile + '" "' + outfile + '"'
        
    try:
        err = 0
        subprocess.call(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        err = e.returncode
    if err != 0:
        raise Exception("Error executing {0}\n\rffmpeg may be missing".format(cmd))    

def audioinfo( infile ):
    '''Get audio file stream info using ffprobe'''
    '''returns an object with attributes Fs, ch, bit, duration, length, codec'''
    '''WARNING: info.bit = 0 in case of lossy codec'''
    
    if not os.path.isfile( infile ):
        raise Exception("Cannot find {0}".format( infile ))
    
    try:
        err = 0
        cmd = 'ffprobe -show_streams "' + infile + '"'
        ffout = subprocess.check_output(cmd, shell=True).decode("utf-8")
    except subprocess.CalledProcessError as e:
        err = e.returncode
    if err != 0:
        raise Exception("Error executing {0}\n\rffprobe may be missing".format(cmd))

    class Info: pass
    info = Info()
    info.Fs = float(re.search('sample_rate=(.*)\\r',ffout).group(1))
    info.ch = int(re.search('channels=(.*)\\r',ffout).group(1))
    info.duration = float(re.search('duration=(.*)\\r',ffout).group(1))
    info.length = int(re.search('duration_ts=(.*)\\r',ffout).group(1))
    info.codec = re.search('codec_name=(.*)\\r',ffout).group(1)
    info.bit = int(re.search('bits_per_sample=(.*)\\r',ffout).group(1))   
    return info

def audio_file(path_file, data_file, name_file, person_file, duplicated: bool):
    '''Create a class audio_file that contains infos/data about that audio file'''
    class File: pass
    file = File()
    file.path = path_file
    file.data = data_file
    file.name = name_file
    file.person = person_file
    file.duplicated = duplicated
    #file.length = length_file
    return file

def find_file(name, path):
    '''Search for the file by its name with and without the extension'''
    '''and return the first file found with the exact path of the file.'''
    for root, dirs, files in os.walk(path):
        for file in files:
            if name in file and (file.endswith(".wav") or file.endswith(".mp3")):
                return os.path.join(root, file)
    raise Exception(f"File {name}.wav or {name}.mp3 not found in {path}")

def folder_info(folder_path):
    '''count the number of audio files in a folder'''
    mp3_wav_count = 0
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp3') or filename.endswith('.wav'):
            mp3_wav_count += 1
    return mp3_wav_count

def concatenate(data1, data2, pause_lenght, sample_rate, channels):
    '''generate 2 audio files, one with the first audio muted,'''
    ''' the second with the second audio muted.'''
    n_sample_silence = sample_rate * pause_lenght
    silence = np.zeros((int(n_sample_silence), channels))
    if len(data1.shape) > 1 or len(data2.shape) > 1:
        OUTPUT = np.concatenate((data1, silence, data2), axis=0)
    else:
        OUTPUT = np.concatenate((data1, silence, data2))
    return(OUTPUT)

def get_channels(data):
    '''Get the number of channels in an audio file'''
    if len(np.shape(data)) == 1:
        return 1
    else:
        return np.shape(data)[1]
    
def check_SR_CH(file_names, sample_rate, channels):
    '''Check sample rate and channels of the audio files'''
    for i in range(len(file_names)):
        file_names[i].data, sample_rate_temp = audioread(file_names[i].path)
        channels_temp = get_channels(file_names[i].data)
        if i == 0:
            sample_rate = sample_rate_temp
        elif sample_rate != sample_rate_temp:
            raise Exception(f"\nIl file audio n{i+1} ha frequenza di campionamento diversa ({sample_rate_temp} hz).")
        elif channels != channels_temp:
            raise Exception(f"\n Il file audio n{i+1} ha numero di canali diverso ({channels_temp} ch).")

def read_write_file(file_names):
    ''' MAIN FUNCTION: create the ending file'''
    ''' create the class inside file_names and return to concatenate()'''
    ''' check channels, sample_rate'''
    # Get sample rate
    data_temp, sample_rate = audioread(file_names[0].path)
    # Get channels number
    channels = get_channels(data_temp)

    # Get sampled data from files and check sample rate and channels
    _, sample_rate = audioread(file_names[0].path)
    check_SR_CH(file_names, sample_rate, channels)

    # create an array of pause_length for each (between) file
    silences = []
    for i in range(len(file_names)-1):
        pause_length = random.uniform(0.7, 0.9) #seconds
        silences.append(pause_length)
    
    # i è l'elemento da stampare con i dati, mentre j è l'elemento attuale
    for i in range(len(file_names)):
        print_person = file_names[i].person
        if file_names[i].duplicated == False:
            print_name = file_names[i].name
            for j in range(len(file_names)):
                if j == 0:
                    # gestisce il primo elemento e lo mette vuoto se non è lui
                    if file_names[j].person == print_person:
                        OUTPUT = file_names[0].data
                    else:
                        OUTPUT = np.zeros(( int( len( file_names[0].data ) ), channels ))
                else:
                    # aggiunge pausa e concatena elementi pieni o vuoti in base al valore di i.
                    if file_names[j].person == print_person:
                        OUTPUT = concatenate(OUTPUT, file_names[j].data, silences[j-1], sample_rate, channels)
                    else:
                        file_silence = np.zeros(( int( len( file_names[j].data ) ), channels ))
                        OUTPUT = concatenate(OUTPUT, file_silence, silences[j-1], sample_rate, channels)
            sf.write(f'OUTPUT/merged{i}{print_name}.wav', OUTPUT, sample_rate)

def user_input(dir_path,max_participants):
    '''Ask file1, file2'''
    ''' and check/fix paths (file1, file2)'''
    ''' handle the errors'''
    file_names = []
    for i in range(max_participants):
        while True:
            try:
                file = input(f"Inserisci il nome del {i+1}o audio (scrivi FINE per terminare, max {max_participants - i}): ")
                if file == "FINE" and i > 1:
                    return file_names
                elif file == "FINE" and i <= 1:
                    raise Exception("Non abbastanza files!!!")
                file = find_file(file, dir_path+"\INPUT")
                filename_without_extension = os.path.splitext(os.path.basename(file))[0]
                person = filename_without_extension.split("_")[1]
                duplicated = False
                if person in [file_names[i].person for i in range(len(file_names))]:
                    duplicated = True
                # crea un array costituito da elementi della classe File da audio_file
                file_names.append((audio_file(file, 0, filename_without_extension, person, duplicated)))
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
    max_participants = folder_info(dir_path+"\INPUT")

    print("\nGeneratore di dialoghi realistici.\n")

    try:
        '''ask for user input, if more than one file with same name, return the first file'''
        file_names=user_input(dir_path,max_participants)
        '''Run concatenate (file1, file2) and open the folder'''
        read_write_file(file_names)
        print("\n COMPLETED! (folder opened)")
        os.startfile(dir_path + "\output")
    except Exception as e:
        print("\n ! ERRORE: \n\tOperazione interrotta per un errore interno: {}".format(e))
        exit()


# manca il controllo che nella cartella non ci siano più files con lo stesso nome (posso dichiarare che prende il primo file)