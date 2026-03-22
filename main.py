import streamlit as st
from wotd import previous_WOTD
from wotd import WORD
from PIL import Image
from wotd import create_variants
import os


def compile_data(chosen_word):
    list_of_word_variants= create_variants(chosen_word)
    return list_of_word_variants

list_of_word_variants = compile_data(WORD)

favored = 0
num = len(list_of_word_variants)


def format_text(text):
    text = text.split('^')
    return text


def check_for_no_data(text):
    if text != 'No info available':
        return True

    else:
        return False


def top_of_page(chosen_word):
    st.header("Word of the Day", divider="rainbow")
    st.title(chosen_word)
    st.markdown(f'**{chosen_word[favored].type_of_speech}**')


def first_definition(chosen_word):
    formated_definition = format_text(chosen_word[favored].definition)
    for t in range(len(formated_definition)):
        st.write(
            f'{formated_definition[t]}')


def pull_specific_file(folder_path, file_name):
    # Default case (equivalent to else)
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_path):
        return Image.open(file_path)
    else:
        raise FileNotFoundError(f"The photo '{file_name}' does not exist in the specified folder.")


def display_photo(chosen_word):
    today_photo = pull_specific_file(r"Photos", f"{chosen_word}.jpg")
    st.image(today_photo)


def new_word():
    if st.sidebar.button('Previous words of the day.'):
        for t in range(len(previous_WOTD)):
            if st.sidebar.button(previous_WOTD[t]):
                chosen_word = previous_WOTD[t]
                return chosen_word


def guide_func(chosen_word):
    num = len(list_of_word_variants)
    top_of_page(chosen_word)
    first_definition(chosen_word)
    display_photo(chosen_word)


if __name__ == "__main__":
    guide_func()
    display_photo()
    new_word()