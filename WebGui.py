import Practice as pt
import pandas as pd
import streamlit as st
from streamlit import session_state as ss

st.title("Welcome to Declension Practice!")
st.write("Use this to practice Russian nouns and adjectives in Nominative, Locative, and Genitive forms!")

def reset():
    ss.change_mode = True
    ss.mode = None

def add():
    try:
        with ss.body:
            ss.nouns, ss.adjectives, ss.verbs = pt.add_word(ss.word.lower(),ss.nouns,ss.adjectives,ss.verbs)
            st.button("Return", on_click = reset, type="primary")
            st.success(f"Added {ss.word.lower()}")
            st.text_input("Type word and press [ENTER] to add", placeholder = "Word to add:", label_visibility="visible", key = "word", on_change=add)
    except:
        with ss.body:
            st.button("Return", on_click = reset, type="primary")
            st.error("Could not find word in dictionary. Maybe there was a typo? Please try again")
            st.text_input("Type word and press [ENTER] to add", placeholder = "Word to add:", label_visibility="visible", key = "word", on_change=add)

def practice_gui():
    with ss.body:
        st.button("Return", on_click = reset, type="primary")
        noun, adjective, plurality, ss.n_series, ss.n_index, ss.a_series, ss.a_index = pt.practice_round(ss.form, ss.nouns, ss.adjectives, lambda x, y: x and y)
        st.text_input(f'Please Decline in the {ss.form} Form:\t Noun: {noun}\t Adjective: {adjective}\t Plurality: {plurality}', key = "user_declined", on_change=check)

def check():
    with ss.body:
        st.button("Return", on_click = reset, type="primary")
        st.write(f"You entered: {ss.user_declined}")
        st.write(f"Correct declension: {ss.n_series[ss.n_index]}\t{ss.a_series[ss.a_index]}")
        st.button("Continue", on_click = practice_gui)

def upload():
    with ss.body:
        try:
            st.button("Return", on_click = reset, type="primary")
            pt.upload(ss.file, ss.nouns,ss.adjectives, ss.verbs)
            st.success("Uploaded!")
        except:
            st.button("Return", on_click = reset, type="primary")
            st.error("Sorry, that didn't work! :(\n Try again?")
            st.file_uploader("Select text file to upload:", type="txt", accept_multiple_files=False, key = "file", on_change=upload)

def go_mode():
    if ss.mode != None:
        with ss.body:
            ss.change_mode = False
            st.button("Return", on_click = reset, type="primary")
            match mode:
                case "1. add word":
                    st.text_input("Type word and press [ENTER] to add", placeholder = "Word to add:", label_visibility="visible", key = "word", on_change=add)
                    st.write(ss.word)
                            
                case "2. view word lists":
                    st.subheader("Nouns:")
                    st.write(ss.nouns)
                    st.subheader("Adjectives:")
                    st.write(ss.adjectives)
                    st.subheader("Verbs:")
                    st.write(ss.verbs)
                case "3. practice nominative form":
                    ss.form = "Nominative"
                    noun, adjective, plurality, ss.n_series, ss.n_index, ss.a_series, ss.a_index = pt.practice_round(ss.form, ss.nouns, ss.adjectives, lambda x, y: x and y)
                    st.text_input(f'Please Decline in the {ss.form} Form:\t Noun: {noun}\t Adjective: {adjective}\t Plurality: {plurality}', key = "user_declined", on_change=check)
                case "4. practice locative form":
                    ss.form = "Locative"
                    noun, adjective, plurality, ss.n_series, ss.n_index, ss.a_series, ss.a_index = pt.practice_round(ss.form, ss.nouns, ss.adjectives, lambda x, y: x and y)
                    st.text_input(f'Please Decline in the {ss.form} Form:\t Noun: {noun}\t Adjective: {adjective}\t Plurality: {plurality}', key = "user_declined", on_change=check)
                case "5. practice genitive form":
                    ss.form = "Genitive"
                    noun, adjective, plurality, ss.n_series, ss.n_index, ss.a_series, ss.a_index = pt.practice_round(ss.form, ss.nouns, ss.adjectives, lambda x, y: x and y)
                    st.text_input(f'Please Decline in the {ss.form} Form:\t Noun: {noun}\t Adjective: {adjective}\t Plurality: {plurality}', key = "user_declined", on_change=check)
                case "6. save tables":
                    try:
                        pt.save(ss.nouns, ss.adjectives, ss.verbs)
                        st.success("Saved!")
                    except:
                        st.error("Could not save")
                case "7. add words from text file":
                    st.file_uploader("Select text file to upload:", type="txt", accept_multiple_files=False, key = "file", on_change=upload)

            
    

if "change_mode" not in ss:
    ss.change_mode = True
    ss.nouns = pd.read_csv("Nouns.csv")
    ss.adjectives = pd.read_csv("Adjectives.csv")
    ss.verbs = pd.read_csv("Verbs.csv")

ss.top = st.container()
ss.body = st.container()

with ss.top:
    col_mod, col_but = st.columns([.8,.2])
    with col_mod:
        mode = st.selectbox("What would you like to do?",
            ["1. add word",
            "2. view word lists",
            "3. practice nominative form",
            "4. practice locative form",
            "5. practice genitive form",
            "6. save tables",
            "7. add words from text file"], 
            index=None,
            placeholder = "Select mode...",
            disabled = not(ss.change_mode),
            label_visibility = "collapsed",
            key = "mode"
            )
    with col_but:
        go = st.button("Go!", type="primary", on_click = go_mode, disabled=not(ss.change_mode))

