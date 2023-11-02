"""Frontend for Ovilo project."""

import time

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Ovilo - Language Learning Platform",
    initial_sidebar_state="expanded",
    menu_items={
        # "Get Help": "https://www.apps.adao.tech"
    },
)


@st.cache_data
def read_flashcards_from_gs(gs_id="1ZCnJV1Lt_nD_nWTukv7u0tjOIFJbSse3fu-Jk4u8fOQ"):
    """Reads flashcards data from a Google Sheets document.

    Parameters:
        gs_id (str): Google Sheets document ID.

    Returns:
        pd.DataFrame: DataFrame containing flashcards data.
    """
    try:
        url = f"https://docs.google.com/spreadsheets/d/{gs_id}/gviz/tq?tqx=out:csv"
        df = pd.read_csv(url)
        df.dropna(subset=["dutch_word", "english_word"], inplace=True)
        return df
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {str(e)}")
        return pd.DataFrame()


# @st.cache_data
# def read_flashcards_from_gs(gs_id="1ZCnJV1Lt_nD_nWTukv7u0tjOIFJbSse3fu-Jk4u8fOQ"):
#    with st.spinner(f"Loading s/s from Google Sheets:"):
#        url = f"http://docs.google.com/spreadsheets/d/{gs_id}/gviz/tq?tqx=out:csv"
#        df = pd.read_csv(url)
#        df.dropna(
#            axis=0, how="any", inplace=True, subset=["dutch_word", "english_word"]
#        )

#    return df


def draw_random_card(flashcards, tail_cards=10):
    """
    Draws a random flashcard from the flashcards DataFrame.

    Parameters:
        flashcards (pd.DataFrame): DataFrame containing flashcards data.
        tail_cards (int, optional): Number of tail cards to consider for random selection. Default is 1.

    Returns:
        pd.Series: Randomly selected flashcard as a Pandas Series.
        int: Index of the selected flashcard.
    """
    try:
        if flashcards.empty:
            return pd.Series(), -1  # Handle the case where the DataFrame is empty.

        if tail_cards <= 0:
            raise ValueError("tail_cards should be a positive integer.")

        card_idx = np.random.randint(
            max(0, flashcards.shape[0] - tail_cards), flashcards.shape[0]
        )
        card = flashcards.iloc[card_idx, :]
        return card, card_idx
    except Exception as e:
        # Handle other exceptions and provide an informative error message
        return pd.Series(), -1, str(e)


def markdown_table(word_1, word_2):
    """
    Generate a Markdown table with two words.

    Parameters:
        word_1 (str): The first word to display.
        word_2 (str): The second word to display.

    Returns:
        str: A Markdown-formatted table.
    """
    table = f"""\
| Word to learn | Word translated |
| ------------- | --------------- |
| {word_1}      | {word_2}        |
"""
    return table


# def draw_random_card(cards, tail):
#    card_idx = flashcards.shape[0] - np.random.randint(tail_cards) - 1
#    random_0_1 = np.random.choice([0, 1])
#    card = flashcards.iloc[card_idx, :].T
#    return card, card_idx


HIDE_STREAMLIT_STYLE = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)


def main():
    # hide_streamlit_style = """
    # <style>
    ##MainMenu {visibility: hidden;}
    # footer {visibility: hidden;}
    # </style>

    # Set up ###
    logo_loc = "./static/ADAO_logo.png"

    with st.sidebar:
        st.image(image=logo_loc, width=300)
        st.markdown("---")
        if st.button("Play again!"):
            st.session_state["play_game"] = True
        st.markdown("---")
        tail_cards = st.slider("Tail cards", 1, 200, 50)
        total_cards = st.slider("Total cards", 1, 50, 10)
        sleep_seconds = st.slider("Sleep 1/10 seconds", 0, 50, 15) / 10.0
        st.markdown("---")
        st.write(
            """### Contact

- Form: [Contact form](https://docs.google.com/forms/d/e/1FAIpQLSeuMiVF7f0XVMQ8C-9jntlQU_lBzX0J5dymg1yLt7Y0QxUN_Q/viewform?usp=sf_link)

- Email: <contact@adao.tech>

            """
        )

    # Main ###
    st.title("Ovilo - Language Learning Platform")

    st.markdown("## Flashcard game")
    flashcards = read_flashcards_from_gs()

    if st.session_state.get("play_game", False):
        game_status = st.progress(0, text="Game progress")
        pl = st.empty()
        card_idx_lst = []
        for idx in range(total_cards):
            game_status.progress(
                (idx + 1) / total_cards, text=f"Game progress - {idx+1} / {total_cards}"
            )
            card, card_idx = draw_random_card(flashcards, tail_cards)
            word_original = card["dutch_word"]
            word_translated = card["english_word"]

            pl.markdown(markdown_table(word_original, ""))
            time.sleep(sleep_seconds)
            pl.markdown(markdown_table(word_original, word_translated))
            time.sleep(sleep_seconds)

            card_idx_lst.append(card_idx)
            st.session_state["play_game"] = False

        st.markdown("---")
        cols_1, cols_2 = st.columns(2)
        with cols_1:
            st.write("## Words learned")
            st.data_editor(flashcards.iloc[card_idx_lst])
        with cols_2:
            st.write("## Words loaded")
            st.data_editor(flashcards)

    else:
        if st.button("Play game!"):
            st.session_state["play_game"] = True
    ## Main - Closure
    st.markdown("---")

    st.write(
        """### Disclaimer
    This software is presented "as-is" and the user accepts this condition
    before using it.  In its current form it is a Demo and no representation is
    given as to performance nor compliance. Also, no warranties are offered as
    to the software's functionality. The software can be used for demonstration
    purposes only. 

    The software is subject to copyrights and no license is offered as part of
    the demonstration offered here. Users are solely responsible for damages of
    any kind that may ensue from using this software in any way beyond this
    demonstration."""
    )


if __name__ == "__main__":
    main()
