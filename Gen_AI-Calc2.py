import streamlit as st
import math

# Title of the app
st.title("Scientific Calculator")

# Select the operation
operation = st.selectbox("Choose Operation:", 
                         ["Addition", "Subtraction", "Multiplication", "Division", 
                          "Square Root", "Exponential", "Logarithm", "Sin", "Cos", "Tan"])

# Input values
if operation in ["Addition", "Subtraction", "Multiplication", "Division"]:
    num1 = st.number_input("Enter first number", value=0.0, format="%.2f")
    num2 = st.number_input("Enter second number", value=0.0, format="%.2f")
else:
    num = st.number_input("Enter a number", value=0.0, format="%.2f")

# Perform calculations
def calculate(operation, num1=None, num2=None, num=None):
    try:
        if operation == "Addition":
            return num1 + num2
        elif operation == "Subtraction":
            return num1 - num2
        elif operation == "Multiplication":
            return num1 * num2
        elif operation == "Division":
            if num2 != 0:
                return num1 / num2
            else:
                return "Cannot divide by zero"
        elif operation == "Square Root":
            return math.sqrt(num)
        elif operation == "Exponential":
            return math.exp(num)
        elif operation == "Logarithm":
            if num > 0:
                return math.log(num)
            else:
                return "Logarithm undefined for non-positive numbers"
        elif operation == "Sin":
            return math.sin(math.radians(num))
        elif operation == "Cos":
            return math.cos(math.radians(num))
        elif operation == "Tan":
            return math.tan(math.radians(num))
    except Exception as e:
        return f"Error: {e}"

# Result calculation and display
if operation in ["Addition", "Subtraction", "Multiplication", "Division"]:
    if st.button("Calculate"):
        result = calculate(operation, num1, num2)
        st.write(f"Result: {result}")
else:
    if st.button("Calculate"):
        result = calculate(operation, num=num)
        st.write(f"Result: {result}")
