# MMLI

## Reqire,emts
conda create --name MMLI python=3.8
conda activate MMLI
conda install cudatoolkit=10.0
pip install git+https://github.com/allenai/longformer.git
pip install google-search-results
pip install pdfminer.six
pip install transformers torch torchvision 

## Process
1. Download Paper
2. Parse using PDF miner to extract references
3. Search for references using google scholars
4. Download PDF of everything in references
5. Back in origina paper create tuple of information + reference. 
6. Truncate 
## Setup