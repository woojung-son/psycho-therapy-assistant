import numpy as np
import os
import wave
import pandas as pd
import sys 
import librosa
import soundfile as sf
from deepspeech import Model
import subprocess


sec = 30

### Split wav files with chunksize as 60 sec
def split_audio(audio_path, sample_rate=16000, chunksize_secs=sec):
    import glob
    import scipy.io.wavfile as wav
    audio_path_noext = os.path.splitext(audio_path)[0]
    fs, _ = wav.read(audio_path)
    if fs != sample_rate:
        if fs < sample_rate:
            print('Warning: original sample rate ({}) is lower than {}Hz. \
                Up-sampling might produce erratic speech recognition.'.format(fs, sample_rate), file=sys.stderr)

    print('Resampling audio to {}Hz'.format(sample_rate))
  
    sox_cmd = 'sox {} --rate {} --bits 16 --channels 1 {}_resampled.wav'.\
        format(audio_path, sample_rate, audio_path_noext)
    try:
        p = subprocess.Popen(sox_cmd.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        _, err = p.communicate()

        if p.returncode:
            raise RuntimeError('SoX returned non-zero status: {}'.format(err))

        print('Splitting audio into {}s chunks'.format(chunksize_secs))

        # sox foo_resampled.wav foo_chunk.wav trim 0 6 : newfile : restart
        sox_cmd = 'sox {}_resampled.wav {}_chunk.wav trim 0 {} : newfile : restart'.format(audio_path_noext, audio_path_noext, chunksize_secs)
        p = subprocess.Popen(sox_cmd.split(),stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        _, err = p.communicate()

        if p.returncode:
            raise RuntimeError('SoX returned non-zero status: {}'.format(err))
    except OSError as e:
        raise OSError('SoX not found, use {}Hz files or install it: '.format(sample_rate), e)

    # list of chunked files
    return sorted(glob.glob('{}_chunk*.wav'.format(audio_path_noext)))


## read wav file and return buffer, rate and frames
def read_wav_file(filename) :
    print('Reading wav file........')
    with wave.open(filename, 'rb') as w :
        rate = w.getframerate()
        frames = w.getnframes()
        buffer = w.readframes(frames)    

    if(rate!=16000):
        y,sr =librosa.load(filename,16000)
        sf.write('resampled_tmp.wav',y,sr,format='WAV', endian='LITTLE', subtype='PCM_16')
        
        print('Rereading wav file........')
        with wave.open('resampled_tmp.wav', 'rb') as w :
            rate = w.getframerate()
            frames = w.getnframes()
            buffer = w.readframes(frames)   
        
    return buffer, rate, frames


def transcribe(audio_file) :
    buffer, rate, frames = read_wav_file(audio_file)
    print('')
    print('Transcribing {} to Metadata.....'.format(audio_file))
    data16 = np.frombuffer(buffer, dtype = np.int16)
    return model.sttWithMetadata(data16)


## convert Metadata to DataFrame with timestamps
def MetaToDf(timeobject,emptytime = 0.8) :
    tmp = timeobject.transcripts
    tmp1 = tmp.pop()
    tmp2 = tmp1.tokens
    
    FindEmpty=[0]
    text = ''
    for i in range(len(tmp2)):
        text = str(text)+tmp2[i].text
        if(tmp2[i].text == ' '):
            if(i == len(tmp2)-1) :     
                pass
            elif(i == 0) :
                pass
            else :
                if(tmp2[i+1].start_time - tmp2[i-1].start_time >= float(emptytime)):
                    FindEmpty.append(i+1)
    FindEmpty.append(len(text))
    
    print(len(FindEmpty))
    results = pd.DataFrame(columns=['text','start_time','end_time'])
    if(len(FindEmpty) <= 2) :
        results = results.append(pd.Series([' ', 0, 30], index = results.columns), ignore_index=True)
    else :
        for j in range(1,len(FindEmpty)):
            befo=FindEmpty[j-1]
            afte=FindEmpty[j]
            timestamS = tmp2[befo].start_time
            timestamE = tmp2[afte-2].start_time
            print(text[befo:afte],'\t',timestamS,'\t',timestamE)
            results = results.append(pd.Series([text[befo:afte], timestamS, timestamE], index = results.columns), ignore_index=True)
    
    return results


def WavToDf(audio_file , emptytime = 0.8 ) :
    buffer, rate, frames = read_wav_file(audio_file)
    
    if(frames > (16000*sec)) :  ## 6sec = 16000
        print('Chunking...')
        split_list = split_audio(audio_file)
        
        result_df = pd.DataFrame()
        count = 0
        print(split_list)
        for i in split_list : 
            timeobject = transcribe(i)
            df = MetaToDf(timeobject, emptytime)
            df['start_time'] = df['start_time']+(sec*count)
            df['end_time'] = df['end_time']+(sec*count)
            result_df = result_df.append(df) 
            count = count + 1
        
    else :
        print('Transcribing...')
        timeobject = transcribe(audio_file)
        result_df = MetaToDf(timeobject)
    
    result_df.to_csv(audio_file[:-4]+'_result.csv',header = None, index=False,float_format = '%.2f', encoding = 'utf-8-sig')
    


if __name__ =="__main__":
    
    model_file_path = 'deepspeech-0.9.1-models.pbmm'
    lm_file_path = 'deepspeech-0.9.1-models.scorer'

    beam_width = 1000
    lm_alpha = 0.93
    lm_beta = 1.18
    model = Model(model_file_path)
    model.enableExternalScorer(lm_file_path)
    model.setScorerAlphaBeta(lm_alpha, lm_beta)
    model.setBeamWidth(beam_width)

    argv = sys.argv
    
    #WavToDf(argv[1],argv[2])
    WavToDf(argv[1])
