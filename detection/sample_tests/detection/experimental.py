"""Experimental Functions

These are prototypes for if we expanded on this project
"""


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
