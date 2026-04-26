from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# ── Load model once at startup ────────────────────────────────────
print("Loading model...")
model = tf.keras.models.load_model("/Users/rudranshgarg/FarmTech/phase4_best.keras")
print("Model loaded successfully!")

CLASS_NAMES = ["blast", "healthy", "insect", "leaf_folder",
               "scald", "stripes", "tungro"]

IMG_SIZE = 224

SEVERITY_THRESHOLDS = {
    "blast":       {"Low": 0.50, "Medium": 0.72},
    "insect":      {"Low": 0.45, "Medium": 0.65},
    "leaf_folder": {"Low": 0.45, "Medium": 0.65},
    "scald":       {"Low": 0.48, "Medium": 0.68},
    "stripes":     {"Low": 0.50, "Medium": 0.70},
    "tungro":      {"Low": 0.50, "Medium": 0.72},
}

PREVENTION = {
    "blast": {
        "Low": [
            "Avoid excess nitrogen fertilizer",
            "Ensure adequate field drainage",
            "Monitor closely — blast spreads rapidly in wet weather",
        ],
        "Medium": [
            "Spray Tricyclazole 75 WP @ 0.6 g/L water",
            "Spray Isoprothiolane 40 EC @ 1.5 ml/L water",
            "Maintain flood depth in paddy fields",
            "Avoid overhead irrigation",
        ],
        "High": [
            "URGENT: Apply Propiconazole 25 EC @ 1 ml/L immediately",
            "Repeat spray after 7-10 days",
            "Remove and burn heavily infected crop debris",
            "Do NOT grow susceptible varieties next season",
            "Consult your local agricultural officer",
        ],
    },
    "tungro": {
        "Low": [
            "Control leafhopper population with yellow sticky traps",
            "Remove infected plants from the field",
            "Avoid late planting when leafhopper populations are high",
        ],
        "Medium": [
            "Apply imidacloprid 17.8 SL @ 0.3 ml/L to control leafhoppers",
            "Remove and destroy infected plants within 1-meter radius",
            "Avoid planting next to older infected fields",
        ],
        "High": [
            "URGENT: No cure exists — tungro is viral",
            "Remove and destroy ALL infected plants immediately",
            "Apply systemic insecticide to eliminate leafhopper vectors",
            "Consider replanting with tungro-resistant varieties (TN1, IR36)",
            "Consult agricultural officer for field quarantine assessment",
        ],
    },
    "scald": {
        "Low": [
            "Improve field drainage — scald thrives in waterlogged conditions",
            "Balance potassium and silicon fertilizer levels",
            "Avoid dense planting — improve air circulation",
        ],
        "Medium": [
            "Apply Mancozeb 75 WP @ 2 g/L water",
            "Spray Iprodione 50 WP @ 1 g/L",
            "Reduce nitrogen application rate",
        ],
        "High": [
            "URGENT: Spray Propiconazole 25 EC @ 1 ml/L",
            "Drain field and allow soil to dry for 2-3 days",
            "Remove heavily infected leaves and burn",
            "Do not use infected straw as mulch",
        ],
    },
    "stripes": {
        "Low": [
            "Monitor for planthopper activity — stripes virus is vector-borne",
            "Apply yellow sticky traps to catch planthoppers",
            "Remove visibly striped seedlings",
        ],
        "Medium": [
            "Apply thiamethoxam 25 WG @ 0.2 g/L to control planthoppers",
            "Remove infected plants in a 2-meter radius",
            "Avoid over-application of nitrogen (attracts planthoppers)",
        ],
        "High": [
            "URGENT: No chemical cure for stripe virus",
            "Remove and destroy all infected plants",
            "Apply systemic insecticide to eliminate planthopper vectors",
            "Plant resistant varieties (IR64, IR72) next season",
            "Coordinate with neighbouring farmers — stripe virus spreads across fields",
        ],
    },
    "insect": {
        "Low": [
            "Monitor insect population — manual inspection every 3 days",
            "Use yellow sticky traps as early warning",
            "Encourage natural predators (spiders, parasitic wasps)",
        ],
        "Medium": [
            "Apply neem-based biopesticide (Azadirachtin 0.03%) @ 5 ml/L",
            "Use targeted spray — avoid broad-spectrum pesticides if possible",
            "Check underneath leaves — most pests feed on the lower surface",
        ],
        "High": [
            "URGENT: Apply chlorpyrifos 20 EC @ 2 ml/L or cypermethrin 10 EC @ 1 ml/L",
            "Spray in early morning or late evening to reduce bee impact",
            "Repeat after 7 days if infestation persists",
            "Consider pheromone traps for long-term pest management",
        ],
    },
    "leaf_folder": {
        "Low": [
            "Crush folded leaves by hand to kill larvae inside",
            "Release Trichogramma egg parasitoids if available",
            "Ensure proper plant spacing for air circulation",
        ],
        "Medium": [
            "Apply chlorantraniliprole 18.5 SC @ 0.3 ml/L",
            "Spray during early evening when adults are active",
            "Remove and destroy rolled leaves with larvae",
        ],
        "High": [
            "URGENT: Apply cartap hydrochloride 50 SP @ 1 g/L",
            "Spray every 7 days until infestation is controlled",
            "Drain field for 2 days to stress larvae",
            "Coordinate with neighboring fields — leaf folder moths migrate",
        ],
    },
    "healthy": {
        "Low":    ["No action needed. Your rice plant looks healthy!"],
        "Medium": ["No action needed. Your rice plant looks healthy!"],
        "High":   ["No action needed. Your rice plant looks healthy!"],
    },
}


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    try:
        file   = request.files["image"]
        img    = Image.open(io.BytesIO(file.read())).convert("RGB")
        img    = img.resize((IMG_SIZE, IMG_SIZE), Image.BILINEAR)
        arr    = np.array(img, dtype=np.float32)
        tensor = np.expand_dims(arr, axis=0)

        probs      = model.predict(tensor, verbose=0)[0]
        class_idx  = int(np.argmax(probs))
        disease    = CLASS_NAMES[class_idx]
        confidence = float(probs[class_idx]) * 100

        if disease != "healthy":
            thresh = SEVERITY_THRESHOLDS.get(disease, {"Low": 0.5, "Medium": 0.7})
            conf   = confidence / 100
            if   conf < thresh["Low"]:    severity = "Low"
            elif conf < thresh["Medium"]: severity = "Medium"
            else:                         severity = "High"
        else:
            severity = "Low"

        prevention    = PREVENTION[disease][severity]
        probabilities = {
            CLASS_NAMES[i]: round(float(probs[i]) * 100, 1)
            for i in range(len(CLASS_NAMES))
        }

        return jsonify({
            "disease":       disease,
            "severity":      severity,
            "confidence":    round(confidence, 1),
            "prevention":    prevention,
            "probabilities": probabilities,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running", "model": "EfficientNetB3", "classes": CLASS_NAMES})


if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")