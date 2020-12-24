## 2020 KISTI AI analysis & application National Competition (prize-winning project, got 2th place)
- Subject : Developing tool that visualizes the flow of emotions of counselle while doing psycho-therapy via timeline chart using Deep Learning

# psycho-therapy-assistant
Making psycho-therapy-assistant using STT and emotion-tagging model.

## System Process
`speecn2text.py` is the file which listens to the input sound file, then takes the contents down as a text using _deepspeech_ STT(speech to text) library.

`mybert_classifier.py` is the file which gets the output of `speech2text.py` as a input file, then returns the sentences of the contents with 28 kinds of emotion tags using customized _bert_ model.

1. When you execute `speech2text.py` file, it will read .wav file which you give as a command line parameter.
2. Resample input file and adjust the sampling rate using _librosa_.
3. Split the input file in each one-minute interval and read each of them.
4. Return `STT.csv` as a result.
5. When you execute `mybert_classifier.py` file, it will read `STT.csv` located in final_bert_emotion_classifier/csv_files folder.
6. Return `STT_emotion_predictions.tsv` as a result.

## Quick Configure
  `sh settings.sh`

## Usage
  sh run.sh [.wav file path]

  `sh run.sh ./final_bert_emotion_classifier/csv_files/sample.wav`
  
  
## References

