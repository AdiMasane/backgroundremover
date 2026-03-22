from flask import Flask, render_template, request, send_file
from rembg import remove, new_session
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 🔥 Load model ONLY ONCE (important)
session = new_session("u2netp")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/remove", methods=["POST"])
def remove_bg():
    if "image" not in request.files:
        return "No file uploaded"

    file = request.files["image"]

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(UPLOAD_FOLDER, "output.png")

    file.save(input_path)

    # Open image
    input_image = Image.open(input_path)

    # ⚡ Resize for speed
    input_image = input_image.resize((512, 512))

    # 🚀 Background removal
    output_image = remove(input_image, session=session)

    # Save output
    output_image.save(output_path)

    return send_file(output_path, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)