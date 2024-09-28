import streamlit as st

# Function to update mouse position
def mouse_position():
    st.session_state.mouse_x = st.session_state.get('mouse_x', 0)
    st.session_state.mouse_y = st.session_state.get('mouse_y', 0)

# Create a placeholder for mouse position display
mouse_pos_placeholder = st.empty()

# JavaScript to track mouse position
mouse_tracking_code = """
<script>
    document.addEventListener('mousemove', function(event) {
        // Send mouse coordinates to Streamlit
        window.parent.streamlit.setMousePosition(event.clientX, event.clientY);
    });
</script>
"""

# Add the JavaScript to the app
st.markdown(mouse_tracking_code, unsafe_allow_html=True)

# Create the function to update mouse position in Streamlit
st.session_state.mouse_x = 0
st.session_state.mouse_y = 0

# Run the function to update mouse position
if 'mouse_x' in st.session_state and 'mouse_y' in st.session_state:
    mouse_position()

# Display the current mouse position
mouse_pos_placeholder.write(f"Vị trí chuột: (X: {st.session_state.mouse_x}, Y: {st.session_state.mouse_y})")
