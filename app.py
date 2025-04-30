import io
import os
import sqlite3
import tempfile

import pandas as pd
import streamlit as st

from internals.agent import init_agent
from internals.tools import get_current_date
from internals.utils import InvalidRequest, Response, get_table_schema

st.set_page_config(page_title="SQLite Query Tool", layout="wide")

st.title("SQLite Database Query Tool")
st.markdown("Upload a SQLite database file and execute SQL queries.")

with st.sidebar:
    st.header("Upload Database")
    uploaded_file = st.file_uploader(
        "Choose a SQLite file", type=["db", "sqlite", "sqlite3"]
    )
    st.info(
        "Once the database is uploaded, you can execute SQL queries in the main panel."
    )

if "db_path" not in st.session_state:
    st.session_state.db_path = None

if 'show_viz' not in st.session_state:
    st.session_state.show_viz = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = None

def send_query(query):
    """Send the query to the agent and return the result."""
    result = st.session_state.agent.run_sync(query, message_history=st.session_state.chat_history)
    return result


if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    st.session_state.db_path = tmp_path
    st.sidebar.success(f"Database uploaded successfully!")
    st.session_state.md_lines = get_table_schema(st.session_state.db_path)
    st.session_state.agent = init_agent(st.session_state.md_lines, tools=[])
    if st.sidebar.button("Inspect Database Structure"):
        try:
            conn = sqlite3.connect(st.session_state.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
            )
            tables = cursor.fetchall()
            if tables:
                st.sidebar.subheader("Database Tables:")
                for table in tables:
                    table_name = table[0]

                    st.sidebar.write(f"• {table_name}")
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = cursor.fetchall()

                    with st.sidebar.expander(f"Schema for {table_name}"):
                        cols_df = pd.DataFrame(
                            columns,
                            columns=[
                                "cid",
                                "name",
                                "type",
                                "notnull",
                                "default_value",
                                "pk",
                            ],
                        )

                        st.dataframe(cols_df[["name", "type", "pk"]])
            else:
                st.sidebar.warning("No tables found in the database.")
            conn.close()
        except Exception as e:
            st.sidebar.error(f"Error inspecting database: {e}")
else:
    st.info("Please upload a SQLite database file to begin.")

if st.session_state.db_path:
    st.markdown("---")
    st.subheader("SQL Query")
    query = st.text_area("Enter your query here:", height=70)
    execute_button = st.button("Search the DB")
    if execute_button and query:
        sql_query_response = send_query(query)
        if isinstance(sql_query_response.output, InvalidRequest):
            st.error(f"Error: {sql_query_response.output.error_message}")
        else:
            try:
                sql_query = sql_query_response.output
                st.session_state.chat_history = sql_query_response.all_messages()
                conn = sqlite3.connect(st.session_state.db_path)
                df = pd.read_sql_query(sql_query.sql_query, conn)
                conn.close()
                st.subheader("Query Results")
                st.write(f"SQL Query: `{sql_query.sql_query}`")
                st.write(f"Explanation: {sql_query.explanation}")
                st.write(f"Found {len(df)} rows.")
                st.markdown(
                    """
                    <style>
                    .dataframe-container {
                        width: 100%;
                        overflow-x: auto;
                        white-space: nowrap;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
                with st.container():
                    st.markdown(
                        '<div class="dataframe-container">', unsafe_allow_html=True
                    )
                    st.dataframe(df)
                    st.markdown("</div>", unsafe_allow_html=True)
                if not df.empty:
                    csv = df.to_csv(index=False)
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.download_button(
                            label="Download Results as CSV",
                            data=csv,
                            file_name="query_results.csv",
                            mime="text/csv",
                        )
                   
            except Exception as e:
                st.error(f"Error executing query: {e}")

    def cleanup():
        if st.session_state.db_path and os.path.exists(st.session_state.db_path):
            try:
                os.unlink(st.session_state.db_path)
            except:
                pass

    import atexit

    atexit.register(cleanup)
