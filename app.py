from flask import Flask, request, send_file, render_template_string
import requests
import os

app = Flask(__name__)

# HTML template for user to enter video URL with added CSS styles
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Video Downloader</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: white;
            padding: 20px;
            width: 400px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        h1 {
            color: #333;
        }
        form {
            margin-top: 20px;
        }
        input[type="text"] {
            padding: 10px;
            width: 80%;
            margin: 10px 0;
            outline: none;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            padding: 10px 20px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #0056b3;
        }
        a {
            color: #007BFF;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        p {
            margin-top: 20px;
            color: green;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Video Downloader</h1>
        <form method="POST" action="/download">
            <input type="text" id="video_url" name="video_url" placeholder="Enter Video URL" required>
            <br>
            <button type="submit">Download Video</button>
        </form>
        {% if video_ready %}
            <p>Video is ready. <a href="{{ url_for('download_video') }}">Click here to download</a></p>
        {% endif %}
    </div>
</body>
</html>
"""

# Route for homepage
@app.route('/')
def index():
    return render_template_string(html_template)

# Route to handle the video download request
@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    video_path = "downloaded_video.mp4"
    
    # Download the video using requests
    try:
        response = requests.get(video_url)
        if response.status_code == 200:
            # Save the video to a file
            with open(video_path, "wb") as video_file:
                video_file.write(response.content)
            return render_template_string(html_template, video_ready=True)
        else:
            return f"Failed to download video. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Route to serve the downloaded video file
@app.route('/download_video')
def download_video():
    video_path = "downloaded_video.mp4"
    
    if os.path.exists(video_path):
        return send_file(video_path, as_attachment=True)
    else:
        return "Video not found!"

if __name__ == '__main__':
    app.run(debug=True)
