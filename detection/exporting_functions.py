"""Exporting functions

Functions that export the new corrections, along with original data information to display
"""


def print_readout(sugg_list, err_message, sequence_switched):
    """Print Function"""
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


def create_dictionary(timestamp, original_sentence, sequence_switched, err_message, suggestion_list):
    """Create Dictionary Function

    Generates and exports a dictionary object with relevant data for website interaction to take place.
    """
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
