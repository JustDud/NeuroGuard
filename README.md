---

## Tech Stack Overview

| Layer                | Technologies Used                                    | Purpose |
|----------------------|------------------------------------------------------|---------|
| **Frontend**         | HTML, CSS, JavaScript                                | Collect user input through a responsive web form |
| **Backend**          | Flask (Python)                                       | Process user input, call ML model, and return response |
| **Machine Learning** | scikit-learn (RandomForestRegressor)                | Predict mental state (0–100) from lifestyle input |
| **Database**         | MySQL                                               | Store historical user data and mental state records |
| **AI Integration**   | Google Gemini API (optional)                        | Generate context-aware suggestions |
| **Data Handling**    | pandas, joblib, json                                | Load and save data/models, preprocess features |
| **Automation**       | data_generator.py, ml.py                            | Generate realistic training data and train ML model |

---

## Project Structure

```
neuroguard/
├── app.py                    # Flask web server
├── templates/
│   └── index.html            # User-facing web form
├── static/
│   ├── style.css             # Web styling
│   └── script.js             # Frontend logic
├── ml.py                     # Machine learning training/prediction
├── data_generator.py         # Sample data generation and scoring
├── trained_model.pkl         # Saved model file
├── generated_sample_data.json# Sample data with mental_state
├── .env                      # Environment variables (API keys)
├── README.md                 # You're reading it :)
└── requirements.txt          # Project dependencies
```

---

## Getting Started

### 1. Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Run the application:

```bash
python app.py
```

Then visit `http://localhost:5000` in your browser.

---

## Retraining the Model

If you wish to retrain the model from sample data:

```bash
python main.py
# Type 'train' when prompted
```

---

## Model Info

- Model: `RandomForestRegressor`
- Target: Predict `mental_state` on a scale of 0–100
- Accuracy (±10 points): ~70–80%
- Average error (MAE): ~12–18
- Training dataset: `generated_sample_data.json`

---
