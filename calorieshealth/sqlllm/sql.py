from dotenv import load_dotenv
import os
import streamlit as st
import sqlite3
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Generative AI client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to load the new model and get responses
def get_gemini_response(question, prompt):
    # Initialize the new model
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Generate content using the new model
    response = model.generate_content([prompt[0], question])

    print(response.text)

    # Execute the SQL query and fetch results
    output = read_sql_query(response.text, "test.db")

    print(output)
    return output


# Function to execute SQL query
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    return rows


# Initialize the Streamlit app
prompt = [
    """You are an expert in converting English questions to SQL code!
      The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
      SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
      the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ; 
      also the sql code should not have ``` in beginning or end and sql word in output
      """
]

st.set_page_config(page_title="I can Retrieve Any SQL query")

st.header("Gemini Application")

questions = st.text_input("Input:", key="input")

submit = st.button("Ask the question")

# If the ask button is clicked
if submit:
    response = get_gemini_response(questions, prompt)
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.subheader(row)
