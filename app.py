from flask import Flask, request, jsonify
from flask_cors import CORS
import cloudinary.uploader
import os
import random
from openai import OpenAI

# Constants
CODES_FILE = "codes.txt"

# Initialize OpenAI client (Groq)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

# Configure Cloudinary
cloudinary.config(
    cloud_name="dsunoxvya",
    api_key="979551848493753",
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Flask app setup
app = Flask(__name__)
CORS(app, origins=["https://projectstepagain.com"])
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB limit

ALLOWED = {"image/jpeg", "image/png", "image/webp"}

def assess_shoe_image(image_url):
    response = client.chat.completions.create(
        model="gpt-image-1",  # Make sure Groq supports this
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Is the image below a shoe? Please answer yes or no."},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ],
        max_tokens=10,
    )
    return response.choices[0].message.content.strip()

@app.post("/proxy/donate-upload")
def donate_upload():
    email = request.form.get("email", "").strip()
    file = request.files.get("shoe_photo")

    if not email or not file:
        return jsonify({"status": "error", "message": "email and image required"}), 400
    if file.mimetype not in ALLOWED:
        return jsonify({"status": "error", "message": "invalid file type"}), 400

    # Upload image to Cloudinary
    upload_result = cloudinary.uploader.upload(file)
    image_url = upload_result["secure_url"]

    # gpt_feedback = assess_shoe_image(image_url)

    # Load discount codes from file
    try:
        with open(CODES_FILE, "r") as f:
            codes = f.read().strip().split(",")
    except FileNotFoundError:
        return jsonify({"status": "error", "message": "codes file not found"}), 500

    if not codes or codes[0] == "":
        return jsonify({"status": "error", "message": "no more discount codes available"}), 500

    discount_code = codes[0]
    codes.remove(discount_code)

    # Save the updated code list
    with open(CODES_FILE, "w") as f:
        f.write(",".join(codes))

    return jsonify({
        "status": "analyzed",
        "email": email,
        "image_url": image_url,
        # "gpt_feedback": gpt_feedback,
        "discount_code": discount_code
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
