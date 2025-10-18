from flask import Flask, request, jsonify
from flask_cors import CORS
import cloudinary.uploader

cloudinary.config(
    cloud_name="projectstepagain",
    api_key="979551848493753",
    api_secret=""
)

app = Flask(__name__)
CORS(app, origins=["https://projectstepagain.com"])  # Update this with your actual store domain

app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB cap

ALLOWED = {"image/jpeg", "image/png", "image/webp"}

@app.post("/proxy/donate-upload")
def donate_upload():
    print("UPLOAD DETECTED")
    email = request.form.get("email", "").strip()
    file = request.files.get("shoe_photo")

    if not email or not file:
        return jsonify({"status": "error", "message": "email and image required"}), 400
    if file.mimetype not in ALLOWED:
        return jsonify({"status": "error", "message": "invalid file type"}), 400

    image_bytes = file.read()
    filename = file.filename
    mime = file.mimetype
    size = len(image_bytes)

    return jsonify({
        "status": "received",
        "email": email,
        "filename": filename,
        "mime": mime,
        "bytes": size
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
