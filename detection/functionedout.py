# -*- coding: utf-8 -*-
"""functionedOut.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14EOEpUCLQX1P1wZFuPWUl8cvzOXhm2U9

Install
"""

# pip install transformers

# pip install grammarbot

"""Import"""

# from google.colab import files
import re
import spacy
import json
import torch

from transformers import pipeline, AutoModelForMaskedLM, AutoTokenizer, AutoModelWithLMHead
from grammarbot import GrammarBotClient

"""Setup Functions

Initialize APIs Function
"""


def initialize_apis():
    """Maybe not necessary to place in a function"""
    # nlp = spacy.load("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
    my_api_key = '782558b415msh8b5088cb428bca0p1ed60djsn0da2ee6624be'
    client = GrammarBotClient(api_key=my_api_key)
    return nlp, client


"""Main File Receiving Function"""


def get_file(file_name):
    """Function for getting the file and reading the lines"""
    file_text = open("GenerateSRT.txt")
    lines = file_text.readlines()
    file_text.close()
    text = file_read(lines)
    timestamps = get_timestamps(lines)
    return text, timestamps


"""Processing File Function"""


def file_read(lines):
    """Function for the file reading process"""
    new_text = ""
    for line in lines:
        if re.search('^[0-9]', line) is None and re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line) is None and re.search(
                '^$', line) is None:
            new_text += ' ' + line.rstrip('\n')
        new_text = new_text.lstrip()
    return new_text


"Getting Timestamps (New Function)"


def get_timestamps(lines):
    timestamps = []
    for line in lines:
        if re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line):
            timestamps.append(line.rstrip('\n'))
    return timestamps


"""Formatting Text Function"""


def format_text(nlp, text):
    doc = nlp(text)
    sentences = list(doc.sents)
    for i, token in enumerate(sentences):
        print('Sentence #%d: %s' % (i, token.text))
    return sentences


"""Functions for the Error-detecting Portion

Get Matches Function
"""


def get_matches(text, client):
    res = client.check(text)
    j = res.raw_json
    matches = j["matches"]
    endMatches = matches.copy()
    return res, matches, endMatches


"""Preparing Tokenizer Function"""


def set_tokenizer(tokenizer, model, sequence_switched):
    token_input = tokenizer.encode(sequence_switched, return_tensors="pt")
    mask_token_index = torch.where(token_input == tokenizer.mask_token_id)[1]
    token_logits = model(token_input).logits
    mask_token_logits = token_logits[0, mask_token_index, :]
    top_tokens = torch.topk(mask_token_logits, suggestion_num, dim=1).indices[j].tolist()


"""Print Header Function"""


def print_header(res):
    print("------------------------------------------------")
    print("Language: ", res.detected_language)
    print("Completion Status: ", res.result_is_incomplete)


"""Initialize Output String Variables"""


def initialize_outputs():
    sequence_switched = ""
    err_message = ""
    indicator_str = ""
    correction_sugg_str = "Possible corrections: \n"
    return sequence_switched, err_message, indicator_str, correction_sugg_str


"""Initialize Variables for Sectioning Out Text"""


def initialize_traverse_variables():
    last_offset = 0
    previous_length = 0
    offset_list = []
    return last_offset, previous_length, offset_list


"""Initialize Tokenizer Variables"""


def initialize_tokenizer_variables():
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-cased")
    model = AutoModelForMaskedLM.from_pretrained("distilbert-base-cased", return_dict=True)
    return tokenizer, model


"""Update Error Message Function"""


def update_error_message(err_message, match, matches, allowProfanity, i):
    if match['shortMessage'] == "Profanity":
        if allowProfanity != True:
            err_message += match['shortMessage'] + ", "
    elif i == (len(matches) - 1):
        err_message += match['shortMessage']
    else:
        err_message += match['shortMessage'] + ", "
    return err_message


"""Update Traversing Variables"""


def update_traverse_variables(sequence_switched, altering_text, offset, length, last_offset, offset_list, tokenizer):
    sequence_switched += altering_text[last_offset:offset] + f"{tokenizer.mask_token}"
    previous_length = len(sequence_switched)
    last_offset = offset + length
    offset_list.append(previous_length)
    return sequence_switched, last_offset, offset_list


"""Profanity Decision Function"""


