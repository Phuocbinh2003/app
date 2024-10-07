import streamlit as st
import cv2 as cv
import numpy as np
from grabcut_processor import GrabCutProcessor

def run_app1():
    st.title("GrabCut Application")
    
    # Upload image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
    if uploaded_file is not None:
        # Read image
        image = cv.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
        processor = GrabCutProcessor(image)
        
        # Initialize variables
        rect = (0, 0, 1, 1)
        
        # Drawing options
        drawing_option = st.selectbox("Choose drawing value", ["Foreground", "Background", "Probable Foreground", "Probable Background"])
        processor.set_drawing_value(drawing_option)
        
        # Display image
        st.image(processor.img_copy, channels="BGR")

        # Draw rectangle or mask
        if st.button("Apply GrabCut"):
            if rect != (0, 0, 1, 1):  # Ensure a rectangle is defined
                output_image = processor.apply_grabcut(rect)
                st.image(output_image, channels="BGR", caption="GrabCut Output")
            else:
                st.warning("Please define a rectangle before applying GrabCut.")
        
        # Save mask
        if st.button("Save Mask"):
            mask = processor.save_mask()
            st.success("Mask saved!")

        # Reload image
        if st.button("Reload Image"):
            processor.reload_image()
            st.image(processor.img_copy, channels="BGR", caption="Reloaded Image")
        
        # Export result
        if st.button("Export Result"):
            filename = st.text_input("Enter filename (with .png):", "output.png")
            if filename:
                processor.export_result(filename)
                st.success(f"Result exported as {filename}")

# Main function to run the application
if __name__ == "__main__":
    run_app1()
