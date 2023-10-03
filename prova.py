
import re
import os
import subprocess
import soundfile as sf
import numpy as np

'''

This library has some functions from DSPfunc by G.Presti

General Purpose Audio DSP functions

Should work on both Python 2.7.x and 3.x
Look at the test() function for some examples...

This collection is based upon the following packages:
  - numpy
  - scipy
  - pysoundfile
  - spectrum
  - matplotlib (for visualization)

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


def concatenate(filename1, filename2):
    data1, samplerate1 = audioread(filename1)
    data2, samplerate2 = audioread(filename2)

    if samplerate1 != samplerate2:
        raise ValueError("I due file audio hanno frequenze di campionamento diverse.")

    #calcolo il numero di canali e campionamento
    channels = data1.shape[1]    
    sample_rate = samplerate1
    # Definiamo la durata del silenzio in secondi
    duration = 0.9

    # Calcola il numero di campioni necessari per 0.2 secondi di silenzio
    n_campioni_silenzio = sample_rate * duration

    # Creiamo un array numpy di zeri per rappresentare il silenzio
    data1_length = len(data1)
    data2_length = len(data2)
    # Crea un array di campioni di audio vuoti con n canali (shape)
    silence = np.zeros((int(n_campioni_silenzio), channels))
    data1_silence = np.zeros((int(data1_length), channels))
    data2_silence = np.zeros((int(data2_length), channels))

    if len(data1.shape) > 1 or len(data2.shape) > 1:
        OUTPUT1 = np.concatenate((data1_silence, silence, data2), axis=0)
        OUTPUT2 = np.concatenate((data1, silence, data2_silence), axis=0)
    else:
        OUTPUT1 = np.concatenate((data1_silence, silence, data2))
        OUTPUT2 = np.concatenate((data1, silence, data2_silence))

    sf.write('OUTPUT/merged1.wav', OUTPUT1, samplerate1)
    sf.write('OUTPUT/merged2.wav', OUTPUT2, samplerate1)
        
def find_file(name, path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if name in file and (file.endswith(".wav") or file.endswith(".mp3")):
                return os.path.join(root, file)
    raise Exception(f"File {name}.wav or {name}.mp3 not found in {path}")

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    testfile1 = input("Inserisci il nome del primo file: ")
    testfile2 = input("Inserisci il nome del secondo file: ")
    '''Run concatenate (file1, file2)'''
    # sarebbe utile generare dialoghi in base a: 
    # voci femminili? 
    # voci maschili? 
    # random?
    # quante domande e risposte? 
    # Pause irrealistiche? 
    file_names = [testfile1, testfile2]
    for i in range(2):
        try:
            file_names[i] = find_file(file_names[i], dir_path)
        except Exception:
            print("il file non esiste")

    concatenate(testfile1, testfile2)