"""Functions for the Error-detecting Portion

Functions responsible for the detection of errors in the text, masking the errors, and returning important
data for the error_detection and exporting_functions to use.
"""
from transformers import AutoModelForMaskedLM, AutoTokenizer


def get_matches(text, client):
    """ Using the GrammarBot API, get matches for errors.

    Returns selected relevant information.
    """
    res = client.check(text)
    j = res.raw_json
    matches = j["matches"]
    end_matches = matches.copy()
    return res, matches, end_matches


def set_tokenizer(tokenizer, model, sequence_switched):
    """Prepares Tokenizer Variables"""
    token_input = tokenizer.encode(sequence_switched, return_tensors="pt")
    mask_token_index = torch.where(token_input == tokenizer.mask_token_id)[1]
    token_logits = model(token_input).logits
    mask_token_logits = token_logits[0, mask_token_index, :]
    top_tokens = torch.topk(mask_token_logits, suggestion_num, dim=1).indices[j].tolist()


def print_header(res):
    """Print Header Function

    Prints a border along with the header with relevant information
    """
    print("------------------------------------------------")
    print("Language: ", res.detected_language)
    print("Completion Status: ", res.result_is_incomplete)


def initialize_outputs():
    """Initialize Output String Variables

    Simply makes empty variables and returns them.
    """
    sequence_switched = ""
    err_message = ""
    indicator_str = ""
    correction_suggestion_str = "Possible corrections: \n"
    return sequence_switched, err_message, indicator_str, correction_suggestion_str


def initialize_traverse_variables():
    """Initialize Variables for Sectioning Out Text

    Creates default variable data, and returns them.
    """
    last_offset = 0
    previous_length = 0
    offset_list = []
    return last_offset, previous_length, offset_list


def initialize_tokenizer_variables():
    """Initialize Tokenizer Variables (and return them)"""
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-cased")
    model = AutoModelForMaskedLM.from_pretrained("distilbert-base-cased", return_dict=True)
    return tokenizer, model


def update_error_message(err_message, match, matches, allow_profanity, i):
    """Update Error Message Function

    Update error message string with the match's error type.  Omits profanity if allowed.
    """
    if match['shortMessage'] == "Profanity":
        if allow_profanity is not True:
            err_message += match['shortMessage'] + ", "
    elif i == (len(matches) - 1):
        err_message += match['shortMessage']
    else:
        err_message += match['shortMessage'] + ", "
    return err_message


def update_traverse_variables(sequence_switched, altering_text, offset, length, last_offset, offset_list,
                              tokenizer):
    """Update Traversing Variables

    """
    sequence_switched += altering_text[last_offset:offset] + f"{tokenizer.mask_token}"
    previous_length = len(sequence_switched)
    last_offset = offset + length
    offset_list.append(previous_length)
    return sequence_switched, last_offset, offset_list


def update_for_profanity(match, allow_profanity, sequence_switched, altering_text, offset, length,
                         last_offset, offset_list, end_matches, tokenizer, i):
    """Profanity Decision Function

    If error type is "Profanity", depending on if profanity has been selected to be allowed, determine if
    variables need to be changed in order to properly ignore error instance.
    """
    if match['shortMessage'] == "Profanity":
        if allow_profanity:
            sequence_switched += altering_text[last_offset:offset+length]
            last_offset = offset + length
            del endMatches[i]
        else:
            sequence_switched, last_offset, offset_list = update_traverse_variables(sequence_switched,
                                                                                    altering_text, offset,
                                                                                    length, last_offset,
                                                                                    offset_list, tokenizer)
    else:
        sequence_switched, last_offset, offset_list = update_traverse_variables(sequence_switched,
                                                                                altering_text, offset,
                                                                                length, last_offset,
                                                                                offset_list, tokenizer)

    return sequence_switched, last_offset, offset_list, end_matches


def detect_errors(text, client, profanity_bool):
    """Main Function for Detection Process

    First calls get_matches to get number of errors detected in the sentence.  Then loops through the
    sentence for an equivalent number to how many errors were detected to obtain the offsets for each error.
    Each loop updates the error message and traversing variables accordingly. Returns the updated string,
    lists with data to traverse the string in the error correction process, and the error message string.
    """
    res, matches, end_matches = get_matches(text, client)
    if len(matches) != 0:
        print_header(res)

        # Initialize Variables
        sequence_switched = ""
        err_message = ""
        altering_text = text
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
            sequence_switched, last_offset, offset_list, end_matches = update_for_profanity(match, allow_profanity,
                                                                                            sequence_switched,
                                                                                            altering_text, offset,
                                                                                            length, last_offset,
                                                                                            offset_list, end_matches,
                                                                                            tokenizer, i)

            # If last of errors, add the rest of the text to the string
            if i == (len(matches) - 1):
                sequence_switched += altering_text[last_offset:]

            # Update the loop variable
            i += 1

        return sequence_switched, end_matches, offset_list, err_message

    else:
        return "", [], [], ""
