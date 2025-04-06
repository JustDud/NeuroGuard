# 🧠 NeuroGuard – Mental State AI Assistant

## Overview
NeuroGuard is a futuristic AI-powered system designed to evaluate and improve your mental well-being in highly digitised environments. Built using machine learning and a modern web interface, it collects lifestyle signals and predicts your mental state on a scale from 0 to 100. The backend is powered by Flask and integrates ML predictions and optional AI suggestions using Google Gemini.

## Features
- **Mental State Prediction:** Uses a trained ML model (RandomForestRegressor) to estimate mental state from input parameters.
- **Web Interface:** Built with HTML, CSS, and JavaScript for clean user interaction.
- **Flask Backend:** Processes form input and interacts with the machine learning model.
- **MySQL Integration:** Stores historical data for analysis and tracking.
- **Gemini API Integration (Optional):** Offers suggestions based on mental state and user context.
- **Retraining Support:** CLI-based retraining using realistic sample data generated automatically.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YourUsername/NeuroGuard.git
```

### 2. Navigate to the Project Directory
```bash
cd NeuroGuard
```

### 3. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### 1. Start the Flask Web Server
```bash
python app.py
```
Then open your browser and go to: `http://localhost:5000`

### 2. Optional: Retrain the Model
```bash
python main.py
# Type 'train' when prompted
```

### 3. Gemini API
Set your Gemini API key in a `.env` file:
```plaintext
GEMINI_API_KEY=your-api-key
```

## Technologies Used
- **Languages:** Python, HTML, CSS, JavaScript
- **Frameworks/Libraries:** Flask, scikit-learn, pandas, joblib, MySQL, dotenv
- **Machine Learning:** RandomForestRegressor
- **AI Integration:** Google Gemini API (optional)

## Contributing
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Submit a pull request for review.


---

*Keywords: Mental Health AI, Web App, Machine Learning, NeuroGuard, Flask, Gemini, scikit-learn*
