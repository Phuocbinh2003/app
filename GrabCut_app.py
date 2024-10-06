drawing_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column; 
            align-items: center; 
        }}
        .canvas-container {{
            position: relative; 
            border: 1px solid black; 
            max-width: 100%; /* Giới hạn kích thước tối đa */
            height: auto; /* Chiều cao tự động điều chỉnh */
        }}
        canvas {{
            cursor: crosshair;
            position: absolute; 
            top: 0;
            left: 0;
            width: {img_width}px; 
            height: {img_height}px; 
            display: block; 
            z-index: 1; 
        }}
        img {{
            max-width: 100%; /* Giới hạn chiều rộng tối đa của hình ảnh */
            height: auto; /* Chiều cao tự động điều chỉnh */
            position: absolute; 
            top: 0;
            left: 0;
            z-index: 0; 
        }}
    </style>
</head>
<body>
    <div class="canvas-container">
        <img id="originalImage" src="data:image/png;base64,{convert_image_to_base64(image)}" />
        <canvas id="drawingCanvas" width="{img_width}" height="{img_height}"></canvas>
    </div>
    <script>
        const canvas = document.getElementById('drawingCanvas');
        const ctx = canvas.getContext('2d');
        const img = document.getElementById('originalImage');

        let drawing = false;
        let startX, startY;
        let hasDrawnRectangle = false; 

        canvas.addEventListener('mousedown', (event) => {{
            if (event.button === 0 && !hasDrawnRectangle) {{
                drawing = true;
                startX = event.offsetX;
                startY = event.offsetY;
            }}
            event.preventDefault();
        }});

        canvas.addEventListener('mouseup', (event) => {{
            if (drawing) {{
                drawing = false;
                const endX = event.offsetX;
                const endY = event.offsetY;
                const width = Math.abs(startX - endX);
                const height = Math.abs(startY - endY);
                
                const size = Math.min(width, height);

                ctx.clearRect(0, 0, canvas.width, canvas.height); 
                ctx.rect(startX, startY, size, size); 
                ctx.strokeStyle = 'blue';
                ctx.lineWidth = 2;
                ctx.stroke();

                const rect = {{ x: Math.min(startX, endX), y: Math.min(startY, endY), width: size, height: size }};
                hasDrawnRectangle = true;
                console.log("Sending rectangle data:", rect); 
                window.parent.postMessage(JSON.stringify({{ type: 'rect_data', rect }}), '*');
            }}
        }});

        canvas.addEventListener('mousemove', (event) => {{
            if (drawing) {{
                event.preventDefault();
            }}
        }});
    </script>
</body>
</html>
"""
