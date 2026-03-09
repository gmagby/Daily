import re
import requests
import os

WORD = 'dialectic'
REF_DICTIONARY = "collegiate"
REF_THESAURUS = "thesaurus"
DICTIONARY_KEY = 'f45f1248-4774-4d20-8d31-ecb2d70452e0'
THESAURUS_KEY = '2431331e-690c-4d83-96ac-1f4e9cb350d5'
DEFINITION_KEY = 'shortdef'
TYPE_OF_SPEECH_KEY = 'fl'
DATE_KEY = 'date'
ETYMOLOGY_KEY = 'et'
SYNONYMS = 'syns'
ANTONYMS = 'ants'
NONE_RESULT = 'No info available'
FILE_NAME = "Former Words of the day"


def get_response_dictionary(ref, word, key):
    url = f"https://www.dictionaryapi.com/api/v3/references/{ref}/json/{word}?key={key}"
    response = requests.get(url)
    print(url)
    return response.json()


def cleaner(clean_text, sharp=None):
    print(clean_text)
    clean_text = str(clean_text)
    patterns = [
        (r"{mat", ''),
        (r"bc}", ''),
        (r"ma}", ''),
        (r"dx}", ''),
        (r'it}', ''),
        (r"'text', ", ''),
        (r']]', ''),
        (r"et_link", ''),
        (r":[12]", ''),
        (r"-ia", ''),
        (r"et_snote',", ''),
        (r"'t',", ''),
        (r"\s+", " "),
        (r"[\#[/@<>{}=~|?]", ''),
        (r"et_snote", ''),
        (r"]", ''),
        (r"andor", 'and/or'),
        (r" u ", " 'u' "),
        (fr"{WORD}{WORD}", fr"{WORD}")
    ]

    for pattern, replacement in patterns:
        clean_text = re.sub(pattern, replacement, clean_text)

    if sharp == 3:
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
    elif sharp == 2:
        clean_text = re.sub(r'dst2|ds1a|dst|ds1b|ds3|dx_ety|dxt|dsi1|ds1|ds2|\.jpg|\.jpeg|\.png|\.gif', '', clean_text)
    elif sharp == 1:
        clean_text = re.sub(r"', '", '^', clean_text)
    clean_text = re.sub(r"'", '', clean_text)
    clean_text = re.sub(r"\s+", " ", clean_text).strip()
    print(clean_text)
    print(" ")
    return clean_text


def list_manager(data, syntax, sharp=None):
    return [
        cleaner(item.get(syntax, NONE_RESULT), sharp) if item.get(syntax) else NONE_RESULT
        for item in data
    ]


def extract_synonyms(data, nyms):
    return [
        [syn for syn_group in entry['meta'].get(nyms, []) for syn in syn_group] or []
        for entry in data
    ]


data = get_response_dictionary(REF_DICTIONARY, WORD, DICTIONARY_KEY)
thes_data = get_response_dictionary(REF_THESAURUS, WORD, THESAURUS_KEY)

definition_list = list_manager(data, DEFINITION_KEY, sharp=1)
date_list = list_manager(data, DATE_KEY, sharp=2)
etymology_list = list_manager(data, ETYMOLOGY_KEY, sharp=3)
type_of_speech_list = list_manager(data, TYPE_OF_SPEECH_KEY)

synonyms_list = extract_synonyms(thes_data, SYNONYMS) if thes_data else NONE_RESULT
antonyms_list = extract_synonyms(thes_data, ANTONYMS) if thes_data else NONE_RESULT


class WordVariant:
    def __init__(self, definition, type_of_speech, date, etymology, synonyms=None, antonyms=None):
        self.definition = definition
        self.type_of_speech = type_of_speech
        self.date = date
        self.etymology = etymology
        self.synonyms = synonyms
        self.antonyms = antonyms


def create_word_variants(definitions, types_of_speech, dates, etymologies, synonyms=None, antonyms=None):
    max_length = max(len(definitions), len(types_of_speech), len(dates), len(etymologies),
                     len(synonyms) if synonyms else 0, len(antonyms) if antonyms else 0)

    word_variants = []

    for i in range(max_length):
        definition = definitions[i] if i < len(definitions) else None
        type_of_speech = types_of_speech[i] if i < len(types_of_speech) else None
        date = dates[i] if i < len(dates) else None
        etymology = etymologies[i] if i < len(etymologies) else None
        synonym = synonyms[i] if synonyms and i < len(synonyms) else None
        antonym = antonyms[i] if antonyms and i < len(antonyms) else None

        word_variants.append(WordVariant(definition, type_of_speech, date, etymology, synonym, antonym))

    return word_variants


list_of_word_variants = create_word_variants(definition_list, type_of_speech_list, date_list, etymology_list,
                                             synonyms_list, antonyms_list)


def split_text(text):
    return text.split('^')


formatted_definition = split_text(list_of_word_variants[0].definition)


def first_definition():
    print("Formatted Definition:")
    for item in formatted_definition:
        print(item)
    print(f'Date first used: {list_of_word_variants[0].date}')
    print(" ")
    print(f'Amount of items in Format: {len(formatted_definition)}')


first_definition()
print(f'Number of variants: {len(list_of_word_variants)}')
print(" ")
print(f'Synonyms List: {synonyms_list}')
print(f'Antonyms List: {antonyms_list}')
print('')


def list_photo_names(folder_path):
    return [file for file in os.listdir(folder_path) if
            file.endswith(('.jpg', '.webp', '.avif', '.jpeg', '.png', '.gif'))]


def list_of_prev_wotd_cleaner(clean_text):
    print(clean_text)
    clean_text = str(clean_text)
    clean_text = re.sub(r'\.(jpg|jpeg|png|gif|webp|avif)', '', clean_text)
    clean_text = re.sub(r"[\#[/@<>{}=~|?]", '', clean_text)
    clean_text = re.sub(r"]", '', clean_text)
    clean_text = re.sub(r"'", '', clean_text)
    clean_text = re.sub(r"2", '', clean_text)
    clean_list = clean_text.split(", ")
    clean_list.sort(key=str.lower)
    print(clean_list)
    return clean_list


# Example usage
photo_folder = r"Photos"
previous_WOTD = list_of_prev_wotd_cleaner(list_photo_names(photo_folder))