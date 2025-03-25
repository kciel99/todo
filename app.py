import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="To-Do List from Image", layout="centered")
st.title("📝 Image ➜ ✅ To-Do List Generator")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # 이미지 보여주기
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # numpy array로 변환
    image_np = np.array(image)

    # EasyOCR로 텍스트 추출
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image_np)

    # 텍스트만 추출
    lines = [line[1] for line in result]

    st.subheader("📄 Extracted Text")
    extracted_text = "\n".join(lines)
    st.text(extracted_text)

    # To-Do 리스트 만들기
    st.subheader("🗒️ To-Do List")
    todo_items = [line for line in lines if line.strip()]
    edited_items = []

    for i, item in enumerate(todo_items):
        edited = st.text_input(f"Task {i+1}", value=item.strip())
        edited_items.append(edited)

    if st.button("💾 Save"):
        st.success("Tasks saved!")
        for task in edited_items:
            st.write("✔️", task)

  
