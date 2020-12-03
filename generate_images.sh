#!/bin/bash
max=0
for filename in corpus/*.png; do
    a=$(echo $(identify -format '%w-%h' $filename) | cut -f1 -d-)
    b=$(echo $(identify -format '%w-%h' $filename) | cut -f2 -d-)
    max_cur=$(( a > b ? a : b ))
    max=$(( max_cur > max ? max_cur : max ))
    python yolov5/detect.py --source $filename --weights models/train/weights/last.pt --conf-thres 0.5 --img $max --project MMLI --name results --exist-ok --save-txt --save-conf
done
echo $max
