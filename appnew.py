import streamlit as st
from PIL import Image
import pytesseract
import numpy as np

st.title("Medical Image Text Reader")
st.write("Upload a medical image to extract text.")

# Upload the image
uploaded_image = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert image to text
    st.write("Extracting text from the image...")
    image_np = np.array(image)
    extracted_text = pytesseract.image_to_string(image_np, lang="eng+ara")

    # Display extracted text
    st.write("Extracted Text:")
    st.text(extracted_text)