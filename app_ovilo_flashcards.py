"""Frontend for Ovilo project."""

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
    with st.spinner(f"Loading s/s from Google Sheets:"):
        url = f"http://docs.google.com/spreadsheets/d/{gs_id}/gviz/tq?tqx=out:csv"
        df = pd.read_csv(url)
        df.dropna(axis=0, how="any", inplace=True)

    return df


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

    # Main ###
    st.title("Ovilo - Language Learning Platform")

    with st.spinner(f"Loading "):
        flashcards = read_flashcards_from_gs()
        # st.write(page_map[page].present())
        st.markdown("## Flashcard game")
        st.button("Draw new card")
        st.text_input("Write the answer")

        # if st.button("Draw card") or card_selected != -1:
        card = flashcards.sample(n=1)

        random_0_1 = np.random.choice([0, 1])
        side_one = card.iloc[0, random_0_1]
        with st.expander(side_one):
            st.write(card)

        st.write("## Flashcard set loaded")
        st.write(flashcards)

    ## Main - Closure
    st.markdown("---")

    st.write(
        """### Contact

- Form: [Contact form](https://docs.google.com/forms/d/e/1FAIpQLSeuMiVF7f0XVMQ8C-9jntlQU_lBzX0J5dymg1yLt7Y0QxUN_Q/viewform?usp=sf_link)

- Email: <contact@adao.tech>

        """
    )

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
