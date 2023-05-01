'''
Reads in a GEO Metadata XML file and fills out various database fields outputting a YAML file

Usage: python metadata_annotator.py -a <accession> -o <output_file> -p <path_to_api_key>

'''
import argparse
import openai
from Bio import Entrez

# from lxml import etree
# from lxml import objectify
# from lxml.etree import XMLSyntaxError
# from lxml.etree import XMLParser
# from lxml.etree import XMLSchema
# from lxml.etree import XPath
# from lxml.etree import XPathSyntaxError
# from lxml.etree import XPathEvalError
# from lxml.etree import XSLT
# from lxml.etree import Element

# from io import StringIO
# from io import BytesIO

# import os
# import sys

def assign_openai_key(path_to_api_key):
    '''
    Assigns the OpenAI API key to the openai.api_key variable
    '''
    openai.api_key_path = path_to_api_key

def get_metadata(accession):
    '''
    Retrieves the GEO metadata XML file for the given accession number

    Parameters
    ----------
    accession : str
        GEO accession number

    Returns 
    -------
    metadata : str
        GEO metadata XML file
    '''
    Entrez.email = "riboseq@gmail.com"
    handle = Entrez.esearch(db="gds", term=accession)
    record = Entrez.read(handle)
    handle.close()
    gds_id = record['IdList'][0]
    handle = Entrez.esummary(db="gds", id=gds_id)
    record = Entrez.read(handle)
    handle.close()

    return record



def main(args):
    assign_openai_key(args.path_to_api_key)
    metadata = get_metadata(args.accession)
    COMPLETIONS_MODEL = "text-davinci-003"

    metadata_prompt = str(metadata) + "\n\n"
    metadata_prompt += "GEO Accession: " + args.accession + "\n\n"
    metadata_prompt += "Fill out the following fields with the appropriate information as brief and accurate as possible. If you do not know the answer to a question, type 'unknown'.\n\n"
    metadata_prompt += "Title: "
    metadata_prompt += "Summary: "
    metadata_prompt += "Number of Samples: "
    metadata_prompt += "Sample Accession Numbers and Titles: "
    metadata_prompt += "Pubmed ID: "
    metadata_prompt += "Publication Date: "
    metadata_prompt += "Organism: "

    response = openai.Completion.create(
        prompt=metadata_prompt,
        temperature=0,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        model=COMPLETIONS_MODEL
    )["choices"][0]["text"].strip(" \n")

    print(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Reads in a GEO Metadata XML file and fills out various database fields outputting a YAML file')
    parser.add_argument('-a', '--accession', help='GEO accession number', required=True)
    parser.add_argument('-o', '--output_file', help='Output file name', required=True)
    parser.add_argument('-p', '--path_to_api_key', default="api_key.txt" , help='Path to OpenAI API key', required=False)
    args = parser.parse_args()
    assign_openai_key(args.path_to_api_key)

    main(args)