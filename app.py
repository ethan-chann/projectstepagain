from flask import Flask, request, jsonify
from flask_cors import CORS
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name="dsunoxvya",
    api_key="979551848493753",
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

app = Flask(__name__)
CORS(app, origins=["https://projectstepagain.com"])  # Update this with your actual store domain

app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB cap

ALLOWED = {"image/jpeg", "image/png", "image/webp"}

@app.post("/proxy/donate-upload")
def donate_upload():
    email = request.form.get("email", "").strip()
    file = request.files.get("shoe_photo")

    if not email or not file:
        return jsonify({"status": "error", "message": "email and image required"}), 400
    if file.mimetype not in ALLOWED:
        return jsonify({"status": "error", "message": "invalid file type"}), 400

    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(file)

    image_url = upload_result["secure_url"]

    # At this point, we can send image_url to GPT
    return jsonify({
        "status": "uploaded",
        "email": email,
        "image_url": image_url
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
