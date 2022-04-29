#!/bin/bash
if [ $# -lt 1 ]; then
    echo Usage:
    echo ./jsbach.sh file.jsb [outFileName]
    exit 1
fi

if [ "$2" == "" ]; then
    OUTFILE=default
else
    OUTFILE=$2
fi

if [ ! -d out ]; then 
    mkdir out 
fi

if antlr4 -Dlanguage=Python3 -no-listener -visitor src/Expr.g &&
   python3 src/jsbach.py $1 out/$OUTFILE && 
   lilypond out/$OUTFILE.lily
then
    timidity -Ow -o $OUTFILE.wav $OUTFILE.midi
    mv $OUTFILE.wav $OUTFILE.pdf $OUTFILE.midi -t out
    ffplay -nodisp -autoexit out/$OUTFILE.wav 
fi