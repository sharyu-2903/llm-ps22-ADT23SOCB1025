"""Streamlit interface for the Flashcard Generator college mini-project."""

import os

import pandas as pd
import streamlit as st

from utils.flashcard_generator import (
    FlashcardError,
    generate_flashcards,
)


st.set_page_config(page_title="Flashcard Generator", page_icon="📘", layout="centered")

SAMPLE_NOTES = """Photosynthesis is the process by which green plants make their food.
It mainly takes place in the chloroplasts, which contain the green pigment chlorophyll.
Plants use sunlight, carbon dioxide from the air, and water from the soil to produce glucose
and oxygen. The process has two main stages: the light-dependent reactions and the Calvin cycle.
During the light-dependent reactions, light energy is captured and converted into chemical energy
in the form of ATP and NADPH, and oxygen is released from water. In the Calvin cycle, carbon
dioxide is fixed and used to build sugar molecules. Photosynthesis supports most food chains by
converting light energy into chemical energy stored in food."""

DEMO_FLASHCARDS = [
    {
        "question": "Where does photosynthesis mainly take place?",
        "answer": "In chloroplasts, which contain the green pigment chlorophyll.",
    },
    {
        "question": "What materials do plants use in photosynthesis?",
        "answer": "Sunlight, carbon dioxide from the air, and water from the soil.",
    },
    {
        "question": "What products are made during photosynthesis?",
        "answer": "Glucose and oxygen.",
    },
]


st.markdown(
    """
    <style>
    .block-container {max-width: 900px; padding-top: 2.2rem; padding-bottom: 3rem;}
    h1 {color: #17365d; letter-spacing: -0.02em;}
    div[data-testid="stProgress"] > div > div {background-color: #3977b8;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Flashcard Generator")
st.write("Turn your study notes into AI-powered flashcards for quick revision.")
st.caption("Paste notes, choose how many cards to create, then revise at your own pace.")

if "notes" not in st.session_state:
    st.session_state.notes = ""
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []
if "card_index" not in st.session_state:
    st.session_state.card_index = 0
if "revealed" not in st.session_state:
    st.session_state.revealed = False


def load_sample() -> None:
    st.session_state.notes = SAMPLE_NOTES


def clear_notes() -> None:
    st.session_state.notes = ""


def load_demo_cards() -> None:
    """Load example cards so revision and CSV export can be tried without an API key."""
    st.session_state.flashcards = DEMO_FLASHCARDS.copy()
    st.session_state.card_index = 0
    st.session_state.revealed = False


st.header("1. Study notes")
st.text_area(
    "Paste or type your notes",
    key="notes",
    height=260,
    placeholder="Paste a paragraph or set of notes here…",
    help="Use notes with enough detail to support the number of cards you request.",
)
sample_col, clear_col = st.columns(2)
sample_col.button("Load sample notes", on_click=load_sample, use_container_width=True)
clear_col.button("Clear notes", on_click=clear_notes, use_container_width=True)

st.header("2. Generation settings")
settings_col, button_col = st.columns([1, 1])
with settings_col:
    card_count = st.selectbox("Number of flashcards", [5, 10, 15, 20], index=0)
with button_col:
    st.write("")
    st.write("")
    generate_clicked = st.button("Generate flashcards", type="primary", use_container_width=True)

st.button("Load demo flashcards (no API key needed)", on_click=load_demo_cards)

if generate_clicked:
    notes = st.session_state.notes.strip()
    if not notes:
        st.warning("Please enter study notes before generating flashcards.")
    elif len(notes) < 40:
        st.warning("These notes are very short. Add more detail so the cards can be useful and accurate.")
    else:
        try:
            with st.spinner("Reading your notes and preparing flashcards…"):
                cards = generate_flashcards(notes, card_count)
            st.session_state.flashcards = cards
            st.session_state.card_index = 0
            st.session_state.revealed = False
            st.success(f"Generated {len(cards)} flashcards.")
        except FlashcardError as exc:
            st.error(str(exc))
        except Exception:
            st.error("Something unexpected went wrong. Please try again with shorter or clearer notes.")

cards = st.session_state.flashcards
if cards:
    st.divider()
    st.header("3. Revise your flashcards")
    total = len(cards)
    index = min(st.session_state.card_index, total - 1)
    st.session_state.card_index = index
    st.caption(f"Card {index + 1} of {total}")
    st.progress((index + 1) / total)
    card = cards[index]
    with st.container(border=True):
        st.subheader(card["question"])
        if st.session_state.revealed:
            st.markdown("**Answer**")
            st.write(card["answer"])
        else:
            st.button(
                "Reveal answer",
                key=f"reveal_{index}",
                on_click=lambda: setattr(st.session_state, "revealed", True),
            )

    previous_col, restart_col, next_col = st.columns(3)
    if previous_col.button("Previous", disabled=index == 0, use_container_width=True):
        st.session_state.card_index -= 1
        st.session_state.revealed = False
        st.rerun()
    if restart_col.button("Restart revision", use_container_width=True):
        st.session_state.card_index = 0
        st.session_state.revealed = False
        st.rerun()
    if next_col.button("Next", disabled=index >= total - 1, use_container_width=True):
        st.session_state.card_index += 1
        st.session_state.revealed = False
        st.rerun()

    st.divider()
    st.header("4. Export")
    dataframe = pd.DataFrame(cards, columns=["question", "answer"])
    dataframe.columns = ["Question", "Answer"]
    csv_bytes = dataframe.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "Download all flashcards as CSV",
        data=csv_bytes,
        file_name="flashcards.csv",
        mime="text/csv",
        use_container_width=True,
    )

with st.expander("About this project"):
    st.write("Problem Statement 22 · Education & Learning · Roll Number 22")
    st.write("Flashcards are generated only from the notes provided. Review the answers before relying on them for an exam.")
