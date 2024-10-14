import streamlit as st
import math

# Title of the app
st.title("Scientific Calculator")

# Text input for expression or individual operations
operation = st.text_input("Enter your operation:", "")

# Buttons for various operations
st.write("Choose a basic operation:")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button('Addition'):
        operation = '+'
with col2:
    if st.button('Subtraction'):
        operation = '-'
with col3:
    if st.button('Multiplication'):
        operation = '*'
with col4:
    if st.button('Division'):
        operation = '/'

st.write("Advanced functions:")
if st.button("Square Root"):
    operation = 'sqrt'
if st.button("Power"):
    operation = 'pow'
if st.button("Sine"):
    operation = 'sin'
if st.button("Cosine"):
    operation = 'cos'
if st.button("Tangent"):
    operation = 'tan'
if st.button("Logarithm"):
    operation = 'log'

# Input values
num1 = st.number_input("Enter first number", value=0.0)
num2 = None
if operation not in ['sqrt', 'sin', 'cos', 'tan', 'log']:
    num2 = st.number_input("Enter second number", value=0.0)

# Perform the operation
result = None

try:
    if operation == '+':
        result = num1 + num2
    elif operation == '-':
        result = num1 - num2
    elif operation == '*':
        result = num1 * num2
    elif operation == '/':
        result = num1 / num2 if num2 != 0 else "Cannot divide by zero"
    elif operation == 'sqrt':
        result = math.sqrt(num1)
    elif operation == 'pow':
        result = math.pow(num1, num2)
    elif operation == 'sin':
        result = math.sin(math.radians(num1))
    elif operation == 'cos':
        result = math.cos(math.radians(num1))
    elif operation == 'tan':
        result = math.tan(math.radians(num1))
    elif operation == 'log':
        result = math.log(num1) if num1 > 0 else "Cannot take log of non-positive numbers"
except Exception as e:
    result = f"Error: {str(e)}"

# Output result
if result is not None:
    st.write(f"Result: {result}")
