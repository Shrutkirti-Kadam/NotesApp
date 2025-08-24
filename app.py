import streamlit as st
import sqlite3

# ---------- DATABASE SETUP ----------
conn = sqlite3.connect("notes.db", check_same_thread=False)
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    note TEXT
)
''')
conn.commit()

# ---------- FUNCTIONS ----------
def add_note(note_text):
    c.execute("INSERT INTO notes (note) VALUES (?)", (note_text,))
    conn.commit()
    st.session_state['notes_updated'] = True

def delete_note(note_id):
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    st.session_state['notes_updated'] = True

def get_all_notes():
    c.execute("SELECT * FROM notes")
    return c.fetchall()

# ---------- APP UI ----------
st.title("📒 Notes App")

# Input for adding a new note
note_input = st.text_input("Write a new note:")
if st.button("Add Note"):
    if note_input.strip() != "":
        add_note(note_input)
        st.experimental_rerun()
    else:
        st.warning("Please enter some text.")

# Display existing notes
st.subheader("Your Notes:")
notes = get_all_notes()

if notes and isinstance(notes, list):
    for note in notes:
        if len(note) != 2:
            continue  # skip malformed entries
        note_id, note_text = note
        col1, col2 = st.columns([8, 1])
        col1.write(note_text)
        if col2.button("❌", key=f"delete_{note_id}"):
            delete_note(note_id)
            st.experimental_rerun()
else:
    st.info("No notes yet! Add one above.")

# ---------- SESSION STATE ----------
if 'notes_updated' not in st.session_state:
    st.session_state['notes_updated'] = False
