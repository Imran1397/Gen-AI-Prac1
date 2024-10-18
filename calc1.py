import streamlit as st
import math

# Function to evaluate the expression
def evaluate_expression(expression):
    try:
        # Evaluate the expression using eval (use with caution)
        result = eval(expression, {"__builtins__": None}, {
            "math": math,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "sqrt": math.sqrt,
            "pi": math.pi,
            "e": math.e
        })
        return result
    except Exception as e:
        return str(e)

# Streamlit UI
st.title("Scientific Calculator")

# Input box for the user to enter expressions
expression = st.text_input("Enter your expression:", "")

# Display buttons for numbers and operations
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("1"): expression += "1"
    if st.button("2"): expression += "2"
    if st.button("3"): expression += "3"
    if st.button("sin"): expression += "math.sin("
    if st.button("cos"): expression += "math.cos("
    if st.button("tan"): expression += "math.tan("
    if st.button("sqrt"): expression += "math.sqrt("

with col2:
    if st.button("4"): expression += "4"
    if st.button("5"): expression += "5"
    if st.button("6"): expression += "6"
    if st.button("log"): expression += "math.log("
    if st.button("pi"): expression += "math.pi"
    if st.button("e"): expression += "math.e"

with col3:
    if st.button("7"): expression += "7"
    if st.button("8"): expression += "8"
    if st.button("9"): expression += "9"
    if st.button("+"): expression += "+"
    if st.button("-"): expression += "-"
    if st.button("*"): expression += "*"
    if st.button("/"): expression += "/"

# Button to evaluate the expression
if st.button("Evaluate"):
    result = evaluate_expression(expression)
    st.write("Result:", result)

# Display the current expression
st.write("Current Expression:", expression)
