import streamlit as st
import sqlite3
import re

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

def find_query(sentence):
    select_regex = r"give me the (.+) of the students"
    update_regex = r"update the (.+) of the student having roll no (\d+) to (.+)"
    conditional_regex = r"show the (.+) of the students whose (.+)"
    all_regex = r"give me all the (.+) of the students"

    select_match = re.search(select_regex, sentence)
    update_match = re.search(update_regex, sentence)
    conditional_match = re.search(conditional_regex, sentence)
    all_match = re.search(all_regex, sentence)
    keywords = {
        'more than': '>',
        'less than': '<',
        'equal to': '=', 
        'and':','
    }

    if select_match:
        select = select_match.group(1)
        if select == "roll numbers":
            sql_query = "SELECT roll FROM students;"
        elif select == "all the information":
            sql_query = "SELECT * FROM students;"
        else:
            sql_query = f"SELECT {select} FROM students;"
    elif update_match:
        col = update_match.group(1)
        roll_no = update_match.group(2)
        value = update_match.group(3)
        sql_query = f"UPDATE students SET {col}={value} WHERE roll={roll_no};"
    elif conditional_match:
        select = conditional_match.group(1)
        condition = conditional_match.group(2)
        for x in keywords:
            if x in select: 
                select=select.replace(x,keywords[x])
            if x in condition: 
                condition=condition.replace(x,keywords[x])
        
        sql_query = f"SELECT {select} FROM students WHERE {condition};"
    elif all_match:
        sql_query = "SELECT * FROM students;"
    else:
        sql_query = "Invalid input."

    return sql_query

def execute_query(query):
    cursor.execute(query)
    db = cursor.fetchall()
    return db

st.title('SQL Query Generator')
text = st.text_input("Text to parse")

if st.button('Find'):
    result = find_query(text)
    st.markdown('## Results')
    st.markdown('Query: ')
    st.write(result)
    db = execute_query(result)
    st.markdown('Output from database: ')
    st.write(db)