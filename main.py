import streamlit as st
from wotd import previous_WOTD, WORD, list_of_word_variants
from PIL import Image
import os

def display_word_of_the_day():
    favored = 0
    st.header("Word of the Day", divider="rainbow")
    st.title(WORD)
    st.markdown(f'**{list_of_word_variants[favored].type_of_speech}**')

def split_text(text):
    return text.split('^')

def format_definition(iteration):
    return split_text(list_of_word_variants[iteration].definition)

def display_definitions():
    favored = 0
    formatted_definition = format_definition(favored)
    st.write('\n'.join(formatted_definition))
    st.markdown(f'**Date first used: {list_of_word_variants[favored].date}**')
    st.markdown(f'Synonyms: {list_of_word_variants[favored].synonyms}')
    st.markdown(f'Antonyms: {list_of_word_variants[favored].antonyms}')

def display_more_definitions():
    for t in range(1, len(list_of_word_variants)):
        if list_of_word_variants[t].definition != 'No info available':
            st.header(WORD, divider="rainbow")
            st.markdown(f'{format_definition(t)}')
            st.markdown(f'**{list_of_word_variants[t].type_of_speech}**')
            st.markdown(f'Etymology: {list_of_word_variants[t].etymology}')
            st.markdown(f'Date first used: {list_of_word_variants[t].date}')
            st.markdown(f'Synonyms: {list_of_word_variants[t].synonyms}')
            st.markdown(f'Antonyms: None found')

def display_instructions():
    st.sidebar.markdown('Instructions on how to make WOTD into a widget on your homescreen.')
    st.sidebar.markdown('Safari Instructions: [Here](https://docs.google.com/presentation/d/1ICISEQxe1UuQ7Z3xBA9gU8fPLrTMFCbIZSy9M_au0HY/edit?usp=sharing)')
    st.sidebar.markdown('Chrome instructions: [Here](https://docs.google.com/presentation/d/1B5HWIi_X_8wNhbKWEcTfKhnWs4DfLsemZEEiym612Y8/edit?usp=sharing)')

def check_for_no_data(text):
    return text == 'No info available'

def guide_func():
    display_word_of_the_day()
    display_definitions()

    st.sidebar.title(WORD)
    st.sidebar.markdown(f'**{list_of_word_variants[0].type_of_speech}**')

    if check_for_no_data(list_of_word_variants[0].etymology):
        if st.sidebar.button("Etymology"):
            st.sidebar.markdown('\n'.join(split_text(list_of_word_variants[0].etymology)))

    if check_for_no_data(list_of_word_variants[0].synonyms):
        if st.sidebar.button('Thesaurus'):
            st.sidebar.markdown("Synonyms:")
            st.sidebar.markdown(list_of_word_variants[0].synonyms)
            st.sidebar.markdown("Antonyms:")
            st.sidebar.markdown(list_of_word_variants[0].antonyms)

    if len(list_of_word_variants) > 1 and check_for_no_data(list_of_word_variants[1].definition):
        if st.button("All Definitions"):
            display_more_definitions()

    url = f'https://www.merriam-webster.com/dictionary/{WORD}'
    st.sidebar.link_button("Merriam-Webster", url)

    if st.sidebar.button("Instructions to add WOTD to your homescreen"):
        display_instructions()

    if st.sidebar.button('Previous words of the day.'):
        for word in previous_WOTD:
            st.sidebar.markdown(word)


def pull_specific_photo(folder_path, photo_name):
    # Default case (equivalent to else)
    photo_path = os.path.join(folder_path, photo_name)
    if os.path.exists(photo_path):
        return Image.open(photo_path)
    else:
        raise FileNotFoundError(f"The photo '{photo_name}' does not exist in the specified folder.")

def display_photo():
    today_photo = pull_specific_photo(r"Photos", f"{WORD}.jpg")
    st.image(today_photo)

guide_func()
display_photo()