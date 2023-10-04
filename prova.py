
import re
import os
import subprocess
import soundfile as sf
import numpy as np

'''

This library has some functions from DSPfunc by G.Presti

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

def audio_file(path_file, length_file: float, data_file):
    '''crea una classe contenente i dati per la concatenazione'''
    class File: pass
    file = File()
    file.path = path_file
    file.length = length_file
    file.data = data_file
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

def concatenate(data1, data2, pause_lenght, sample_rate):
    '''generate 2 audio files, one with the first audio muted,'''
    ''' the second with the second audio muted.'''
    #calcolo il numero di canali
    channels = data1.shape[1]

    # Calcola il numero di campioni necessari per 0.2 secondi di silenzio
    n_sample_silence = sample_rate * pause_lenght

    # Creiamo un array numpy di zeri per rappresentare il silenzio
    data1_length = len(data1)
    data2_length = len(data2)
    # Crea un array di campioni di audio vuoti con n canali (shape)
    silence = np.zeros((int(n_sample_silence), channels))
    data1_silence = np.zeros((int(data1_length), channels))
    data2_silence = np.zeros((int(data2_length), channels))

    if len(data1.shape) > 1 or len(data2.shape) > 1:
        OUTPUT1 = np.concatenate((data1_silence, silence, data2), axis=0)
        OUTPUT2 = np.concatenate((data1, silence, data2_silence), axis=0)
    else:
        OUTPUT1 = np.concatenate((data1_silence, silence, data2))
        OUTPUT2 = np.concatenate((data1, silence, data2_silence))
    
    return(OUTPUT1, OUTPUT2)

def read_write_file(filename1, filename2):
    data1, samplerate1 = audioread(filename1)
    data2, samplerate2 = audioread(filename2)

    pause_lenght = 0.9 #seconds

    if samplerate1 != samplerate2:
        raise Exception("I due file audio hanno frequenze di campionamento diverse.")

    OUTPUT1, OUTPUT2 = concatenate(data1, data2, pause_lenght, samplerate1)
    sf.write('OUTPUT/merged1.wav', OUTPUT1, samplerate1)
    sf.write('OUTPUT/merged2.wav', OUTPUT2, samplerate1)

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    max_participants = folder_info(dir_path+"\INPUT")

    print("\nGeneratore di dialoghi realistici.\n")

    n_participants = int(input("Numero di partecipanti al dialogo: "))
    if n_participants <= 1 or n_participants > max_participants:
        raise Exception(f"Non abbastanza files o numero errato!")

    '''Ask file1, file2'''
    ''' and check/fix paths (file1, file2)'''
    file_names = []
    for i in range(n_participants):
        file = input("Inserisci il nome del {}o audio: ".format(i+1))
        file = find_file(file, dir_path+"\INPUT")
        # crea un array costituito da elementi della classe File da audio_file
        file_names.append((audio_file(file, 0, 0)))

    '''Run concatenate (file1, file2)'''
    read_write_file(file_names[0].path, file_names[1].path)
    print("\n COMPLETED!")
    os.startfile(dir_path + "\output")

# manca il controllo che nella cartella non ci siano più files con lo stesso nome