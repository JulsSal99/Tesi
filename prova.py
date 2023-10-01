
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


def concatenate(filename1, filename2, frames=-1, start=0 ):
    data1, samplerate1 = audioread(filename1)
    data2, samplerate2 = audioread(filename2)

    if samplerate1 != samplerate2:
        raise ValueError("I due file audio hanno frequenze di campionamento diverse.")

    if len(data1.shape) > 1 or len(data2.shape) > 1:
        raise ValueError("I due file audio non sono mono.")
    
    # Definiamo la durata del silenzio in secondi
    duration = 0.9

    # Creiamo un array numpy di zeri per rappresentare il silenzio
    silence = np.zeros(int(duration * samplerate1))

    data = np.concatenate((data1, silence, data2))

    sf.write('OUTPUT/merged.wav', data, samplerate1)

if __name__ == '__main__':
    testfile1 = 'C:/Users/giuli/Documents/GitHub/Tesi/Sample.wav'
    testfile2 = 'C:/Users/giuli/Documents/GitHub/Tesi/Sample.wav'
    '''Run concatenate (file1, file2)'''
    concatenate(testfile1, testfile2)