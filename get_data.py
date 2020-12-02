from serpapi import GoogleSearch
import requests
from io import StringIO
import re
from bs4 import BeautifulSoup
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

output_string = StringIO()
serpapi_api_key = "edd83773cbed6d242886297694fd94297237a8d11b916cf7e51d50d8fb46c32f"

def load_pdf(filename):
    with open(filename , 'rb') as r:
        parser = PDFParser(r)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

def get_pdf(doi, filename, corpus_dir):
    url = 'https://sci-hub.se/{}'.format(doi)
    response = requests.get(url)
    soup =  BeautifulSoup(response.content, features="lxml")
    response = requests.get(soup.find(id='article').iframe['src'])
    with open('{}{}.pdf'.format(corpus_dir,filename), 'wb') as f:
        f.write(response.content)

load_pdf('corpus/or100.09.pdf')
print("Document Parsed. Searching Google Scholar For papers")

reference_count = 1
matches = 0
other_matches = 0
with open('refid2urlscholar.tsv','w') as w:
    for section in output_string.getvalue().split('REFERENCES')[1:]:
        for reference in section.split('\n'):
            if len(reference) > 3:
                number = reference.split(' ')[0]
                if number.isnumeric():
                    if int(number) == reference_count: 
                        query = ' '.join(reference.split(' ')[1:])
                        reference_count += 1
                        params = {"engine": "google","q": query,"api_key": serpapi_api_key}
                        corpus_dir = 'corpus/'
                        try:
                            client = GoogleSearch(params)
                            results = client.get_dict()
                            organic_results = results['organic_results']
                            url= organic_results[0]['link']
                            w.write("{}\t{}\n".format(reference_count-1,url))
                            doi = re.findall(r'/10.*',url)
                            other_doi = []
                            if len(doi) == 0:
                                response = requests.get(url)
                                List =  re.findall(r'https?://doi.org/[^\s<>"]+[^\s<>"]', str(response.content))
                                get_pdf(max(set(List), key = List.count).strip("https://doi.org/"), reference_count-1,corpus_dir)
                                matches += 1
                            else:
                                get_pdf(doi[0], reference_count-1,corpus_dir)
                                matches += 1
                        except:
                            pass
                        corpus_dir = 'corpus/scholar_'
                        params = {"engine": "google_scholar","q": query,"api_key": serpapi_api_key}
                        try:
                            client = GoogleSearch(params)
                            results = client.get_dict()
                            organic_results = results['organic_results']
                            url= organic_results[0]['link']
                            w.write("{}\t{}\n".format(reference_count-1,url))
                            doi = re.findall(r'/10.*',url)
                            other_doi = []
                            if len(doi) == 0:
                                response = requests.get(url)
                                List =  re.findall(r'https?://doi.org/[^\s<>"]+[^\s<>"]', str(response.content))
                                get_pdf(max(set(List), key = List.count).strip("https://doi.org/"), reference_count-1,corpus_dir)
                                matches += 1
                            else:
                                get_pdf(doi[0], reference_count-1,corpus_dir)
                                matches += 1
                        except:
                            pass

print("Done creating corpus. \n {} target papers found.".format(matches))