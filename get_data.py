from serpapi import GoogleSearch
import requests
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

output_string = StringIO()
serpapi_api_key = "edd83773cbed6d242886297694fd94297237a8d11b916cf7e51d50d8fb46c32f"
elsevier_api_key = "87103ccd3ec88b1acdcd2496609f5aa6"
filename = 'or100.09.pdf'

with open(filename , 'rb') as r:
    parser = PDFParser(r)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)


reference_count = 1
matches = 0
with open('refid2link.tsv','w') as w:
    for section in output_string.getvalue().split('REFERENCES')[1:]:
        for reference in section.split('\n'):
            if len(reference) > 3:
                number = reference.split(' ')[0]
                try:
                    if int(number) == reference_count: 
                        query = ' '.join(reference.split(' ')[1:])
                        reference_count += 1
                        matches += 1
                        params = {"engine": "google_scholar","q": query,"api_key": serpapi_api_key}
                        client = GoogleSearch(params)
                        results = client.get_dict()
                        organic_results = results['organic_results']
                        url= organic_results[0]['link']
                        w.write("{}\t{}\n".format(reference_count,url))
                        response = requests.get(url)
                        with open('{}.html'.format(reference_count), 'wb') as f:
                            f.write(response.content)
                except:
                    pass