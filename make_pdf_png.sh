#!/bin/bash
for filename in corpus/*.pdf; do
    pdftoppm $filename $filename -png
done
