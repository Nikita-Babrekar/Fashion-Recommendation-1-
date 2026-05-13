from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import uuid

from src.skin_tone_logic import get_pro_recommendation
from src.skin_tone_detect import detect_skin_tone

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- HOME ROUTE ----------------
@app.route('/')
def home():
    return "FitCheck AI Backend is running 🚀"


# ---------------- RECOMMEND ROUTE ----------------
@app.route('/recommend', methods=['POST'])
def recommend():
    filepath = None
    try:
        tone = None
        shape = None

        # ================= IMAGE MODE =================
        if 'image' in request.files:
            file = request.files['image']

            if file and file.filename != "":
                # Generate unique filename to avoid conflicts
                ext = os.path.splitext(file.filename)[1]
                unique_name = f"{uuid.uuid4()}{ext}"
                filepath = os.path.join(UPLOAD_FOLDER, unique_name)

                file.save(filepath)
                print(f"Saved image for analysis: {filepath}")

                # Detect tone using your OpenCV logic
                tone = detect_skin_tone(filepath)
                print(f"Detected Tone: {tone}")

                if tone is None:
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    return jsonify({"error": "Face not clear. Please take a better photo."}), 400

            # Get body shape from the multipart form
            shape = request.form.get("body_shape")

        # ================= MANUAL MODE =================
        elif request.is_json:
            data = request.get_json()
            tone = data.get("skin_tone")
            shape = data.get("body_shape")

        print(f"Final Processing -> Tone: {tone}, Shape: {shape}")

        # Validation
        if not tone or not shape:
            return jsonify({"error": "Missing skin tone or body shape data"}), 400

        # ================= RECOMMENDATION LOGIC =================
        results = get_pro_recommendation(tone, shape)

        # Cleanup uploaded file immediately after processing
        if filepath and os.path.exists(filepath):
            os.remove(filepath)

        # ================= STRUCTURED RESPONSE =================
        if isinstance(results, pd.DataFrame) and not results.empty:
            # We return a dictionary so the frontend can see the 'tone' AND the 'items'
            return jsonify({
                "tone": tone,
                "recommendations": results.to_dict(orient="records")
            })

        return jsonify({"error": "No recommendations found for this combination"}), 404

    except Exception as e:
        print("SYSTEM ERROR:", str(e))
        # Final cleanup safety
        if filepath and os.path.exists(filepath):
            try: os.remove(filepath)
            except: pass
        return jsonify({"error": "Internal server error. Please try again."}), 500


# ---------------- RUN APP ----------------
if __name__ == '__main__':
    # use_reloader=False prevents the 'double start' that can crash OpenCV cameras
    app.run(port=5000, debug=True, use_reloader=False)