#!/bin/bash
for filename in *.pdf; do
    pdftoppm $filename $filename -png
done
