import cv2
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas, CanvasResult

from Grabcut.grabcut import grabcut

# Khởi tạo trạng thái
def init_session_state():
    keys = ["final_mask", "result_grabcut"]
    for key in keys:
        if key not in st.session_state:
            st.session_state[key] = None

# Hướng dẫn sử dụng
def display_guide():
    st.markdown("""
        #### Hướng dẫn sử dụng
        1. Chọn ảnh cần tách nền.
        2. Chọn chế độ vẽ và độ dày nét vẽ.
        3. Vẽ hình chữ nhật lên ảnh để chọn vùng cần tách nền.
        4. Vẽ lên ảnh để chỉ định vùng cần giữ lại hoặc loại bỏ.
        5. Ấn nút `Tách nền` để xem kết quả.
    """)

# Hiển thị canvas để người dùng vẽ lên ảnh
def display_st_canvas(raw_image: Image.Image, drawing_mode: str, stroke_width: int):
    w, h = raw_image.size
    width = min(w, 475)
    height = width * h // w
    mode = "rect"
    stroke_color = "rgb(0, 0, 0)"

    if drawing_mode == "sure_bg":
        mode = "freedraw"
        stroke_color = "rgb(0, 255, 0)"
    elif drawing_mode == "sure_fg":
        mode = "freedraw"
        stroke_color = "rgb(255, 0, 0)"

    canvas_result = st_canvas(
        background_image=raw_image,
        drawing_mode=mode,
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        width=width + 1,
        height=height + 1,
        key="full_app",
    )
    return canvas_result

# Hiển thị lựa chọn chế độ vẽ và độ dày nét vẽ
def display_form_draw():
    def format_func(option):
        if option == "rect":
            return "Chọn vùng cần tách nền"
        if option == "sure_bg":
            return "Chọn vùng cần giữ lại (sure foreground)"
        return "Chọn vùng cần loại bỏ (sure background)"

    cols = st.columns(2)
    drawing_mode = cols[0].selectbox("Chọn chế độ", ["rect", "sure_bg", "sure_fg"], format_func=format_func)
    stroke_width = cols[1].slider("Độ dày nét vẽ", 1, 10, 2)
    return (drawing_mode, stroke_width)

# Xử lý thuật toán GrabCut
def process_grabcut(raw_image: Image.Image, st_canvas: CanvasResult, rects: list, true_fgs: list, true_bgs: list):
    orginal_image = np.array(raw_image)
    orginal_image = cv2.cvtColor(orginal_image, cv2.COLOR_RGBA2BGR)
    org_height, org_width = orginal_image.shape[:2]
    stc_height, stc_width = st_canvas.image_data.shape[:2]
    scale: int = org_width / stc_width
    rect = list(map(lambda x: int(x * scale), [rects[0]["left"], rects[0]["top"], rects[0]["width"], rects[0]["height"]]))

    mask = np.zeros((org_height, org_width), np.uint8)
    if st.session_state["final_mask"] is not None:
        mask = st.session_state["final_mask"]

    if len(true_fgs) > 0:
        for fg in true_fgs:
            for path in fg["path"]:
                points = np.array(path[1:])
                points = (points * scale).astype(int).reshape((-1, 2))
                if len(points) == 1:
                    mask = cv2.circle(mask, points[0], fg["strokeWidth"], cv2.GC_FGD, -1)
                else:
                    mask = cv2.polylines(mask, [points], False, cv2.GC_FGD, fg["strokeWidth"])

    if len(true_bgs) > 0:
        for bg in true_bgs:
            for path in bg["path"]:
                points = np.array(path[1:])
                points = (points * scale).astype(int).reshape((-1, 2))
                if len(points) == 1:
                    mask = cv2.circle(mask, points[0], bg["strokeWidth"], cv2.GC_BGD, -1)
                else:
                    mask = cv2.polylines(mask, [points], False, cv2.GC_BGD, bg["strokeWidth"])

    result, final_mask = grabcut(
        original_image=orginal_image,
        rect=rect,
        mask=mask,
        mode=(cv2.GC_INIT_WITH_RECT if len(true_fgs) + len(true_bgs) == 0 else cv2.GC_INIT_WITH_MASK),
    )

    st.session_state["final_mask"] = final_mask
    st.session_state["result_grabcut"] = result
    return result
