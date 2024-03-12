import streamlit as st
import time

progress_text = "Operation in progress. Please wait."
percent_complete = 0

my_bar = st.progress(0, text=progress_text)
time.sleep(2)
my_bar.progress(percent_complete+50, text = "loading extra stuff")
time.sleep(2)
