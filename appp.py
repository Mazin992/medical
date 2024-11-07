import easyocr
import cv2
import numpy as np
from PIL import Image
import os

# مسار الصورة (تأكد من تحديثه إلى المسار الصحيح)
path = r"C:\UsingTempImageDonnotDELETE\image.png"  # استخدم المسار الكامل للصورة مع اسم الملف

# تهيئة قارئ EasyOCR لدعم اللغتين العربية والإنجليزية
reader = easyocr.Reader(['en', 'ar'])


# تحميل الصورة من مسار الملف
def load_image(path):
    image = Image.open(path)
    return np.array(image)


# معالجة الصورة واستخراج النصوص
def extract_text_from_image(image):
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


# تحقق من وجود الصورة
if not os.path.exists(path):
    print("الصورة غير موجودة في المسار المحدد.")
else:
    image = load_image(path)
    texts = extract_text_from_image(image)