def update_for_profanity(match, allow_profanity, sequence_switched, altering_text, offset, length, last_offset, offset_list, endMatches, tokenizer, i):
    if match['shortMessage'] == "Profanity":
        if allow_profanity:
            sequence_switched += altering_text[last_offset:offset+length]
            last_offset = offset + length
            del endMatches[i]
        else:
            sequence_switched, last_offset, offset_list = update_traverse_variables(sequence_switched, altering_text, offset, length, last_offset, offset_list, tokenizer)
    else:
        sequence_switched, last_offset, offset_list = update_traverse_variables(sequence_switched, altering_text, offset, length, last_offset, offset_list, tokenizer)

    return sequence_switched, last_offset, offset_list, endMatches


"""Main Function for Detection Process"""


def detect_errors(text, client, profanity_bool):
    res, matches, endMatches = get_matches(text, client)
    if len(matches) != 0:
        print_header(res)

        # Initialize Variables
        sequence_switched = ""
        err_message = ""
        altering_text = text
        # sequence_switched, err_message, indicator_str, correction_sugg_str = initialize_outputs()
        last_offset, previous_length, offset_list = initialize_traverse_variables()
        tokenizer, model = initialize_tokenizer_variables()
        allow_profanity = profanity_bool

        i = 0

        while i < len(matches):
            match = matches[i]

            # Update error message
            err_message = update_error_message(err_message, match, matches, allow_profanity, i)

            # Update offset variables
            offset = match["offset"]
            length = match["length"]

            # Check on profanity choice
            sequence_switched, last_offset, offset_list, endMatches = update_for_profanity(match, allow_profanity, sequence_switched, altering_text, offset, length, last_offset, offset_list, endMatches, tokenizer, i)

            # If last of errors, add the rest of the text to the string
            if i == (len(matches) - 1):
                sequence_switched += altering_text[last_offset:]

            # Update the loop variable
            i += 1

        return sequence_switched, endMatches, offset_list, err_message

    else:
        return "", [], [], ""


"""Functions for the Error-replacing Portion

Function for Initializing suggestion_list
"""


def initialize_suggestion_list(suggestion_num):
    y = 0
    suggestion_list = []
    while y < suggestion_num:
        suggestion_list.append("")
        y += 1
    return suggestion_list


"""Deciding what section mask token is in"""


def section_decision(j, sequence_switched, offset_list):
    if j == 0:
        # First section:
        mask_str = sequence_switched[:offset_list[j]]

    elif j == (len(endMatches) - 1):
        # The last section:
        mask_str = sequence_switched[offset_list[j - 1]:]

    else:
        # Any middle sections:
        mask_str = sequence_switched[offset_list[j - 1]:offset_list[j]]

    return mask_str


"""Get Top Tokens Function"""


def get_top_tokens(sequence_switched, indexer, tokenizer, model):
    token_input = tokenizer.encode(sequence_switched, return_tensors="pt")
    mask_token_index = torch.where(token_input == tokenizer.mask_token_id)[1]
    token_logits = model(token_input).logits
    mask_token_logits = token_logits[0, mask_token_index, :]
    top_tokens = torch.topk(mask_token_logits, suggestion_num, dim=1).indices[indexer].tolist()
    return top_tokens


"""Replace Tokens Function"""


def replace_tokens(the_string, sequence_switched, suggestion_list, indexer, tokenizer, model):
    # Get top tokens
    top_tokens = get_top_tokens(sequence_switched, indexer, tokenizer, model)

    iterator = 0
    for token in top_tokens:
        suggestion_list[iterator] += the_string.replace(tokenizer.mask_token, tokenizer.decode([token]))
        iterator += 1

    return suggestion_list


"""Main Function for Error-replacing Process"""


def replace_errors(suggestion_num, sequence_switched, endMatches, offset_list):
    if len(endMatches) != 0:
        # Initialize Variables
        new_list = initialize_suggestion_list(suggestion_num)
        tokenizer, model = initialize_tokenizer_variables()

        # Swapping masks with corrections section
        if len(endMatches) > 1:
            k = 0
            j = 0
            current = 0
            keep_going = True

            while keep_going:
                # Determine what section to locate mask token in
                mask_str = section_decision(j, sequence_switched, offset_list)

                new_list = replace_tokens(mask_str, sequence_switched, new_list, j, tokenizer, model)

                # If end of sentence, return j to 0, else continue iterations
                if j == (len(endMatches) - 1):
                    # Update variables
                    j = 0
                    current += 1
                    keep_going = False

                else:
                    j += 1

                k += 1

        else:
            new_list = replace_tokens(sequence_switched, sequence_switched, new_list, 0, tokenizer, model)

        return new_list

    else:
        return []


