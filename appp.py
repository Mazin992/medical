import os

import easyocr
import cv2
import numpy as np
import requests
from PIL import Image
from io import BytesIO
import re

# تهيئة قارئ EasyOCR لدعم اللغتين العربية والإنجليزية
reader = easyocr.Reader(['en', 'ar'])

# تحديد مسار الصورة (رابط URL أو مسار محلي)
path = "https://support.content.office.net/en-us/media/f6bd775e-0af4-4840-b9c5-de4ef1cd5aa3.png"


# تحميل الصورة من رابط URL أو مسار محلي
def load_image(path):
    if re.match(r'^https?://', path):  # التحقق إذا كان المسار URL
        response = requests.get(path)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            return np.array(image)
        else:
            print("فشل في تحميل الصورة من الرابط.")
            return None
    else:
        if not os.path.exists(path):
            print("الصورة غير موجودة في المسار المحدد.")
            return None
        else:
            image = Image.open(path)
            return np.array(image)


# معالجة الصورة واستخراج النصوص
def extract_text_from_image(image):
    if image is None:
        print("الصورة غير متوفرة للمعالجة.")
        return []

    # التحقق من عدد القنوات في الصورة وتحويلها إذا لزم الأمر
    if len(image.shape) == 3 and image.shape[2] == 3:  # صورة RGB
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    elif len(image.shape) == 2:  # صورة رمادية
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    results = reader.readtext(image, detail=1)
    extracted_texts = []
    for (bbox, text, prob) in results:
        extracted_texts.append((text, prob))
        print(f"النص: {text} - الدقة: {prob:.2f}")

        # رسم مستطيل حول النصوص المكتشفة
        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

    # تحويل الصورة من BGR إلى RGB قبل عرضها باستخدام PIL
    image_with_boxes = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    image_with_boxes.show()

    return extracted_texts


# تحميل ومعالجة الصورة واستخراج النصوص
image = load_image(path)
if image is not None:
    texts = extract_text_from_image(image)