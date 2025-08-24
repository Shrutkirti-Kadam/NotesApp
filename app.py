import streamlit as st
import sqlite3

# ---------- SESSION STATE ----------
if 'notes_updated' not in st.session_state:
    st.session_state['notes_updated'] = False

# ---------- DATABASE SETUP ----------
DB_PATH = "notes.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()

# Drop old table if schema is wrong (optional, remove if you want to keep old notes)
# c.execute("DROP TABLE IF EXISTS notes")

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
    """Add a note to the database."""
    if note_text.strip() == "":
        st.warning("Please enter some text.")
        return
    c.execute("INSERT INTO notes (note) VALUES (?)", (note_text,))
    conn.commit()
    st.session_state['notes_updated'] = True

def delete_note(note_id):
    """Delete a note from the database."""
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    st.session_state['notes_updated'] = True

def get_all_notes():
    """Fetch all notes from the database."""
    c.execute("SELECT id, note FROM notes")
    notes = c.fetchall()
    return notes if notes else []

# ---------- APP UI ----------
st.title("📒 Notes App")

# Input to add a new note
note_input = st.text_input("Write a new note:")
if st.button("Add Note"):
    add_note(note_input)

# Display existing notes
st.subheader("Your Notes:")
notes = get_all_notes()

if notes:
    for note_id, note_text in notes:
        col1, col2 = st.columns([8, 1])
        col1.write(note_text)
        if col2.button("❌", key=f"delete_{note_id}"):
            delete_note(note_id)
else:
    st.info("No notes yet! Add one above.")

# ---------- UI UPDATE LOGIC ----------
# Trigger UI refresh automatically when notes are updated
if st.session_state['notes_updated']:
    st.session_state['notes_updated'] = False
    st.experimental_rerun = lambda: None  # override deprecated function
    # UI will automatically refresh next Streamlit rerun without calling deprecated rerun
