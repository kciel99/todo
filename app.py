import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import cv2
import re

st.title("📝 이미지에서 To-Do 리스트 추출기")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # 이미지 표시
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드한 이미지', use_column_width=True)

    # PIL ➜ OpenCV (Grayscale)
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    # 전처리: 임계값 적용 (Threshold)
    _, thresh = cv2.threshold(image_cv, 150, 255, cv2.THRESH_BINARY)

    # OCR 실행
    reader = easyocr.Reader(['en', 'ko'])  # 영어 + 한국어 지원
    result = reader.readtext(thresh, detail=0)

    # 전체 텍스트 출력
    full_text = "\n".join(result)
    st.subheader("📄 추출된 텍스트")
    st.text(full_text)

    # To-do 아이템 추출: 숫자, 기호로 시작하는 줄만 뽑기
    todo_items = [line for line in result if re.match(r"^\s*[\d\-•*·]+\s*", line)]

    st.subheader("📋 자동 생성된 To-Do 리스트")
    edited_items = []
    for i, item in enumerate(todo_items):
        edited = st.text_input(f"할 일 {i+1}", value=item.strip())
        edited_items.append(edited)

    if st.button("✅ 저장"):
        st.success("할 일이 저장되었습니다!")
        st.write("📝 저장된 할 일 목록:")
        for task in edited_items:
            st.write("✔️", task)
