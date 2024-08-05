import streamlit as st
import subprocess
import re

# Function to check if a string contains only Latin letters
def is_latin_letters(input_string):
    return re.match("^[A-Za-z ]*$", input_string) is not None

# Function to read the LaTeX template from a file and generate the PDF
def generate_pdf(first_name, last_name, school_name, class_level):
    # Read the LaTeX template file
    with open('template.tex', 'r') as file:
        latex_template = file.read()

    # Replace placeholders with actual data
    latex_content = latex_template.replace('{{ first_name }}', first_name)
    latex_content = latex_content.replace('{{ last_name }}', last_name)
    latex_content = latex_content.replace('{{ school_name }}', school_name)
    latex_content = latex_content.replace('{{ class_level }}', class_level)

    # Write the filled template to a .tex file
    with open('output.tex', 'w') as file:
        file.write(latex_content)

    # Compile the .tex file to a PDF
    subprocess.run(['pdflatex', 'output.tex'])

    return 'output.pdf'

# Streamlit form for user input
st.title("PDF Generator")

first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
school_name = st.text_input("School Name")
class_level = st.text_input("Class Level")

# Validate input data
if st.button("Generate PDF"):
    if (is_latin_letters(first_name) and is_latin_letters(last_name) and 
        is_latin_letters(school_name) and is_latin_letters(class_level)):
        pdf_path = generate_pdf(first_name, last_name, school_name, class_level)
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(label="Download PDF", data=pdf_file, file_name="generated_document.pdf")
    else:
        st.error("Please use only Latin letters in all fields.")
