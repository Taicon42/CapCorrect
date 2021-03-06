"""Import files and import/install necessary libraries"""
import preparation_functions as pf
import error_detection_functions as edf
import error_correction_functions as ecf
import exporting_functions as ef
import os

# pip install transformers

# pip install grammarbot


"""Main for Caption Correction

Slightly altered for testing purposes, specifically addition of 'final_error_total' and 'sentence_error_total'.
The detect_errors() and update_error_message() functions are altered to return these values.
"""
# Get filename
# filename = "GenerateSRT.txt"
filename = input("What is the name of the file you want to correct? \n")
allow_profanity = True

if os.path.exists(filename):
    # Setup functions
    text_list, timestamps = pf.get_file(filename)
    client = pf.initialize_api()
    sentences = pf.print_sentences(text_list)
    suggestion_num = 5
    final_error_total = 0

    # Setup dictionary list
    dictionary_list = []

    # Main/Full error correction process
    for i, token in enumerate(sentences):
        sequence_switched, end_matches, offset_list, err_message, sentence_error_total = \
            edf.detect_errors(str(sentences[i]), client, allow_profanity)

        final_error_total += sentence_error_total

        suggestion_list = ecf.replace_errors(suggestion_num, sequence_switched, end_matches, offset_list)

        # Create readout and dictionary objects
        result = ef.print_readout(suggestion_list, err_message, sequence_switched)
        dictionary = ef.create_dictionary(timestamps[i], sentences[i], sequence_switched, err_message, suggestion_list)
        dictionary_list.append(dictionary)
        print(result)

    print(final_error_total)
    print(dictionary_list)

else:
    print("File couldn't be found.")
