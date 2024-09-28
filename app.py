import streamlit as st

st.title("Theo Dõi Vị Trí Chuột trong Streamlit")

# Khởi tạo session state cho tọa độ chuột
if 'mouse_x' not in st.session_state:
    st.session_state.mouse_x = 0
if 'mouse_y' not in st.session_state:
    st.session_state.mouse_y = 0

# Hiển thị tọa độ chuột
mouse_pos_placeholder = st.empty()
mouse_pos_placeholder.write(f"Vị trí chuột: (X: {st.session_state.mouse_x}, Y: {st.session_state.mouse_y})")

# Nhập tọa độ chuột
st.sidebar.header("Nhập tọa độ chuột")
x_input = st.sidebar.number_input("Tọa độ X:", value=0)
y_input = st.sidebar.number_input("Tọa độ Y:", value=0)

# Cập nhật tọa độ chuột khi người dùng nhập
if st.sidebar.button("Cập nhật vị trí"):
    st.session_state.mouse_x = x_input
    st.session_state.mouse_y = y_input
    mouse_pos_placeholder.write(f"Vị trí chuột: (X: {st.session_state.mouse_x}, Y: {st.session_state.mouse_y})")
