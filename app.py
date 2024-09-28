import streamlit as st

# Embed HTML and JavaScript for drawing
drawing_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        canvas {
            border: 1px solid black;
        }
    </style>
</head>
<body>
    <canvas id="drawingCanvas" width="600" height="400"></canvas>
    <script>
        const canvas = document.getElementById('drawingCanvas');
        const ctx = canvas.getContext('2d');
        let drawing = false;

        canvas.addEventListener('mousedown', () => {
            drawing = true;
        });

        canvas.addEventListener('mouseup', () => {
            drawing = false;
            ctx.beginPath();
        });

        canvas.addEventListener('mousemove', (event) => {
            if (!drawing) return;
            ctx.lineWidth = 5;
            ctx.lineCap = 'round';
            ctx.strokeStyle = 'red';
            ctx.lineTo(event.clientX - canvas.offsetLeft, event.clientY - canvas.offsetTop);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(event.clientX - canvas.offsetLeft, event.clientY - canvas.offsetTop);
        });
    </script>
</body>
</html>
"""

# Render the HTML in Streamlit
st.components.v1.html(drawing_html, height=500)
