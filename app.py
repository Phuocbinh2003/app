import streamlit as st
from PIL import Image

# Cấu hình ứng dụng Streamlit
st.set_page_config(layout="wide", page_title="Tải Ảnh và Vẽ Bounding Box")

st.title("Tải Ảnh Lên và Vẽ Bounding Box")

# Sidebar để tải ảnh
st.sidebar.write("## Upload Image")
uploaded_file = st.sidebar.file_uploader("Chọn ảnh để tải lên", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Đọc ảnh
    image = Image.open(uploaded_file)
    st.image(image, caption='Ảnh đầu vào', use_column_width=True)

    # Hiển thị kích thước ảnh
    width, height = image.size
    st.write(f"Kích thước ảnh: {width} x {height}")

    # Placeholder để hiển thị vị trí chuột
    mouse_pos_placeholder = st.empty()

    # Thông tin về bounding box
    st.session_state.bounding_boxes = []

    # CSS và JavaScript để theo dõi vị trí chuột, vẽ bounding box và ngăn chặn sự kiện nhấp chuột
    st.markdown(f"""
        <style>
        .overlay {{
            position: absolute; /* Sử dụng absolute để phủ lên ảnh */
            top: 0; /* Đẩy lên 0 */
            left: 0; /* Đẩy sang trái 0 */
            width: 100%; /* Chiều rộng của overlay 100% */
            height: 100%; /* Chiều cao của overlay 100% */
            background-color: rgba(255, 255, 255, 0); /* Trong suốt */
            pointer-events: all; /* Cho phép nhận sự kiện chuột */
            z-index: 100; /* Đảm bảo overlay nằm trên tất cả */
        }}
        img {{
            pointer-events: none; /* Ngăn chặn mọi sự kiện chuột trên ảnh */
            user-select: none; /* Ngăn chặn việc chọn văn bản */
            -webkit-user-drag: none; /* Ngăn chặn kéo ảnh trên Safari */
            -moz-user-select: none; /* Ngăn chặn kéo ảnh trên Firefox */
            -ms-user-select: none; /* Ngăn chặn kéo ảnh trên IE */
        }}
        </style>
        <script>
        const img = document.querySelector("img[alt='Ảnh đầu vào']");
        let isDrawing = false;
        let startX = 0;
        let startY = 0;

        // Ngăn chặn kéo ảnh mặc định
        img.addEventListener('dragstart', function(event) {{
            event.preventDefault();
        }});

        // Theo dõi vị trí chuột
        img.addEventListener('mousemove', function(event) {{
            const rect = img.getBoundingClientRect();
            const x = Math.round(event.clientX - rect.left); // Tọa độ X trong ảnh
            const y = Math.round(event.clientY - rect.top); // Tọa độ Y trong ảnh
            
            // Gửi vị trí chuột về Streamlit
            window.parent.postMessage({{x: x, y: y}}, "*");

            // Nếu đang vẽ, cập nhật bounding box
            if (isDrawing) {{
                drawBox(startX, startY, x, y);
            }}
        }});

        // Bắt đầu vẽ khi nhấn chuột trái
        img.addEventListener('mousedown', function(event) {{
            if (event.button === 0) {{ // Kiểm tra nếu chuột trái được nhấn
                isDrawing = true;
                const rect = img.getBoundingClientRect();
                startX = Math.round(event.clientX - rect.left); // Vị trí bắt đầu X
                startY = Math.round(event.clientY - rect.top); // Vị trí bắt đầu Y
            }}
        }});

        // Kết thúc vẽ khi nhả chuột
        img.addEventListener('mouseup', function(event) {{
            if (isDrawing) {{
                isDrawing = false;
                const rect = img.getBoundingClientRect();
                const endX = Math.round(event.clientX - rect.left);
                const endY = Math.round(event.clientY - rect.top);
                
                // Ghi nhận bounding box
                window.parent.postMessage({{
                    action: 'saveBox',
                    box: {{ startX: startX, startY: startY, endX: endX, endY: endY }}
                }}, "*");
            }}
        }});

        function drawBox(startX, startY, endX, endY) {{
            const overlay = document.querySelector('.overlay');
            overlay.innerHTML = ''; // Xóa bounding box cũ
            const box = document.createElement('div');
            box.style.position = 'absolute';
            box.style.border = '2px solid red';
            box.style.left = Math.min(startX, endX) + 'px';
            box.style.top = Math.min(startY, endY) + 'px';
            box.style.width = Math.abs(endX - startX) + 'px';
            box.style.height = Math.abs(endY - startY) + 'px';
            overlay.appendChild(box);
        }
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
        if 'action' in msg and msg['action'] == 'saveBox':
            st.session_state.bounding_boxes.append(msg['box'])  # Lưu bounding box

    # Đăng ký lắng nghe tin nhắn
    st.session_state.on_message = on_message

    # Gọi hàm cập nhật vị trí chuột
    update_mouse_position()

    # Hiển thị bounding boxes
    if st.session_state.bounding_boxes:
        for box in st.session_state.bounding_boxes:
            st.markdown(f"Bounding Box: Từ ({box['startX']}, {box['startY']}) đến ({box['endX']}, {box['endY']})")
else:
    st.write("Vui lòng tải lên một bức ảnh.")
