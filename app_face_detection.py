import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image

def run_app3():
    # Part 1: Display face and non-face images
    st.title("Face and Non-face Data")
    
    st.subheader("Face Images")
    face_image_paths = [
        'Face_Detection_folder/faces_24x24.png', 
        'Face_Detection_folder/non_faces_24x24.png'
    ]  # Add your actual image paths here
    for img_path in face_image_paths:
        img = Image.open(img_path)
        st.image(img, caption=f"Face Image: {img_path}", use_column_width=True)

    st.subheader("Non-Face Images")
    non_face_image_paths = [
        'path_to_non_face_image_1.jpg', 
        'path_to_non_face_image_2.jpg'
    ]  # Add your actual image paths here
    for img_path in non_face_image_paths:
        img = Image.open(img_path)
        st.image(img, caption=f"Non-Face Image: {img_path}", use_column_width=True)

    # Part 2: Display training results and vector image
    st.title("Training Results")
    st.subheader("Training Accuracy for Different `n_neighbors`")
    n_neighbors = range(1, 11)
    accuracy = [0.85, 0.87, 0.89, 0.90, 0.88, 0.86, 0.91, 0.93, 0.92, 0.94]  # Example accuracies

    plt.figure(figsize=(10, 5))
    plt.plot(n_neighbors, accuracy, marker='o', linestyle='-', color='b')
    plt.title('KNN Accuracy vs n_neighbors')
    plt.xlabel('n_neighbors')
    plt.ylabel('Accuracy')
    plt.grid(True)
    st.pyplot(plt)

    st.subheader("Vector Representation Image")
    vector_image_path = 'path_to_vector_image.jpg'  # Add your actual image path here
    vector_image = Image.open(vector_image_path)
    st.image(vector_image, caption="Vector Representation", use_column_width=True)

    # Part 3: Display final result
    st.title("Final Result")
    result_image_path = 'path_to_final_result_image.jpg'  # Add your actual image path here
    result_image = Image.open(result_image_path)
    st.image(result_image, caption="Detection Result", use_column_width=True)

# Main app where you can call run_app3()


if __name__ == "__main__":
    run_app3()
