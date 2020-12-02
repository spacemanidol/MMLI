# MMLI

## Reqire,emts
see requirements.txt

## Process
1. Download Paper
2. Parse using PDF miner to extract references
3. Search for references using google scholars
4. Download PDF of what can be found.
5. Extract chemicals and conditions using custom YOLOv5


## Setup
1. '''conda create --name MMLI python=3.8
conda activate MMLI
conda install cudatoolkit=10.0
pip install -r requirements.txt'''
## yoloCHEMEXTRACTION
To set up our CHEMYOLO we first take all our PDFs and split them into PNG. Then, we annotate the data using [makesense.ai](makesense.ai) and with this annotated data train a yolo vision system. 

1. ''' sh make_pdf_png.sh'''
2. ''' git clone https://github.com/ultralytics/yolov5.git'''
3. '''python -m torch.distributed.launch --nproc_per_node 2 yolov5/train.py --img 1755 --batch 2 --epochs 400 --data MMLIconfig.yaml --weights models/yolov5x.pt --cache-images --multi-scale --project models --name train --exist-ok'''
4. Run inference
'''
filename=corpus/103.pdf-05.png
a=$(echo $(identify -format '%w-%h' $filename) | cut -f1 -d-)
b=$(echo $(identify -format '%w-%h' $filename) | cut -f2 -d-)
max=$(( a > b ? a : b ))
python yolov5/detect.py --source $filename --weights models/last.pt --conf-thres 0.75 --img $max --project MMLI --name results --exist-ok --save-txt --save-conf
filename=corpus/103.pdf-03.png
a=$(echo $(identify -format '%w-%h' $filename) | cut -f1 -d-)
b=$(echo $(identify -format '%w-%h' $filename) | cut -f2 -d-)
max=$(( a > b ? a : b ))
python yolov5/detect.py --source $filename --weights models/last.pt --conf-thres 0.75 --img $max --project MMLI --name results --exist-ok --save-txt --save-conf
python train.py --img 640 --batch 16 --epochs 5 --data coco128.yaml --weights
'''
