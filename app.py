import streamlit as st
import sqlite3
import os

# ---------- SESSION STATE ----------
if 'notes_updated' not in st.session_state:
    st.session_state['notes_updated'] = False

# ---------- DATABASE SETUP ----------
DB_PATH = "notes.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()

# Drop old table if schema is wrong (only if you don't need old notes)
c.execute("DROP TABLE IF EXISTS notes")
conn.commit()

# Create table with correct schema
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

# Add note
note_input = st.text_input("Write a new note:")
if st.button("Add Note"):
    add_note(note_input)

# Display notes
st.subheader("Your Notes:")
notes = get_all_notes()

if notes:
    for note in notes:
        if len(note) < 2:
            continue
        note_id, note_text = note[:2]
        col1, col2 = st.columns([8, 1])
        col1.write(note_text)
        if col2.button("❌", key=f"delete_{note_id}"):
            delete_note(note_id)
            st.session_state['notes_updated'] = True
else:
    st.info("No notes yet! Add one above.")

# ---------- REFRESH LOGIC ----------
# If notes were updated, rerun UI without using deprecated function
if st.session_state['notes_updated']:
    st.session_state['notes_updated'] = False
    st.experimental_rerun()  # For Streamlit <1.25
    # For Streamlit >=1.25, you can just rely on state; UI updates automatically
