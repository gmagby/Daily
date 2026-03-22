import streamlit as st
from wotd import previous_WOTD
from wotd import WORD
from PIL import Image
from wotd import create_variants
import os

def main():
    def compile_data(chosen_word):
        list_of_word_variants= create_variants(chosen_word)
        return list_of_word_variants

    list_of_word_variants = compile_data(WORD)

    favored = 0
    num = len(list_of_word_variants)


    def top_of_page(chosen_word):
        st.header("Word of the Day", divider="rainbow")
        st.title(chosen_word)
        st.markdown(f'**{compile_data(chosen_word)[favored].type_of_speech}**')


    # Text to List Converter
    def format_text(text):
        text = text.split('^')
        return text

    def check_for_no_data(text):
        if text != 'No info available':
            return True

        else:
            return False

    def display_photo(chosen_word):
        today_photo = pull_specific_photo(r"Photos", f"{chosen_word}.jpg")
        st.image(today_photo)

    def first_definition(chosen_word):
        formated_definition = format_text(list_of_word_variants[favored].definition)
        for t in range(len(formated_definition)):
            st.write(
                f'{formated_definition[t]}')
        # st.markdown(f'Synonyms: {list_of_word_variants[0].synonyms}')
        # st.markdown(f'Antonyms: {list_of_word_variants[0].antonyms}')

    def more_definitions(chosen_word):
        for t in range(num - 1):
            if check_for_no_data(list_of_word_variants[t].definition):
                pass

            st.header(chosen_word, divider="rainbow")
            st.markdown(
                f'{format_text(list_of_word_variants[t + 1].definition)}')
            st.markdown(
                f'**{list_of_word_variants[t + 1].type_of_speech}**')
            st.markdown(f'Etymology: {format_text(list_of_word_variants[t + 1].etymology)}')
            st.markdown(
                f'Date first used: {list_of_word_variants[t + 1].date}')
            if check_for_no_data(list_of_word_variants[t + 1].synonyms):
                st.markdown("Synonyms:")
                st.markdown(list_of_word_variants[t + 1].synonyms)
                st.markdown("Antonyms:")
                st.markdown(list_of_word_variants[t + 1].antonyms)
            # st.markdown(f'Antonyms: None found')

    def display_instructions():
        st.sidebar.markdown('Instructions on how to make WOTD into a widget on your homescreen.')
        st.sidebar.markdown(
            'Safari Instructions: [Here](https://docs.google.com/presentation/d/1ICISEQxe1UuQ7Z3xBA9gU8fPLrTMFCbIZSy9M_au0HY/edit?usp=sharing)')
        st.sidebar.markdown(
            'Chrome instructions: [Here](https://docs.google.com/presentation/d/1B5HWIi_X_8wNhbKWEcTfKhnWs4DfLsemZEEiym612Y8/edit?usp=sharing)')

    def pull_specific_photo(folder_path, photo_name):
        # Default case (equivalent to else)
        photo_path = os.path.join(folder_path, photo_name)
        if os.path.exists(photo_path):
            return Image.open(photo_path)
        else:
            raise FileNotFoundError(f"The photo '{photo_name}' does not exist in the specified folder.")


    def sidebar(chosen_word):
        st.sidebar.title(chosen_word)
        st.sidebar.markdown(f'**{list_of_word_variants[favored].type_of_speech}**')

        if check_for_no_data(list_of_word_variants[favored].etymology):
            if st.sidebar.button("Etymology"):
                for t in range(num):
                    st.sidebar.markdown(list_of_word_variants[t].etymology)
        else:
            pass

        if check_for_no_data(list_of_word_variants[favored].synonyms):
            if st.sidebar.button('Thesaurus'):
                st.sidebar.markdown("Synonyms:")
                st.sidebar.markdown(list_of_word_variants[favored].synonyms)
                st.sidebar.markdown("Antonyms:")
                st.sidebar.markdown(list_of_word_variants[favored].antonyms)
            else:
                pass
        url = f'https://www.merriam-webster.com/dictionary/{chosen_word}'
        st.sidebar.link_button("Merriam-Webster", url)

        if st.sidebar.button("Instructions to add WOTD to your homescreen"):
            display_instructions()



    def guide_func(chosen_word):
        top_of_page(chosen_word)
        first_definition(chosen_word)
        sidebar(chosen_word)
        if num > 1:
            if check_for_no_data(list_of_word_variants[1].definition):
                if st.button("All Definitions"):
                    more_definitions(chosen_word)
            else:
                pass
        display_photo(WORD)
    def new_word():
        if st.sidebar.button('Previous words of the day.'):
            for t in range(len(previous_WOTD)):
                if st.sidebar.button(previous_WOTD[t]):
                    guide_func(t)

    guide_func(WORD)

    new_word()



if __name__ == "__main__":
    main()