from dotenv import load_dotenv
import os
import sqlite3
import google.generativeai as genai
from streamlit_lottie import st_lottie
import json
import streamlit as st

# Load environment variables
load_dotenv()  # Load all the environment variables

# Configure GenAI Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Lottie animation from file
def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Load your Lottie animation
lottie_animation = load_lottie_file("D:\Animation - 1733443519214.json")  # Replace with your actual path


# Function To Load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function To retrieve query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    # Retrieve column names from the cursor
    columns = [desc[0] for desc in cur.description]
    conn.commit()
    conn.close()
    return rows, columns

# Define Your Prompt
prompt = [
    """
    You are an expert in translating natural language questions into SQL queries. The SQL database has table named 'STUDENT', which contains the following columns:

    - NAME: The name of the student (Character data type, e.g., 'John Doe')
    - CLASS: The class the student is enrolled in (Character data type, e.g., 'Data Science')
    - GRADE: The grade the student received (Character data type, e.g., 'A+', 'B-', 'C')
    - MARKS: The marks the student received in their exams (Numeric data type, e.g., 85, 90, etc.)
    - SECTION: The section of the class the student belongs to (Character data type, e.g., 'A', 'B', 'C')

    Your task is to generate SQL queries based on the English questions provided. Here are some guidelines and examples to help you:

    **Guidelines:**
    1. The SQL query should be valid, syntactically correct, and written in standard SQL.
    2. Do not include the sql word in the output and do not start or end SQL query with ``` in output.
    3. Use proper SQL functions, clauses, and operators (e.g., SELECT, WHERE, COUNT, etc.) to answer the question.
    4. Be aware of data types:
        - The **GRADE** column is a **character** data type (e.g., 'A+', 'B-', 'C') and should not be treated as numeric.
        - The **MARKS** column is a **numeric** data type (e.g., 85, 90, etc.).
        - The **NAME**, **CLASS**, and **SECTION** columns are also **character** data types.
    5. **Do NOT** apply functions like `MAX()` or `MIN()` to the **GRADE** column, as it is a text-based column.
    6. Focus on answering the question accurately based on the database structure and the data types of column attributes.
    7. Be careful not to treat text-based columns (like **GRADE**, **NAME**, **CLASS**, **SECTION**) as numeric values.
    8.'A+' grade means student has got highest grade and 'F' grade means student has failed.
    9.The database does not include students with invalid or missing grades, so make sure queries handle only valid grades and records.
    10.Please generate a precise SQL query based on the English question given. Be mindful of SQL syntax, correct column names, and the database schema.

    **Examples:**
    Example 1 - "How many records are in the database?"
    SQL Query: SELECT COUNT(*) FROM STUDENT;

    Example 2 - "List all students enrolled in the 'Data Science' class."
    SQL Query: SELECT * FROM STUDENT WHERE CLASS = 'Data Science';

    Example 3 - "What is the average marks of students in the 'ECE' class?"
    SQL Query: SELECT AVG(MARKS) FROM STUDENT WHERE CLASS = 'ECE';

    Example 4 - "Which students have received an 'A+' grade?"
    SQL Query: SELECT NAME FROM STUDENT WHERE GRADE = 'A+';

    Example 5 - "What is the total number of students in each section?"
    SQL Query: SELECT SECTION, COUNT(*) FROM STUDENT GROUP BY SECTION;

    Example 6 - "List all students who scored more than 80 marks and are in the 'Data Science' class."
    SQL Query: SELECT NAME FROM STUDENT WHERE CLASS = 'Data Science' AND MARKS > 80;

    Example 7 - "Find the student with the maximum marks in each class."
    SQL Query: SELECT CLASS, NAME, MAX(MARKS) FROM STUDENT GROUP BY CLASS;

    Example 8 - "What are the names of students who scored more than the average marks of the entire class?"
    SQL Query: SELECT NAME FROM STUDENT WHERE MARKS > (SELECT AVG(MARKS) FROM STUDENT);

    Example 9 - "Show details of students with the highest grade."
    SQL Query: SELECT * FROM STUDENT WHERE GRADE = 'A+';

    Example 10 - "Which students have the least marks in the 'Data Science' class?"
    SQL Query: SELECT NAME FROM STUDENT WHERE CLASS = 'Data Science' AND MARKS = (SELECT MIN(MARKS) FROM STUDENT WHERE CLASS = 'Data Science');


    """
]
# Streamlit App
st.set_page_config(page_title="SQL QUERY RETRIEVER")

# Header with animation
col1, col2 = st.columns([3, 6])  # Adjust column ratios for better alignment
with col1:
    st.markdown("<h1 style='margin-bottom: 10px;'>QueryMate</h1>", unsafe_allow_html=True)
with col2:
    st_lottie(lottie_animation, height=150,width=250, key="querymate_animation")  # Adjust height as necessary

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    st.write("Generated SQL Query:")
    st.code(response, language='sql')  # Display the generated SQL query
    try:
        data, columns = read_sql_query(response, "student.db")
        if data:
            st.subheader("The Response is:")

            # Convert the data and columns to an HTML table with custom styles
            table_html = f"""
            <style>
                .custom-table {{
                    background-color: #ffcccc;  /* Light red background */
                    color: black;              /* Black text color */
                    border-collapse: collapse;
                    width: 100%;
                }}
                .custom-table th, .custom-table td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    color: black;  /* Black text color for table data */
                }}
                .custom-table th {{
                    background-color: white;   /* White background for headings */
                    color: black;              /* Black text for headings */
                    text-align: left;
                }}
            </style>
            <table class="custom-table">
                <thead>
                    <tr>{"".join(f"<th>{col}</th>" for col in columns)}</tr>
                </thead>
                <tbody>
                    {"".join(
                        f"<tr>{''.join(f'<td>{cell}</td>' for cell in row)}</tr>" 
                        for row in data
                    )}
                </tbody>
            </table>
            """

            # Display the styled HTML table
            st.markdown(table_html, unsafe_allow_html=True)
        else:
            st.warning("No data found for the given query.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
