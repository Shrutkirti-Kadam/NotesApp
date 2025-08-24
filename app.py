import streamlit as st
import psycopg2
import os

# Load DB credentials from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "notesdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="notesdb",
    user="postgres",
    password="BATANDBALL",
    port="5432"
)
cur = conn.cursor()

# Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    is_done BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
conn.commit()

# --- Streamlit UI ---
st.title("📝 Notes App")

# Add a new note
note = st.text_input("Enter a new note:")
if st.button("Add Note"):
    cur.execute("INSERT INTO notes (content) VALUES (%s)", (note,))
    conn.commit()
    st.success("Note added!")

# Display notes
cur.execute("SELECT id, content, is_done FROM notes ORDER BY id DESC")
rows = cur.fetchall()

st.subheader("Your Notes:")
for r in rows:
    note_id, content, is_done = r
    col1, col2, col3 = st.columns([4,1,1])
    with col1:
        st.write(f"{'✅' if is_done else '📝'} {content}")
    with col2:
        if st.button("✔️", key=f"done{note_id}"):
            cur.execute("UPDATE notes SET is_done = TRUE WHERE id = %s", (note_id,))
            conn.commit()
            st.rerun()
    with col3:
        if st.button("❌", key=f"delete{note_id}"):
            cur.execute("DELETE FROM notes WHERE id = %s", (note_id,))
            conn.commit()
            st.rerun()
