import json
import pickle
import re
import requests
import os

WORD = 'brinkmanship'
other_word = 'aver'
REF_DICTIONARY = "collegiate"
REF_THESAURUS = "thesaurus"
DICTIONARY_KEY = 'f45f1248-4774-4d20-8d31-ecb2d70452e0'
Thesaurus_key = '2431331e-690c-4d83-96ac-1f4e9cb350d5'
DEFINITION_KEY = 'shortdef'
TYPE_OF_SPEECH_KEY = 'fl'
DATE_KEY = 'date'
ETYMOLOGY_KEY = 'et'
SYNONYMS = 'syns'
ANTONYMS = 'ants'
NONE_RESULT = 'No info available'
PHOTO_FOLDER = r"Photos"
TXT_FOLDER = 'txt_files'

def get_response_dictionary(ref, word, key):
    url = f"https://www.dictionaryapi.com/api/v3/references/{ref}/json/{word}?key={key}"
    response = requests.get(url)
    print(url)
    return response.json()

def get_data(word_selected):
    data = get_response_dictionary(REF_DICTIONARY, word_selected, DICTIONARY_KEY)
    return data

def get_thes_data(word_selected):
    thes_data = get_response_dictionary(REF_THESAURUS, word_selected, Thesaurus_key)
    return thes_data

def save_to_file(chosen_word):
    file_name = f'{chosen_word}.txt'
    try:
        if os.path.exists(file_name):
            with open(file_name, "w") as f:
                f.write(json.dumps(get_data(chosen_word)))

    except ValueError:
        print("Error", "Something went wrong.")

def read_data(chosen_word):
    file_name = f'{chosen_word}.txt'
    try:
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                new_data = json.loads(f.read())
                return new_data

    except ValueError:
       print("Error", "Something went wrong.")


def editable_list_manager(data,need):
    need_list = []
    for item in data:
        new_item = item.get(need)
        need_list.append(new_item)

    return need_list
p = editable_list_manager(read_data(WORD), DATE_KEY)
print(p)


# def list_photo_names(folder_path):
#     return [file for file in os.listdir(folder_path) if
#             file.endswith(('.jpg', '.webp', '.avif', '.jpeg', '.png', '.gif'))]
#
# def list_of_prev_wotd_cleaner(clean_text):
#     print(clean_text)
#     clean_text = str(clean_text)
#     clean_text = re.sub(r'.jpg', '', clean_text)
#     clean_text = re.sub(r'.jpeg', '', clean_text)
#     clean_text = re.sub(r'.png', '', clean_text)
#     clean_text = re.sub(r'.gif', '', clean_text)
#     clean_text = re.sub(r'.webp', '', clean_text)
#     clean_text = re.sub(r'.avif', '', clean_text)
#     clean_text = re.sub(r"[\#[/@<>{}=~|?]", '', clean_text)
#     clean_text = re.sub(r"]", '', clean_text)
#     clean_text = re.sub(r"'", '', clean_text)
#     clean_text = re.sub(r"2", '', clean_text)
#     clean_text = clean_text.lower()
#     clean_list = clean_text.split(", ")
#     clean_list.sort(key=str.lower)
#     print(clean_list)
#     print('')
#     print(len(clean_list))
#     return clean_list
#
#
# # Example usage
#
previous_WOTD = list_of_prev_wotd_cleaner(list_photo_names(PHOTO_FOLDER))
#
# def all_words(word):
#     for t in (previous_WOTD):
#         save_to_file(t)
#
#
# all_words(previous_WOTD)
file_name = "Former Words of the day"

def adding_a_new_word():
    new_word = input("What's the word for today? ")
    adding_a_new_word_to_list(new_word)
    return new_word

def adding_a_new_word_to_list(new_word):
    try:
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                words_list = json.loads(f.read())
        words_list.append(new_word)
        with open(file_name, "w") as f:
            f.write(json.dumps(words_list))

    except ValueError:
        messagebox.showerror("Error", "Something went wrong.")

    return words_list

new_word = adding_a_new_word()