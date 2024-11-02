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
    
    # Tải ảnh lên
    uploaded_image = st.file_uploader("Chọn hoặc kéo ảnh vào ô bên dưới", type=["jpg", "jpeg", "png"])
    
    if uploaded_image is not None:
        # Mở ảnh và chuyển sang định dạng RGB để đảm bảo màu sắc chính xác
        raw_image = Image.open(uploaded_image).convert("RGB")
        
        # Thiết lập độ dày nét vẽ mặc định là 3 trong hàm display_form_draw()
        drawing_mode, stroke_width = display_form_draw()
        
        # Hiển thị canvas với ảnh đã tải lên và đặt nét vẽ mặc định là 3
        canvas_result = display_st_canvas(raw_image, drawing_mode, stroke_width=3)
        
        # Lấy các đối tượng từ canvas
        rects, true_fgs, true_bgs = get_object_from_st_canvas(canvas_result)
    
        # Xử lý tách nền và hiển thị ảnh kết quả
        if len(rects) > 0:
            result = process_grabcut(raw_image, canvas_result, rects, true_fgs, true_bgs)
            st.image(result, caption="Ảnh sau khi tách nền", use_column_width=True)

if __name__ == "__main__":
    run_app1()
