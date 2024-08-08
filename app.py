import streamlit as st
import subprocess
import os
import zipfile

# Function to read the LaTeX template from a file and generate the PDF
def generate_pdf(template_name, first_name, last_name, school_name, class_level):
    template_path = os.path.join(class_level, template_name, f'{template_name}.tex')
    
    # Ensure the template file exists
    if not os.path.exists(template_path):
        st.error(f"Template file not found: {template_path}")
        return None

    # Read the LaTeX template file
    with open(template_path, 'r', encoding='utf-8') as file:
        latex_template = file.read()

    # Replace placeholders with actual data
    latex_content = latex_template.replace('{{ first_name }}', first_name)
    latex_content = latex_content.replace('{{ last_name }}', last_name)
    latex_content = latex_content.replace('{{ school_name }}', school_name)
    latex_content = latex_content.replace('{{ class_level }}', class_level)

    # Write the filled template to a .tex file
    output_tex_path = os.path.join(class_level, template_name, f'{template_name}_output.tex')
    with open(output_tex_path, 'w', encoding='utf-8') as file:
        file.write(latex_content)

    # Compile the .tex file to a PDF
    subprocess.run(['xelatex', '-output-directory', os.path.join(class_level, template_name), output_tex_path])

    output_pdf_path = os.path.join(class_level, template_name, f'{template_name}_output.pdf')
    if os.path.exists(output_pdf_path):
        return output_pdf_path
    else:
        st.error(f"Failed to generate PDF for template: {template_name}")
        return None

# Streamlit form for user input
st.title("PDF Generator for Multiple Templates")

first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
school_name = st.text_input("School Name")
class_level = st.selectbox("Class Level", ["3APIC", "2APIC", "1APIC"])

if class_level == "3APIC":
    template_names = ["Ch_1_Identités remarquables et puissances", "Ch_2_Racines carrées"]
elif class_level == "2APIC":
    template_names = ["Ch_1_Identité remarquable et puissance", "Ch_2_Racine carrée"]

if st.button("Generate PDFs and Download ZIP"):
    pdf_paths = []
    for template_name in template_names:
        pdf_path = generate_pdf(template_name, first_name, last_name, school_name, class_level)
        if pdf_path:
            pdf_paths.append(pdf_path)
    
    if pdf_paths:
        # Create a zip file containing all the PDFs
        zip_path = 'generated_documents.zip'
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for pdf_path in pdf_paths:
                zipf.write(pdf_path, os.path.basename(pdf_path))
        
        # Provide download link for the zip file
        with open(zip_path, "rb") as zip_file:
            st.download_button(label="Download ZIP", data=zip_file, file_name="generated_documents.zip")
