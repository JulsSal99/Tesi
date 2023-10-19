import libsinstall
libsinstall.install_libraries()

import re
import os
import subprocess
import soundfile as sf
import numpy as np
import random

def audioread(filename, frames=-1, start=0, fill_val=None):
    if filename.lower().endswith('mp3'):
        file_do_exist = True
        while file_do_exist:
            temp_id = str(np.random.randint(100000, 999999))
            temp_file = filename[:-4] + '_' + temp_id + '.wav'
            file_do_exist = os.path.isfile(temp_file)
        mp32wav(filename, temp_file, frames, start)
        data, Fs = sf.read(temp_file)
        os.remove(temp_file)
    else:
        data, Fs = sf.read(filename, frames, start, fill_value=fill_val)
    return data, Fs

def mp32wav(infile, outfile, frames=-1, start=0):
    if not os.path.isfile(infile):
        raise Exception(f"Cannot find {infile}")

    if frames + start <= 0:
        cmd = f'ffmpeg -nostdin -y -i "{infile}" "{outfile}"'
    else:
        Fs = audioinfo(infile).Fs
        t = float(frames) / Fs
        ss = float(start) / Fs
        cmd = f'ffmpeg -nostdin -y -ss {ss} -t {t} -i "{infile}" "{outfile}"'

    try:
        err = 0
        subprocess.call(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        err = e.returncode
    if err != 0:
        raise Exception(f"Error executing {cmd}\nffmpeg may be missing")

def audioinfo(infile):
    if not os.path.isfile(infile):
        raise Exception(f"Cannot find {infile}")

    try:
        err = 0
        cmd = f'ffprobe -show_streams "{infile}"'
        ffout = subprocess.check_output(cmd, shell=True).decode("utf-8")
    except subprocess.CalledProcessError as e:
        err = e.returncode
    if err != 0:
        raise Exception(f"Error executing {cmd}\nffprobe may be missing")

    info = {}
    info['Fs'] = float(re.search('sample_rate=(.*)\\r', ffout).group(1))
    info['ch'] = int(re.search('channels=(.*)\\r', ffout).group(1))
    info['duration'] = float(re.search('duration=(.*)\\r', ffout).group(1))
    info['length'] = int(re.search('duration_ts=(.*)\\r', ffout).group(1))
    info['codec'] = re.search('codec_name=(.*)\\r', ffout).group(1)
    info['bit'] = int(re.search('bits_per_sample=(.*)\\r', ffout).group(1))
    return info

def audio_file(path_file, data_file, name_file, person_file, duplicated: bool):
    file = {}
    file['path'] = path_file
    file['data'] = data_file
    file['name'] = name_file
    file['person'] = person_file
    file['duplicated'] = duplicated
    return file

def find_file(name, path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if name in file and (file.endswith(".wav") or file.endswith(".mp3")):
                return os.path.join(root, file)
    raise Exception(f"File {name}.wav or {name}.mp3 not found in {path}")

def folder_info(folder_path):
    mp3_wav_count = 0
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp3') or filename.endswith('.wav'):
            mp3_wav_count += 1
    return mp3_wav_count

def concatenate(data1, data2, pause_length, sample_rate, channels):
    n_sample_silence = sample_rate * pause_length
    silence = np.zeros((int(n_sample_silence), channels))
    if len(data1.shape) > 1 or len(data2.shape) > 1:
        OUTPUT = np.concatenate((data1, silence, data2), axis=0)
    else:
        OUTPUT = np.concatenate((data1, silence, data2))
    return OUTPUT

def get_channels(data):
    if len(np.shape(data)) == 1:
        return 1
    else:
        return np.shape(data)[1]

def check_SR_CH(file_names, sample_rate, channels):
    for i in range(len(file_names)):
        file_names[i]['data'], sample_rate_temp = audioread(file_names[i]['path'])
        channels_temp = get_channels(file_names[i]['data'])
        if i == 0:
            sample_rate = sample_rate_temp
        elif sample_rate != sample_rate_temp:
            raise Exception(f"\nIl file audio n{i+1} ha frequenza di campionamento diversa ({sample_rate_temp} hz).")
        elif channels != channels_temp:
            raise Exception(f"\n Il file audio n{i+1} ha numero di canali diverso ({channels_temp} ch).")

def read_write_file(file_names):
    data_temp, sample_rate = audioread(file_names[0]['path'])
    channels = get_channels(data_temp)
    _, sample_rate = audioread(file_names[0]['path'])
    check_SR_CH(file_names, sample_rate, channels)
    silences = []
    for i in range(len(file_names) - 1):
        pause_length = random.uniform(0.7, 0.9)  # seconds
        silences.append(pause_length)
    for i in range(len(file_names)):
        print_person = file_names[i]['person']
        if not file_names[i]['duplicated']:
            print_name = file_names[i]['name']
            for j in range(len(file_names)):
                if j == 0:
                    if file_names[j]['person'] == print_person:
                        OUTPUT = file_names[0]['data']
                    else:
                        OUTPUT = np.zeros((int(len(file_names[0]['data'])), channels))
                else:
                    if file_names[j]['person'] == print_person:
                        OUTPUT = concatenate(OUTPUT, file_names[j]['data'], silences[j - 1], sample_rate, channels)
                    else:
                        file_silence = np.zeros((int(len(file_names[j]['data'])), channels))
                        OUTPUT = concatenate(OUTPUT, file_silence, silences[j - 1], sample_rate, channels)
            sf.write(f'OUTPUT/merged{i}{print_name}.wav', OUTPUT, sample_rate)

def user_input(dir_path, max_participants):
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