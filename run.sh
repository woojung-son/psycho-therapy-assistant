#!/bin/bash
CURRENT_DIR="$( cd "$( dirname "$0" )" && pwd -P )"
BERT_EXEC_PATH=$CURRENT_DIR/final_bert_emotion_classifier/GoEmotion_bert
BERT_FILE_PATH=$CURRENT_DIR/final_bert_emotion_classifier/csv_files

NumOfArgs=$#
ZERO=0
STT=speech2text.py
SOURCE_FILE="$( basename "$1" )"
SOURCE_FILE_DIR="$( cd "$( dirname "$1" )" && pwd -P )"
SOURCE_FILE_BASENAME="$( basename "$1" .wav )"
SOURCE_FILE_RESULT=$SOURCE_FILE_BASENAME'_result.csv'

DEFAULT_FILE=sample.wav
DEFAULT_FILE_PATH=$CURRENT_DIR/final_bert_emotion_classifier/csv_files
DEFAULT_FILE_BASENAME="$( basename "$DEFAULT_FILE" .wav )"
DEFAULT_FILE_RESULT=$DEFAULT_FILE_BASENAME'_result.csv'

echo "running STT ...\n"

if [ $NumOfArgs -eq $ZERO ]; then
	echo "Usage : ./woojung.sh [SOURCEFILE PATH]\n"
	echo "**You should set the sourcefile path as a parameter**\n\n"
	echo "Running with sample file : ${DEFAULT_FILE}\n"

	python $CURRENT_DIR/$STT $DEFAULT_FILE_PATH/$DEFAULT_FILE
	mv $BERT_FILE_PATH/$DEFAULT_FILE_RESULT $BERT_FILE_PATH/STT.csv
else
	echo "SOURCE_FILE_DIR : $SOURCE_FILE_DIR\n"
	python $CURRENT_DIR/$STT $SOURCE_FILE_DIR/$SOURCE_FILE
	mv $SOURCE_FILE_DIR/$SOURCE_FILE_RESULT $SOURCE_FILE_DIR/STT.csv
fi

cd $BERT_EXEC_PATH

echo "running Bert ...\n"
python mybert_classifier.py

echo "save result in $BERT_FILE_PATH/result/"
mv $BERT_FILE_PATH/STT_emotion_predictions.tsv $BERT_FILE_PATH/result/STT_emotion_predictions.tsv

echo "\nDone. \n"
