import streamlit as st

def set_page_title(title: str, divider: bool = True) -> None:
    """Sets the page title and adds the Metabolic logo to the top of the page.
    Needs to be called at the start of every page."""
    st.set_page_config(page_title=title, layout="wide")
    col1, col2 = st.columns((1, 5))

    with col1:
        st.image("resources/Metabolic_logo.png", width=100)

    with col2:
        st.title(title)

    st.divider() if divider else None