"""Print Function"""


def print_readout(sugg_list, err_message, sequence_switched):
    if len(sugg_list) != 0:
        final_suggestion_str = "Possible corrections: \n"
        for i in sugg_list:
            final_suggestion_str += i + "\n"
        err_message_str = "Possible error: " + err_message + "\n \n"
        print("\nOriginal with mask: ", sequence_switched)
        return_str = "\n" + err_message_str + final_suggestion_str + "\n------------------------------------------------"
        return return_str

    else:
        no_match = "-------------------No errors found-------------------"
        return no_match


"Create Dictionary Function"


def create_dictionary(timestamp, original_sentence, sequence_switched, err_message, suggestion_list):
    if len(suggestion_list) != 0:
        err_message_str = "Possible error: " + err_message + "\n \n"
        new_dictionary = {
            "timestamp": timestamp,
            "original_sentence": original_sentence,
            "masked_sentence": sequence_switched,
            "err_message": err_message,
            "possible_corrections": suggestion_list
        }
        return new_dictionary

    else:
        return {}


"""
def write_to_file(correction):
    test_file = open("testFile.txt", "a")
    test_file.write(correction)
    test_file.write("\n")
    test_file.close()

    # open and read the file after the appending:
    f = open("testFile.txt", "r")
    print(f.read())
"""

"""Main"""
# Setup functions
text, timestamps = get_file("GenerateSRT.txt")
nlp, client = initialize_apis()
sentences = format_text(nlp, text)
suggestion_num = 5

# Setup dictionary list
dictionary_list = []

# Main/Full error correction process
for i, token in enumerate(sentences):
    sequence_switched, endMatches, offset_list, err_message = detect_errors(str(sentences[i]), client, False)
    suggestion_list = replace_errors(suggestion_num, sequence_switched, endMatches, offset_list)

    # Create readout and dictionary objects
    result = print_readout(suggestion_list, err_message, sequence_switched)
    dictionary = create_dictionary(timestamps[i], sentences[i], sequence_switched, err_message, suggestion_list)
    dictionary_list.append(dictionary)
    print(result)
    """
    # Portion for writing to file
    for j in suggestion_list:
        write_to_file(j)
    """
print(dictionary_list)

"""User Prompt functions"""

"""
def copy_file(original_sentences, file_name, new_file_name):
    # Copy lines into a file of given name
    copied_file = open(new_file_name, "w")
    # origin_file = open(file_name, 'r')
    # new_file_text = origin_file.readlines()
    new_file_text = ""
    for line, _ in enumerate(original_sentences):
        new_file_text += str(original_sentences[line]) + "\n"
    copied_file.writelines(new_file_text)
    copied_file.close()
    # origin_file.close()
    return new_file_text


def find_line_in_file(search_string, file):
    # Find the line that contains the given string and return the index of the line
    line_index = None

    the_file = open(file, 'r')
    for num, line in enumerate(the_file):
        if search_string in line:
            line_index = num
    the_file.close()
    return line_index


def swap_line_with_string(file_name, index, replace_string):
    # Swap the line in the file at given index with the given string
    new_file = open(file_name, "r")
    the_lines = new_file.readlines()
    new_file.close()

    the_lines[index] = replace_string + "\n"

    new_file = open(file_name, "w")
    new_file.writelines(the_lines)
    new_file.close()


def user_prompt():
    # Ask user what string to replace and what to replace with
    to_be_replaced = input("What sentence would you like to replace?\n")
    to_be_replacing = input("What would you like to replace the sentence with?\n")
    return to_be_replaced, to_be_replacing
"""

"""Copying files and replacing lines"""
"""
original_file = "testFile.txt"
next_file = "new_file.txt"
# looking_string = "A second sentence where the error is fauertr in the sentence."
# replacing_string = "A completely new sentence, with all new words to fill up space inside this void."
looking_string, replacing_string = user_prompt()
file_text = copy_file(sentences, original_file, next_file)
index_of_line = find_line_in_file(looking_string, next_file)
swap_line_with_string(next_file, index_of_line, replacing_string)
"""
