import streamlit as st
import math

# Title of the app
st.title("Scientific Calculator")

# Store the current input and operation
if 'expression' not in st.session_state:
    st.session_state.expression = ""

# Function to update the expression
def update_expression(value):
    st.session_state.expression += str(value)

# Function to clear the expression
def clear_expression():
    st.session_state.expression = ""

# Function to calculate the result
def calculate_expression():
    try:
        # Use Python's eval to calculate the result of the expression
        st.session_state.expression = str(eval(st.session_state.expression))
    except Exception as e:
        st.session_state.expression = "Error"

# Display the current input
st.text_input("Input", value=st.session_state.expression, key='input_box', disabled=True)

# Create button layout (calculator style)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.button("7", on_click=update_expression, args=("7",))
    st.button("4", on_click=update_expression, args=("4",))
    st.button("1", on_click=update_expression, args=("1",))
    st.button("0", on_click=update_expression, args=("0",))

with col2:
    st.button("8", on_click=update_expression, args=("8",))
    st.button("5", on_click=update_expression, args=("5",))
    st.button("2", on_click=update_expression, args=("2",))
    st.button(".", on_click=update_expression, args=(".",))

with col3:
    st.button("9", on_click=update_expression, args=("9",))
    st.button("6", on_click=update_expression, args=("6",))
    st.button("3", on_click=update_expression, args=("3",))
    st.button("+", on_click=update_expression, args=("+",))  # Addition

with col4:
    st.button("&#247;", on_click=update_expression, args=("/",))  # Division
    st.button("&#215;", on_click=update_expression, args=("*",))  # Multiplication
    st.button("-", on_click=update_expression, args=("-",))  # Subtraction
    st.button("=", on_click=calculate_expression)  # Calculate result

# Second row of scientific buttons
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.button("sin", on_click=update_expression, args=("math.sin(",))
    st.button("cos", on_click=update_expression, args=("math.cos(",))

with col6:
    st.button("tan", on_click=update_expression, args=("math.tan(",))
    st.button("log", on_click=update_expression, args=("math.log(",))

with col7:
    st.button("sqrt", on_click=update_expression, args=("math.sqrt(",))
    st.button("exp", on_click=update_expression, args=("math.exp(",))

with col8:
    st.button("C", on_click=clear_expression)  # Clear button

# Info text
st.write("Use buttons to build the expression and press '=' to calculate.")
