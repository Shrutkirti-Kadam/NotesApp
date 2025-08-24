import streamlit as st
import sqlite3

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("notes.db")  # File-based DB
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_note(title, content):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()

def get_notes():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    data = c.fetchall()
    conn.close()
    return data

def delete_note(note_id):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()

# --- Streamlit App ---
st.title("📝 Notes App")

# Initialize DB
init_db()

# Add new note
st.subheader("Add a new note")
title = st.text_input("Title")
content = st.text_area("Content")

if st.button("Add Note"):
    if title and content:
        add_note(title, content)
        st.success("✅ Note added!")
    else:
        st.error("⚠️ Please fill in both fields.")

# Show existing notes
st.subheader("Your Notes")
notes = get_notes()

if notes:
    for note in notes:
        st.markdown(f"### {note[1]}")
        st.write(note[2])
        if st.button("Delete", key=note[0]):
            delete_note(note[0])
            st.warning(f"❌ Deleted note: {note[1]}")
            st.experimental_rerun()
else:
    st.info("No notes yet. Add one above 👆")
