import streamlit as st 
from streamlit_pdf_viewer import pdf_viewer
import subprocess
import tempfile
import os
import base64
import pathlib as Path


TEXTESTFILE = "main.tex"
TEXDIR = "Hyvong_chuong_trinh"
CURRENT_DIR = Path.Path.cwd()
OUTPUT_DIR = CURRENT_DIR.joinpath("output")
OUTPUT_FILENAME = "TEST_output"

def sidebar():
  add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
  )
  with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
  st.write(f"you select: {add_radio}")
  options = ["what to eat?", "what to drink?"]
  options.append("when to sleep?")
  with st.sidebar:
    add_radio = st.radio(
        "Test options",
        options
    )
  st.write(f"you select: {add_radio}")

def generate_pdf(file=TEXTESTFILE):
  file_to_compile = CURRENT_DIR.joinpath(TEXDIR,TEXTESTFILE) 
  st.write(f"File to compile: {file_to_compile}")
  st.write(f"File out: {OUTPUT_FILENAME}")
  st.write(f"OUTPUT_DIR: {OUTPUT_DIR}")
  #if not OUTPUT_DIR.exists: 
  #  st.write("Folder not exist")
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  with st.spinner("Compiling..."):
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", 
         f"-jobname={OUTPUT_FILENAME}", 
         f"-output-directory={OUTPUT_DIR}",
         file_to_compile.name],
        cwd= CURRENT_DIR.joinpath(TEXDIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
  st.write(file_to_compile)
  if result.returncode != 0:
    st.error("Compilation failed")
    st.text(result.stdout)
    st.text(result.stderr)
  else:
    st.success("Compilation successful!")
    #view pdf 
    #st.pdf(OUTPUT_DIR.joinpath(file_out), 500)

def preview_pdf(pdf_filename: Path =OUTPUT_DIR.joinpath(OUTPUT_FILENAME)):
  """This is pdf good backup"""
  #st.pdf(CURRENT_DIR.joinpath(TEXDIR, "TEST_output.pdf"))
  # Display PDF with custom zoom, alignment, and separators
  #Similar to st.pdf but this method does not call iframe which renders the pdf using browser extension
  #pdf_viewer(
  #  pdf_path,
  ##  height=1000,
  #  zoom_level="auto",           
  #  viewer_align="center",             # Center alignment
  #  show_page_separator=True,           # Show separators between pages
  #  )
  ############
  #pdf_filename = CURRENT_DIR.joinpath(TEXDIR, "TEST_output.pdf")
  if pdf_filename.suffix != ".pdf":
    st.write("file not have extension")
    pdf_filename= pdf_filename.with_suffix(".pdf")
  else:
    st.write("File has extension")
  st.write(f"output name {pdf_filename.name}")
  with open(pdf_filename, "rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode("utf-8")
  
  pdf_viewer_html = f"""
    <iframe 
        src="data:application/pdf;base64,{base64_pdf}" 
        width="100%" 
        height="720px"
        style="border:1px solid black; border-radius:8px;"
    ></iframe>
    """

  st.markdown(f"""
  <style>
  /* Target the specific element containing the PDF viewer */
  [data-testid="stPdfViewer"] {{
      background-color: #F0F2F6; /* Light gray background */
      padding: 20px; /* Add some padding around the PDF */
      border-radius: 8px; /* Optional: rounded corners */
  }}
  </style>
  """, unsafe_allow_html=True)

  st.markdown(pdf_viewer_html, unsafe_allow_html=True)
  return 0

def main():

  st.set_page_config(layout="centered") # Or leave default
  sidebar()

  # Inject custom CSS
  st.markdown("""
  <style>
  .stApp {
      max-width: 1200px; /* Adjust this value for your desired width */
      margin: 0 auto;   /* ✅ This actually centers the app */
  }
  /* Target the main content block */
  .stMainBlockContainer {
      max-width: 100%;
  }
  </style>
  """, unsafe_allow_html=True)

  st.title("Create Chuong Trinh Tho Phuong template web-app")
  st.header("Create Chuong Trinh Tho Phuong template web-app")
  st.write("This app has a fixed max-width of 1200px.")
  st.subheader("Not sure what to put here")
  st.header("Latex testing")
  st.latex(r"E=mc^2")
  generate_pdf()
  preview_pdf() 

  
  
if __name__ == "__main__":
  main()