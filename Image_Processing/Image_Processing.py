import streamlit as st
import cv2
import numpy as np
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# Hàm xử lý ảnh
def flip_image(image, flip_code):
    return cv2.flip(image, flip_code)

def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h))

def change_color_space(image, code):
    return cv2.cvtColor(image, code)

def translate_image(image, x, y):
    M = np.float32([[1, 0, x], [0, 1, y]])
    (h, w) = image.shape[:2]
    return cv2.warpAffine(image, M, (w, h))

def crop_image(image, rect):
    x1, y1, x2, y2 = rect
    return image[y1:y2, x1:x2]

def run_app12():
  
  # Ứng dụng Streamlit
  st.title("Ứng dụng xử lý ảnh")
  
  # Upload ảnh
  uploaded_file = st.file_uploader("Tải ảnh lên", type=["jpg", "png", "jpeg"])
  if uploaded_file:
      image = Image.open(uploaded_file)
      image = np.array(image)
      st.image(image, caption="Ảnh gốc", use_column_width=True)
  
      # Chức năng 1: Lật ảnh
      st.header("1. Lật ảnh")
      flip_option = st.selectbox("Chọn kiểu lật", ["Không lật", "Lật ngang", "Lật dọc", "Lật cả hai"])
      flip_code = {"Không lật": None, "Lật ngang": 1, "Lật dọc": 0, "Lật cả hai": -1}[flip_option]
      if st.button("Lật ảnh") and flip_code is not None:
          flipped_image = flip_image(image, flip_code)
          st.image(flipped_image, caption="Ảnh đã lật", use_column_width=True)
  
      # Chức năng 2: Xoay ảnh
      st.header("2. Xoay ảnh")
      angle = st.slider("Nhập góc xoay (độ)", -360, 360, 0)
      if st.button("Xoay ảnh"):
          rotated_image = rotate_image(image, angle)
          st.image(rotated_image, caption=f"Ảnh xoay {angle}°", use_column_width=True)
  
      # Chức năng 3: Chuyển đổi không gian màu
      st.header("3. Chuyển đổi không gian màu")
      color_space = st.selectbox("Chọn không gian màu", ["Grayscale", "HSV", "Lab"])
      color_code = {"Grayscale": cv2.COLOR_BGR2GRAY, "HSV": cv2.COLOR_BGR2HSV, "Lab": cv2.COLOR_BGR2Lab}[color_space]
      if st.button("Chuyển đổi không gian màu"):
          converted_image = change_color_space(image, color_code)
          if color_space == "Grayscale":
              st.image(converted_image, caption="Ảnh Grayscale", use_column_width=True, channels="GRAY")
          else:
              st.image(converted_image, caption=f"Ảnh {color_space}", use_column_width=True)
  
      # Chức năng 4: Cắt ảnh
      st.header("4. Cắt ảnh")
      st.write("Vẽ một hình chữ nhật trên canvas để chọn vùng cắt.")
      canvas_result = st_canvas(
          fill_color="rgba(255, 165, 0, 0.3)",  # Màu phủ
          stroke_width=2,  # Độ dày nét vẽ
          background_image=Image.fromarray(image),  # Ảnh nền
          update_streamlit=True,
          height=image.shape[0],
          width=image.shape[1],
          drawing_mode="rect",  # Chế độ vẽ hình chữ nhật
          key="canvas",
      )
      if canvas_result.json_data and "objects" in canvas_result.json_data:
          objects = canvas_result.json_data["objects"]
          if objects:
              rect = objects[0]
              x1, y1 = int(rect["left"]), int(rect["top"])
              x2, y2 = x1 + int(rect["width"]), y1 + int(rect["height"])
              cropped_image = crop_image(image, (x1, y1, x2, y2))
              st.image(cropped_image, caption="Ảnh đã cắt", use_column_width=True)
  
      # Chức năng 5: Dịch ảnh
      st.header("5. Dịch ảnh")
      dx = st.number_input("Nhập khoảng dịch theo trục X", value=0)
      dy = st.number_input("Nhập khoảng dịch theo trục Y", value=0)
      if st.button("Dịch ảnh"):
          translated_image = translate_image(image, dx, dy)
          st.image(translated_image, caption=f"Ảnh đã dịch ({dx}, {dy})", use_column_width=True)
