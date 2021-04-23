"""Import files and import/install necessary libraries"""
import preparation_functions as pf
import error_detection_functions as edf
import error_correction_functions as ecf
import exporting_functions as ef


# pip install transformers

# pip install grammarbot

import re
import spacy
import json
import torch

from transformers import pipeline, AutoModelForMaskedLM, AutoTokenizer, AutoModelWithLMHead
from grammarbot import GrammarBotClient


"""Main for Caption Correction"""
# Setup functions
text, timestamps = pf.get_file("GenerateSRT.txt")
nlp, client = pf.initialize_apis()
sentences = pf.format_text(nlp, text)
suggestion_num = 5

# Setup dictionary list
dictionary_list = []

# Main/Full error correction process
for i, token in enumerate(sentences):
    sequence_switched, end_matches, offset_list, err_message = edf.detect_errors(str(sentences[i]), client, False)
    suggestion_list = ecf.replace_errors(suggestion_num, sequence_switched, end_matches, offset_list)

    # Create readout and dictionary objects
    result = ef.print_readout(suggestion_list, err_message, sequence_switched)
    dictionary = ef.create_dictionary(timestamps[i], sentences[i], sequence_switched, err_message, suggestion_list)
    dictionary_list.append(dictionary)
    print(result)

print(dictionary_list)
