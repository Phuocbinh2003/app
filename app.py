import streamlit as st
from PIL import Image

# Cấu hình ứng dụng Streamlit
st.set_page_config(layout="wide", page_title="Tải Ảnh và Theo Dõi Vị Trí Chuột")

st.title("Tải Ảnh Lên và Theo Dõi Vị Trí Chuột")

# Sidebar để tải ảnh
st.sidebar.write("## Upload Image")
uploaded_file = st.sidebar.file_uploader("Chọn ảnh để tải lên", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Đọc ảnh
    image = Image.open(uploaded_file)
    
    # Chỉ định kích thước mới cho ảnh
    new_width = 400  # Thay đổi kích thước theo nhu cầu
    image.thumbnail((new_width, new_width))  # Giữ tỷ lệ khung hình

    # Hiển thị ảnh đã thu nhỏ
    st.image(image, caption='Ảnh đầu vào', use_column_width=False)  # Không sử dụng chiều rộng cột

    # Hiển thị kích thước ảnh
    width, height = image.size
    st.write(f"Kích thước ảnh: {width} x {height}")

    # Placeholder để hiển thị vị trí chuột
    mouse_pos_placeholder = st.empty()

    # CSS và JavaScript để theo dõi vị trí chuột
    st.markdown(f"""
        <style>
        .overlay {{
            position: absolute; /* Sử dụng absolute để phủ lên ảnh */
            top: 0;
            left: 0;
            width: {new_width}px; /* Chiều rộng của overlay bằng chiều rộng ảnh */
            height: {height}px; /* Chiều cao của overlay bằng chiều cao ảnh */
            background-color: rgba(255, 255, 255, 0);  /* Màu trong suốt */
            pointer-events: none;  /* Ngăn chặn mọi sự kiện chuột trên overlay */
            z-index: 100;  /* Đảm bảo overlay nằm trên ảnh */
        }}
        </style>
        <script>
        const img = document.querySelector("img[alt='Ảnh đầu vào']");
        
        // Theo dõi vị trí chuột
        img.addEventListener('mousemove', function(event) {{
            const rect = img.getBoundingClientRect();
            const x = Math.round(event.clientX - rect.left); // Tọa độ X trong ảnh
            const y = Math.round(event.clientY - rect.top); // Tọa độ Y trong ảnh
            
            // Gửi vị trí chuột về Streamlit
            window.parent.postMessage({{x: x, y: y}}, "*");
        }});
        </script>
        <div class="overlay"></div>
    """, unsafe_allow_html=True)

    # Cập nhật vị trí chuột từ tin nhắn
    if 'mouse_position' not in st.session_state:
        st.session_state.mouse_position = {'x': 0, 'y': 0}

    # Cập nhật vị trí chuột
    def update_mouse_position():
        mouse_pos_placeholder.write(f"Vị trí chuột trong ảnh: (X: {st.session_state.mouse_position['x']}, Y: {st.session_state.mouse_position['y']})")

    # Lắng nghe các tin nhắn từ JavaScript
    def on_message(msg):
        if 'x' in msg and 'y' in msg:
            st.session_state.mouse_position = {'x': msg['x'], 'y': msg['y']}
            update_mouse_position()

    # Đăng ký lắng nghe tin nhắn
    st.session_state.on_message = on_message

    # Gọi hàm cập nhật vị trí chuột
    update_mouse_position()
else:
    st.write("Vui lòng tải lên một bức ảnh.")
