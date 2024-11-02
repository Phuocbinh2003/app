import streamlit as st
from PIL import Image
from Grabcut.grabcut_processor import (
    display_form_draw,
    display_guide,
    display_st_canvas,
    init_session_state,
    process_grabcut,
)
from Grabcut.ultis import get_object_from_st_canvas

# Thiết lập cấu hình trang phải đặt ở đầu tiên
st.set_page_config(
    page_title="Ứng dụng tách nền bằng thuật toán GrabCut",
    layout="wide",
    initial_sidebar_state="expanded",
)

def run_app1():
    init_session_state()
    
    st.title("Ứng dụng tách nền bằng thuật toán GrabCut")
    
    with st.container():
        display_guide()
    
    uploaded_image = st.file_uploader("Chọn hoặc kéo ảnh vào ô bên dưới", type=["jpg", "jpeg", "png"])
    
    if uploaded_image is not None:
        drawing_mode, stroke_width = display_form_draw()
        cols = st.columns(2, gap="large")
        raw_image = Image.open(uploaded_image)
    
        with cols[0]:
            canvas_result = display_st_canvas(raw_image, drawing_mode, stroke_width)
            rects, true_fgs, true_bgs = get_object_from_st_canvas(canvas_result)
    
        if len(rects) < 1:
            st.session_state["result_grabcut"] = None
            st.session_state["final_mask"] = None
            st.warning("Vui lòng vẽ một hình chữ nhật để chọn vùng cần tách nền.")
        elif len(rects) > 1:
            st.warning("Chỉ được chọn một vùng cần tách nền.")
        else:
            with cols[1]:
                result = process_grabcut(raw_image, canvas_result, rects, true_fgs, true_bgs)
                st.image(result, caption="Ảnh sau khi tách nền", use_column_width="always")
    else:
        st.info("Vui lòng tải lên một bức ảnh để bắt đầu.")

if __name__ == "__main__":
    run_app1()
