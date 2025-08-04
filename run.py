from flask import Flask, request, render_template, send_file
import instaloader
import os

app = Flask(__name__)

# Create an Instaloader instance
L = instaloader.Instaloader()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        # Extract shortcode from URL
        shortcode = url.split("/")[-2]
        
        # Download the post
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        # Download video
        L.download_post(post, target=shortcode)
        
        # Find the video file
        video_file = None
        for f in os.listdir(shortcode):
            if f.endswith(".mp4"):
                video_file = os.path.join(shortcode, f)
                break
        
        if video_file:
            return send_file(video_file, as_attachment=True)
        else:
            return "Could not find the downloaded video."

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
