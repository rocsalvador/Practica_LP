#!/bin/bash

if antlr4 -Dlanguage=Python3 -no-listener -visitor src/Expr.g; then
    python3 src/main.py $1
fi