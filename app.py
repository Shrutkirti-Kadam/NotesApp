import streamlit as st
import sqlite3
import os

# ---------- SESSION STATE INIT ----------
if 'notes_updated' not in st.session_state:
    st.session_state['notes_updated'] = False

# ---------- DATABASE SETUP ----------
DB_PATH = "notes.db"

# Connect to SQLite with thread safety for Streamlit
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()

# Drop table if old schema exists (optional, remove if you want to keep old notes)
# c.execute("DROP TABLE IF EXISTS notes")

# Create table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    note TEXT NOT NULL
)
''')
conn.commit()

# ---------- FUNCTIONS ----------
def add_note(note_text):
    if note_text.strip() == "":
        st.warning("Please enter some text.")
        return
    c.execute("INSERT INTO notes (note) VALUES (?)", (note_text,))
    conn.commit()
    st.session_state['notes_updated'] = True

def delete_note(note_id):
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    st.session_state['notes_updated'] = True

def get_all_notes():
    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    return notes if notes else []

# ---------- APP UI ----------
st.title("📒 Notes App")

# Input for adding a new note
note_input = st.text_input("Write a new note:")
if st.button("Add Note"):
    add_note(note_input)
    st.experimental_rerun()  # safe rerun after database change

# Display existing notes
st.subheader("Your Notes:")
notes = get_all_notes()

if notes:
    for note in notes:
        if len(note) < 2:
            continue  # skip malformed rows
        note_id, note_text = note[:2]  # only take first 2 elements
        col1, col2 = st.columns([8, 1])
        col1.write(note_text)
        if col2.button("❌", key=f"delete_{note_id}"):
            delete_note(note_id)
            st.experimental_rerun()
else:
    st.info("No notes yet! Add one above.")
