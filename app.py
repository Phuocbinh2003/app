import streamlit as st

# Initialize session state for mouse coordinates
if 'mouse_x' not in st.session_state:
    st.session_state.mouse_x = 0
if 'mouse_y' not in st.session_state:
    st.session_state.mouse_y = 0

# Function to update mouse position using Streamlit's session state
def update_mouse_position(x, y):
    st.session_state.mouse_x = x
    st.session_state.mouse_y = y

# Create a placeholder for mouse position display
mouse_pos_placeholder = st.empty()

# JavaScript to track mouse position
mouse_tracking_code = """
<script>
    document.addEventListener('mousemove', function(event) {
        // Send mouse coordinates to Streamlit
        const x = event.clientX;
        const y = event.clientY;

        // Use Streamlit's method to update mouse position
        window.parent.streamlit.setMousePosition(x, y);
    });
</script>
"""

# Add the JavaScript to the app
st.markdown(mouse_tracking_code, unsafe_allow_html=True)

# Display the current mouse position
while True:
    # Update the mouse position in the Streamlit session state
    if 'mouse_x' in st.session_state and 'mouse_y' in st.session_state:
        mouse_pos_placeholder.write(f"Vị trí chuột: (X: {st.session_state.mouse_x}, Y: {st.session_state.mouse_y})")

    # Allow Streamlit to rerun
    st.experimental_rerun()
