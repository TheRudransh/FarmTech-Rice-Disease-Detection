# 🌾 FarmTech — Rice Leaf Disease Detection

An AI-powered web application that detects rice plant diseases from leaf images, classifies severity levels, and provides actionable prevention recommendations for farmers.

---

## 🎯 Project Overview

Rice is one of the most important staple crops in the world, particularly in South and Southeast Asia. Diseases in rice crops can cause significant yield losses if not detected and treated early. This project uses deep learning to help farmers identify diseases quickly and take appropriate action.

**FarmTech** combines a trained convolutional neural network with a web interface that allows users to upload a rice leaf photo and instantly receive:
- Disease identification
- Severity level (Low / Medium / High)
- Confidence score
- Step-by-step prevention and treatment recommendations

---

## 🚀 Demo

![FarmTech Demo](assets/demo.png)

> Upload a rice leaf image → Get instant disease diagnosis → Follow prevention steps

---

## 🦠 Supported Disease Classes

| Class | Type | Description |
|---|---|---|
| **Blast** | Fungal | Diamond-shaped grey lesions on leaves |
| **Healthy** | — | No disease detected |
| **Insect** | Pest | Mechanical damage from insects |
| **Leaf Folder** | Pest | Leaves rolled by Cnaphalocrocis medinalis larvae |
| **Scald** | Fungal | Brown scorch marks on leaf edges |
| **Stripes** | Viral | Yellow striping, transmitted by planthoppers |
| **Tungro** | Viral | Yellowing and stunting, transmitted by leafhoppers |

---

## 🧠 Model Architecture

- **Base Model:** EfficientNetB3 pretrained on ImageNet
- **Training Strategy:** Transfer learning with 2-phase training
  - Phase 1: Frozen backbone, custom head trained
  - Phase 2+: Progressive unfreezing and fine-tuning
- **Dataset:** RiceGuard 19k Cleaned (18,558 JPEG images)
- **Input Size:** 224 × 224 pixels
- **Classes:** 7
- **Test Accuracy:** 79.89%
- **Framework:** TensorFlow / Keras

### Training Results

| Phase | Best Val Accuracy |
|---|---|
| Phase 1 | 62.72% |
| Phase 2 | 76.22% |
| Phase 3 | 81.34% |
| Phase 4 | 84.08% |

### Classification Report (Test Set)

| Class | Precision | Recall | F1-Score |
|---|---|---|---|
| blast | 0.89 | 0.68 | 0.77 |
| healthy | 0.81 | 0.87 | 0.84 |
| insect | 0.87 | 0.88 | 0.87 |
| leaf_folder | 0.87 | 0.98 | **0.92** |
| scald | 0.26 | 0.77 | 0.39 |
| stripes | 0.85 | 0.67 | 0.75 |
| tungro | 0.74 | 0.82 | 0.78 |

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| AI Model | TensorFlow 2.16, Keras, EfficientNetB3 |
| Backend API | Python, Flask, Flask-CORS |
| Frontend | HTML5, CSS3, JavaScript (Vanilla) |
| Training Platform | Google Colab (T4 GPU) + Mac M4 (Metal GPU) |
| Dataset | RiceGuard 19k Cleaned (Kaggle) |

---

## 📁 Project Structure

```
FarmTech/
├── app.py                          ← Flask REST API
├── Rice_Disease_Detection_FINAL_colab.ipynb  ← Training notebook
├── build-a-professional-rice-leaf-disease/   ← Website
│   ├── index.html                  ← Home page
│   ├── detect.html                 ← Detection page
│   ├── styles.css                  ← Styling
│   ├── script.js                   ← JavaScript
│   └── assets/                     ← Images
├── phase1_log.csv                  ← Training logs
├── phase2_log.csv
├── phase3_log.csv
├── phase4_log.csv
└── .gitignore
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.11
- Mac (Apple Silicon) or Linux

### 1. Clone the repository
```bash
git clone https://github.com/rudranshgarg/FarmTech-Rice-Disease-Detection.git
cd FarmTech-Rice-Disease-Detection
```

### 2. Create virtual environment
```bash
python3.11 -m venv .venv311
source .venv311/bin/activate
```

### 3. Install dependencies
```bash
pip install tensorflow==2.16.1 tensorflow-metal==1.1.0
pip install flask flask-cors numpy pillow scikit-learn
```

### 4. Download the trained model
Download `phase4_best.keras` from Google Drive:
> [Download Model](YOUR_GOOGLE_DRIVE_LINK_HERE)

Place it in the root `FarmTech/` directory.

### 5. Run the Flask API
```bash
python app.py
```
API will start at `http://localhost:8080`

### 6. Run the website
Open a new terminal:
```bash
cd build-a-professional-rice-leaf-disease
python3 -m http.server 8000
```
Open browser and go to `http://localhost:8000`

---

## 🌐 API Reference

### POST /predict
Upload a rice leaf image and get disease prediction.

**Request:**
```
Content-Type: multipart/form-data
Body: image (file)
```

**Response:**
```json
{
  "disease": "blast",
  "severity": "High",
  "confidence": 85.9,
  "prevention": [
    "URGENT: Apply Propiconazole 25 EC @ 1 ml/L immediately",
    "Repeat spray after 7-10 days",
    "Remove and burn heavily infected crop debris"
  ],
  "probabilities": {
    "blast": 85.9,
    "healthy": 7.1,
    "tungro": 4.1,
    "stripes": 1.3,
    "scald": 1.0,
    "insect": 0.4,
    "leaf_folder": 0.2
  }
}
```

### GET /health
Check if API is running.

**Response:**
```json
{
  "status": "running",
  "model": "EfficientNetB3"
}
```

---

## 📊 Dataset

**RiceGuard 19k Cleaned** — [Kaggle Dataset](https://www.kaggle.com/datasets/chaitanyakamble69/rice-leaf-disease-riceguard-19k-cleaned)

| Split | Images |
|---|---|
| Train | 12,983 |
| Val | 2,776 |
| Test | 2,799 |
| **Total** | **18,558** |

---

## ⚠️ Limitations

- Model performs best on isolated leaf images with white/plain backgrounds
- `scald` class has lower accuracy due to limited training data (294 images)
- Real-world field photos with complex backgrounds may reduce accuracy
- Future improvement: collect diverse field photography for training data

---

## 🔮 Future Work

- [ ] Add weather-based disease risk prediction
- [ ] Collect real farm photos for training
- [ ] Build mobile app (React Native)
- [ ] Deploy to cloud (Render + Netlify)
- [ ] Add more disease classes
- [ ] Support regional languages for farmers

---

## 👨‍💻 Author

**Rudransh Garg**
B.Tech Student

---

## 📄 License

This project is for educational purposes.

---

## 🙏 Acknowledgements

- RiceGuard dataset by Chaitanya Kamble (Kaggle)
- EfficientNetB3 by Google Brain team
- TensorFlow and Keras teams
