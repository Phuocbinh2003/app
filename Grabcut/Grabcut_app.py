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
init_session_state()
st.set_page_config(
    page_title="Ứng dụng tách nền bằng thuật toán GrabCut",
    layout="wide",
    initial_sidebar_state="expanded",
)

def run_app1():
    st.title("Ứng dụng tách nền bằng thuật toán GrabCut")
    
    with st.container(border=True):
        display_guide()
    
    with st.container(border=True):
        uploaded_image = st.file_uploader(
            ":material/image: Chọn hoặc kéo ảnh vào ô bên dưới", type=["jpg", "jpeg", "png"]
        )
    
    # Giữ chế độ vẽ đã chọn và độ dày nét vẽ
    if 'drawing_mode' not in st.session_state:
        st.session_state['drawing_mode'] = "rect"  # Chế độ vẽ mặc định là hình chữ nhật

    if 'stroke_width' not in st.session_state:
        st.session_state['stroke_width'] = 3  # Độ dày nét vẽ mặc định là 3

    if uploaded_image is not None:
        with st.container(border=True):
            drawing_mode = st.session_state['drawing_mode']
            stroke_width = st.session_state['stroke_width']

        with st.container(border=True):
            cols = st.columns(2, gap="large")
            raw_image = Image.open(uploaded_image)
    
            with cols[0]:
                canvas_result = display_st_canvas(raw_image, drawing_mode, stroke_width)
                rects, true_fgs, true_bgs = get_object_from_st_canvas(canvas_result)

                # Cập nhật trạng thái nếu đã vẽ hình chữ nhật
                if len(rects) > 0:
                    st.session_state["rect_drawn"] = True
                else:
                    st.session_state["rect_drawn"] = False

            # Reset trạng thái khi không có hình chữ nhật nào được vẽ
            if len(rects) < 1:
                st.session_state["result_grabcut"] = None
                st.session_state["final_mask"] = None
                st.session_state["rect_drawn"] = False
            elif len(rects) > 1:
                st.warning("Chỉ được chọn một vùng cần tách nền.")
            else:
                with cols[0]:
                    submit_btn = st.button(
                        ":material/settings_timelapse: Tách nền",
                    )
    
                if submit_btn:
                    if len(rects) > 1:
                        st.warning("Chỉ được chọn một hình chữ nhật để tách nền.")
                    else:
                        with st.spinner("Đang xử lý..."):
                            result = process_grabcut(
                                raw_image, canvas_result, rects, true_fgs, true_bgs
                            )
                            cols[1].image(result, channels="BGR", caption="Ảnh kết quả")
                elif st.session_state["result_grabcut"] is not None:
                    cols[1].image(
                        st.session_state["result_grabcut"],
                        channels="BGR",
                        caption="Ảnh kết quả",
                    )

if __name__ == "__main__":
    run_app1()
