import streamlit as st

# Initialize session state for mouse coordinates
if 'mouse_x' not in st.session_state:
    st.session_state.mouse_x = 0
if 'mouse_y' not in st.session_state:
    st.session_state.mouse_y = 0

# Create a placeholder for mouse position display
mouse_pos_placeholder = st.empty()

# JavaScript to track mouse position and send it to Streamlit
mouse_tracking_code = """
<script>
    document.addEventListener('mousemove', function(event) {
        // Send mouse coordinates to Streamlit
        const x = event.clientX;
        const y = event.clientY;

        // Update the Streamlit app with the mouse position
        const data = {x: x, y: y};
        window.parent.streamlit.setMousePosition(data);
    });
</script>
"""

# Add the JavaScript to the app
st.markdown(mouse_tracking_code, unsafe_allow_html=True)

# Function to update mouse position in session state
def update_mouse_position(data):
    st.session_state.mouse_x = data['x']
    st.session_state.mouse_y = data['y']

# Display the current mouse position
if 'mouse_position' not in st.session_state:
    st.session_state.mouse_position = {'x': 0, 'y': 0}

# Continuously update the display of mouse position
while True:
    # Use a callback to update mouse position
    if 'mouse_position' in st.session_state:
        mouse_pos_placeholder.write(f"Vị trí chuột: (X: {st.session_state.mouse_x}, Y: {st.session_state.mouse_y})")

    # Allow Streamlit to rerun
    st.experimental_rerun()
