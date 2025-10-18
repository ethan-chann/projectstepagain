from flask import Flask, request, jsonify

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB cap

ALLOWED = {"image/jpeg", "image/png", "image/webp"}

@app.post("/proxy/donate-upload")
def donate_upload():
    print("UPLOAD DETECTED")
    email = request.form.get("email", "").strip()
    file = request.files.get("shoe_photo")  # <-- werkzeug FileStorage

    if not email or not file:
        return jsonify({"status": "error", "message": "email and image required"}), 400
    if file.mimetype not in ALLOWED:
        return jsonify({"status": "error", "message": "invalid file type"}), 400

    # Store in a variable (bytes in memory)
    image_bytes = file.read()              # <-- your image data as bytes
    filename = file.filename               # optional: original name
    mime = file.mimetype                   # optional: content type

    # Example: confirm size to prove we got it
    size = len(image_bytes)

    # If you plan to also save later, you already have bytes.
    # If you need to re-use the FileStorage stream again:
    # file.stream.seek(0)

    return jsonify({
        "status": "received",
        "email": email,
        "filename": filename,
        "mime": mime,
        "bytes": size
    }), 200

if __name__ == "__main__":
    app.run(port=5000)
