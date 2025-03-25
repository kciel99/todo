
 import streamlit as st
import easyocr
from PIL import Image
import re

st.title("📸 Image → ✅ To-Do Generator")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded image', use_column_width=True)

    # OCR
    reader = easyocr.Reader(['en', 'ko'])  # English + Korean
    result = reader.readtext(uploaded_file)

    # Combine recognized text
    text = "\n".join([item[1] for item in result])
    st.subheader("📃 Extracted Text")
    st.text(text)

    # Extract to-do items (lines that start with numbers or bullets)
    lines = text.split('\n')
    todo_items = [line for line in lines if re.match(r"^\s*[\d\-\●•]+", line)]

    st.subheader("📝 Auto-generated To-Do List")
    edited_items = []

    for i, item in enumerate(todo_items):
        edited = st.text_input(f"Task {i+1}", value=item.strip())
        edited_items.append(edited)

    if st.button("📁 Save Tasks"):
        st.success("Tasks have been saved!")
        st.write("✅ Saved Tasks:")
        for task in edited_items:
            st.write("✔️", task)
