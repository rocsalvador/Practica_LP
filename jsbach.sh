#!/bin/bash

if [ "$2" == "" ]; then
    OUTFILE=default
else
    OUTFILE=$2
fi

if [ ! -d out ]; then 
    mkdir out 
fi

antlr4 -Dlanguage=Python3 -no-listener -visitor src/Expr.g

python3 src/jsbach.py $1 out/$OUTFILE

lilypond out/$OUTFILE.lily

timidity -Ow -o $OUTFILE.wav $OUTFILE.midi

mv $OUTFILE.wav $OUTFILE.pdf $OUTFILE.midi -t out

ffplay -nodisp -autoexit out/$OUTFILE.wav 