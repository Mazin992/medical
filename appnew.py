import streamlit as st
from PIL import Image
import numpy as np


# إعداد واجهة Streamlit
st.title("قارئ الصور الطبية")
st.write("قم برفع صورة للنتائج الطبية لقراءتها.")

# تحميل الصورة من المستخدم
uploaded_image = st.file_uploader("اختر صورة", type=["jpg", "jpeg", "png"])

# التحقق من تحميل الصورة
if uploaded_image is not None:
    # عرض الصورة
    image = Image.open(uploaded_image)
    st.image(image, caption="الصورة الطبية", use_column_width=True)


    # تحويل الصورة إلى صيغة مناسبة لـ EasyOCR
    image_np = np.array(image)
