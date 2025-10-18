from flask import Flask, request, jsonify
from flask_cors import CORS
import cloudinary.uploader
import os
import openai
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

cloudinary.config(
    cloud_name="dsunoxvya",
    api_key="979551848493753",
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


app = Flask(__name__)
CORS(app, origins=["https://projectstepagain.com"])  # Update this with your actual store domain

app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB cap

ALLOWED = {"image/jpeg", "image/png", "image/webp"}

def assess_shoe_image(image_url):
    response = client.chat.completions.create(
        model="gpt-image-1",  # assuming Groq supports this vision model
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
    return (response.choices[0].message.content)
    

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
    # gpt_feedback = assess_shoe_image(image_url)
    
    return jsonify({
        "status": "analyzed",
        "email": email,
        "image_url": image_url,
        # "gpt_feedback": gpt_feedback
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
