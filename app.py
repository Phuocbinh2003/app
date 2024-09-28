import streamlit as st

# Initialize session state for mouse coordinates
if 'mouse_x' not in st.session_state:
    st.session_state.mouse_x = 0
if 'mouse_y' not in st.session_state:
    st.session_state.mouse_y = 0

# Create sliders to simulate mouse position
st.write("## Vị trí chuột")
x = st.slider("X", min_value=0, max_value=1000, value=st.session_state.mouse_x)
y = st.slider("Y", min_value=0, max_value=1000, value=st.session_state.mouse_y)

# Update session state with slider values
st.session_state.mouse_x = x
st.session_state.mouse_y = y

# Display the current mouse position
st.write(f"Vị trí chuột: (X: {st.session_state.mouse_x}, Y: {st.session_state.mouse_y})")
