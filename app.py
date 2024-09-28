import streamlit as st
import numpy as np
from PIL import Image

# Cấu hình trang Streamlit
st.set_page_config(layout="wide", page_title="Mouse Position Tracking")

st.write("# Theo dõi vị trí chuột trên hình ảnh")

# Sidebar để tải ảnh
st.sidebar.write("## Upload Image")
uploaded_file = st.sidebar.file_uploader("", type=["jpg", "jpeg", "png"])

# Khởi tạo session_state nếu chưa có
if 'mouse_in_image' not in st.session_state:
    st.session_state.mouse_in_image = False

if uploaded_file is not None:
    # Đọc ảnh
    image = Image.open(uploaded_file)
    image = np.array(image)

    # Hiển thị ảnh với lớp CSS cho con trỏ
    st.image(image, caption='Ảnh đầu vào', use_column_width=True)

    # JavaScript để theo dõi sự kiện chuột di chuyển vào và ra khỏi ảnh
    st.markdown("""
        <script>
        const img = document.querySelector('img');
        img.addEventListener('mouseenter', function() {
            // Cập nhật giá trị session_state chuột vào ảnh
            window.parent.postMessage({ type: 'mouse_in', value: true }, '*');
        });

        img.addEventListener('mouseleave', function() {
            // Cập nhật giá trị session_state chuột ra khỏi ảnh
            window.parent.postMessage({ type: 'mouse_in', value: false }, '*');
        });
        </script>
    """, unsafe_allow_html=True)

    # JavaScript gửi dữ liệu lên session_state thông qua postMessage API
    st.markdown("""
        <script>
        window.addEventListener('message', (event) => {
            if (event.data.type === 'mouse_in') {
                let mouseState = event.data.value;
                // Cập nhật trạng thái trong session_state
                window.parent.streamlitApi.setComponentValue(mouseState);
            }
        });
        </script>
    """, unsafe_allow_html=True)

    # Kiểm tra trạng thái session_state và hiển thị
    if st.session_state.mouse_in_image:
        st.write("Đã vào bức ảnh")
    else:
        st.write("Chưa vào bức ảnh")
