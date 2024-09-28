import streamlit as st

# Initialize session state for mouse coordinates
if 'mouse_x' not in st.session_state:
    st.session_state.mouse_x = 0
if 'mouse_y' not in st.session_state:
    st.session_state.mouse_y = 0

# Create a placeholder for mouse position display
mouse_pos_placeholder = st.empty()

# JavaScript to track mouse position
st.markdown("""
    <script>
    document.addEventListener('mousemove', function(event) {
        const x = event.clientX;
        const y = event.clientY;
        
        // Use Streamlit's method to update mouse position
        window.parent.streamlit.setMousePosition({x: x, y: y});
    });
    </script>
""", unsafe_allow_html=True)

# Display the current mouse position
def display_mouse_position():
    mouse_pos_placeholder.write(f"Vị trí chuột: (X: {st.session_state.mouse_x}, Y: {st.session_state.mouse_y})")

# Update the mouse position when the function is called
def update_mouse_position(data):
    st.session_state.mouse_x = data['x']
    st.session_state.mouse_y = data['y']
    display_mouse_position()

# Use a Streamlit widget to keep the app responsive
st.selectbox("Choose an option", ["Option 1", "Option 2"])  # This keeps the app running

# Call the function to update the mouse position
if st.button('Get Mouse Position'):
    update_mouse_position({'x': st.session_state.mouse_x, 'y': st.session_state.mouse_y})
