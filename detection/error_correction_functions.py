"""Functions for the Error-replacing Portion

Functions that are responsible for the process of generating possible corrections, swapping out mask tokens
with the corrections, and returning the new sentence list.
"""
import error_detection_functions as edf
import torch



def initialize_suggestion_list(suggestion_num):
    """Function for Initializing suggestion_list

    Simply creates an empty list of size "suggestion_num" and returns it
    """
    y = 0
    suggestion_list = []
    while y < suggestion_num:
        suggestion_list.append("")
        y += 1
    return suggestion_list


def section_decision(indexer, sentence, offset_list, end_matches):
    """Decides what section mask token is in

    Returns a specific section of the sentence given which error is being worked on by splitting the text
    at the offset given in the offset_list.
    """
    if indexer == 0:
        # First section:
        mask_str = sentence[:offset_list[indexer]]

    elif indexer == (len(end_matches) - 1):
        # The last section:
        mask_str = sentence[offset_list[indexer - 1]:]

    else:
        # Any middle sections:
        mask_str = sentence[offset_list[indexer - 1]:offset_list[indexer]]

    return mask_str


def get_top_tokens(sequence_switched, indexer, tokenizer, model, suggestion_num):
    """Generates the suggestions for the error"""
    token_input = tokenizer.encode(sequence_switched, return_tensors="pt")
    mask_token_index = torch.where(token_input == tokenizer.mask_token_id)[1]
    token_logits = model(token_input).logits
    mask_token_logits = token_logits[0, mask_token_index, :]
    top_tokens = torch.topk(mask_token_logits, suggestion_num, dim=1).indices[indexer].tolist()
    return top_tokens


def replace_tokens(the_string, sequence_switched, suggestion_list, indexer, tokenizer, model, suggestion_num):
    """Replaces tokens with suggestions stored in the suggestion list"""
    # Get top tokens
    top_tokens = get_top_tokens(sequence_switched, indexer, tokenizer, model, suggestion_num)

    iterator = 0
    for token in top_tokens:
        suggestion_list[iterator] += the_string.replace(tokenizer.mask_token, tokenizer.decode([token]))
        iterator += 1

    return suggestion_list


def replace_errors(suggestion_num, sequence_switched, end_matches, offset_list):
    """Main Function for Error-replacing Process

    Loops through the process to replace all errors in the sentence.  Returns string list containing the new
    sentences with possible corrections.
    """
    if len(end_matches) != 0:
        # Initialize Variables
        new_list = initialize_suggestion_list(suggestion_num)
        tokenizer, model = edf.initialize_tokenizer_variables()

        # Swapping masks with corrections section
        if len(end_matches) > 1:
            k = 0
            j = 0
            current = 0
            keep_going = True

            while keep_going:
                # Determine what section to locate mask token in
                mask_str = section_decision(j, sequence_switched, offset_list, end_matches)

                new_list = replace_tokens(mask_str, sequence_switched, new_list, j, tokenizer, model, suggestion_num)

                # If end of sentence, return j to 0, else continue iterations
                if j == (len(end_matches) - 1):
                    # Update variables
                    j = 0
                    current += 1
                    keep_going = False

                else:
                    j += 1

                k += 1

        else:
            new_list = replace_tokens(sequence_switched, sequence_switched, new_list, 0, tokenizer, model,
                                      suggestion_num)

        return new_list

    else:
        return []
