## 2020 KISTI AI analysis & application National Competition <br/>(prize-winning project, 2th place)
- Subject : Developing tool that visualizes the flow of emotions of counselee while doing psycho-therapy via timeline chart using Deep Learning

# psycho-therapy-assistant
<strong>_psycho-therapy-assistant_</strong> is a assistive tool for Psychotherapy that listens to counselee's speaking, show a timeline graph of flow of emotions to counselor. It classifies sentences of speaking into 28 kinds of emotions (e.g. happiness, sadness, disappointment, neutral, ...). It internally uses _Deepspeech_ as a STT(speech-to-text) model, _bert_ as a tagging model.

## System Process
`speecn2text.py` is the file which listens to the input sound file, then takes the contents down as a text using _deepspeech_ STT(speech to text) library.

`mybert_classifier.py` is the file which gets the output of `speech2text.py` as a input file, then returns the sentences of the contents with 28 kinds of emotion tags using customized _bert_ model.


1. When you execute `speech2text.py` file, it will read .wav file which you give as a command line parameter.
2. Resample input file and adjust the sampling rate using _librosa_.
3. Split the input file in each one-minute interval and read each of them.
4. Return `STT.csv` as a result.
5. When you execute `mybert_classifier.py` file, it will read `STT.csv` located in `final_bert_emotion_classifier/csv_files` folder.
6. Return `STT_emotion_predictions.tsv` as a result in `final_bert_emotion_classifier/csv_files/result` folder.
7. When you execute `index.html` which is located in same folder as `STT_emotion_predictions.tsv` file, it will automatically read the result file and show you the timeline graph. 
  <small>Note that you should consider CORS policy when you execute `index.html`</small>

## Requirements

  `requirements.txt`

## Quick Configuration
Simply run settings.sh to configure environment variables.

  `sh settings.sh`

## Usage
Run run.sh with the path of sound file as a command line parameter.

  `sh run.sh ./final_bert_emotion_classifier/csv_files/sample.wav`
  
  
## References
[1] https://github.com/mozilla/DeepSpeech Deepspeech

[2] https://github.com/google-research/bert bert 

[3] Mattias Heldner, Jens Edlund, _Pauses, gaps and overlaps in conversations_, Oct, 2010.
