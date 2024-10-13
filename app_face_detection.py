import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image

def run_app3():
    # Part 1: Display face and non-face images
    st.title("Face and Non-face Data")
    
    st.subheader("Face Images")
    face_image_paths = [
    ]  # Add your actual image paths here
    for img_path in face_image_paths:
        img = Image.open(img_path)
        st.image(img, caption=f"Face Image: {img_path}", use_column_width=True)

    st.subheader("Non-Face Images")
    non_face_image_paths = [

    ]  # Add your actual image paths here
    for img_path in non_face_image_paths:
        img = Image.open(img_path)
        st.image(img, caption=f"Non-Face Image: {img_path}", use_column_width=True)

    # Part 2: Display training results and vector image
    st.title("Training Results")
    st.subheader("Train")
    non_face_image_paths = [
        'Face_Detection_folder/vecto.png'
    ]  # Add your actual image paths here
    for img_path in non_face_image_paths:
        img = Image.open(img_path)
        st.image(img, caption=f"Non-Face Image: {img_path}", use_column_width=True)

    st.subheader("Train")
    non_face_image_paths = [
        'Face_Detection_folder/bieu_do.png'
    ]  # Add your actual image paths here
    for img_path in non_face_image_paths:
        img = Image.open(img_path)
        st.image(img, caption=f"Non-Face Image: {img_path}", use_column_width=True)

    
    # Part 3: Display final result
    st.title("Final Result")
    result_image_path = 'Face_Detection_folder/kq_face.png'  # Add your actual image path here
    result_image = Image.open(result_image_path)
    st.image(result_image, caption="Detection Result", use_column_width=True)

# Main app where you can call run_app3()


if __name__ == "__main__":
    run_app3()
