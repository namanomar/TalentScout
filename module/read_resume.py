import spacy
import json
import PyPDF2
import requests
from collections import Counter

class EntityGenerator:
    __slots__ = ['text']

    def __init__(self, text=None):
        self.text = text

    def get(self):
        """ Return extracted entities as JSON """
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.text)

        text = [ent.text for ent in doc.ents]
        entity = [ent.label_ for ent in doc.ents]

        # Count unique entities
        data = Counter(entity)
        unique_entity = list(data.keys())

        # Create dictionary for entity grouping
        d = {val: [] for val in unique_entity}

        for key, val in zip(text, entity):
            d[val].append(key)

        return json.dumps(d, indent=4)

class Resume:
    def __init__(self, filename=None):
        self.filename = filename

    def get(self):
        """ Extract text from a PDF resume """
        with open(self.filename, 'rb') as fFileObj:
            pdfReader = PyPDF2.PdfReader(fFileObj)
            print("Total Pages : {} ".format(len(pdfReader.pages)))

            # Extract text from all pages
            resume_text = ""
            for page in pdfReader.pages:
                resume_text += page.extract_text()  

        return resume_text
