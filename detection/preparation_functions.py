"""Setup Functions

Functions that initialize important libraries, get contents from the imported file, and format the content
for easy usability
"""


def initialize_apis():
    """Initialize APIs Function

    Make sure to enter in a GrammarBot api key to run program
    """
    # nlp = spacy.load("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
    my_api_key = <'insert key here'>
    client = GrammarBotClient(api_key=my_api_key)
    return nlp, client


def get_file(file_name):
    """Main File Receiving Function

    Gets the file and reads the lines.  Calls other functions to split the text up and receives the data.
    Returns text and timestamps
    """
    file_text = open(file_name)
    lines = file_text.readlines()
    file_text.close()
    text = file_read(lines)
    timestamps = get_timestamps(lines)
    return text, timestamps


def file_read(lines):
    """ Function for the file reading process

    Strips file to get ONLY the text; No timestamps or sentence indexes added so returned string is only the
    caption text.
    """
    new_text = ""
    for line in lines:
        if re.search('^[0-9]', line) is None and re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line)\
                is None and re.search(
                '^$', line) is None:
            new_text += ' ' + line.rstrip('\n')
        new_text = new_text.lstrip()
    return new_text


def get_timestamps(lines):
    """ Function for getting the timestamps

    Strips the file to get ONLY the timestamps; No caption text or sentence indexes are added to the list.
    Returns a list of strings.
    """
    timestamps = []
    for line in lines:
        if re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line):
            timestamps.append(line.rstrip('\n'))
    return timestamps


def format_text(nlp, text):
    """Formatting Text Function

    Formats the text string into a list containing individual sentences. Returns this list.
    """
    doc = nlp(text)
    sentences = list(doc.sents)
    for i, token in enumerate(sentences):
        print('Sentence #%d: %s' % (i, token.text))
    return sentences
