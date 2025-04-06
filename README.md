# 🧠 NeuroGuard – Mental State AI Assistant

> *"In 2080, your mind is the battlefield. NeuroGuard is your last line of defence."*

---

## 👥 Team Size: 3  
- Dmytro Dudarenko
- Khusainov Kamronbek
- Thomas Palmer


## 💡 Project Name: NeuroGuard

---

### ⚠️ Problem in the Year 2080

Welcome to 2080. Cities pulse with code. Brain implants stream ads into your dreams. You're connected, enhanced, optimised—until you're not.

In this hyper-digital world, attention isn’t just valuable—it’s under siege. Constant sensory input, AI-driven life assistance, immersive neural feeds—over time, it all builds up. The human brain, once adapted for silence, now drowns in data. The result?  
**Mental fragmentation. Cognitive crashes. Synthetic psychosis.**

While cybernetics evolve, mental health decays. We don’t need more stimulation—we need a **shield**.

---

### 🛡️ Our Solution: NeuroGuard

**NeuroGuard** is an AI-powered mental state monitoring system designed to defend users from digital overload and emotional burnout in ultra-connected environments.

Built with machine learning and a sleek web interface, NeuroGuard collects key lifestyle signals and outputs a **mental state score** (0–100). Based on that score, it can activate **Gemini AI**-driven interventions and suggest lifestyle tweaks to restore cognitive balance.

---

### 💻 Code Summary

#### 🔧 Core Features:
| Feature | Description |
|--------|-------------|
| 🧠 **Mental State Estimator** | Trained **RandomForestRegressor** Machine Learning Model predicts user's mental state based on input parameters |
| 🧬 **AI Suggestions (Gemini API)** | Context-aware tips & mental health prompts based on predicted state |
| 💻 **Web Interface** | Simple and elegant frontend in HTML/CSS/JS |
| 💾 **MySQL Integration** | Stores user history for long-term analysis and model refinement |
| 🧠 **Data Privacy** | Designed to run locally; Gemini integration is optional and transparent |

#### ⚙️ Tech Stack:
- **Languages**: Python, HTML, CSS, JavaScript  
- **Frameworks & Tools**: Flask, scikit-learn, pandas, MySQL, dotenv  
- **AI APIs**: Google Gemini (Optional)  
- **ML Model**: RandomForestRegressor  
- **Data Storage**: Local or MySQL-based  

#### 🚀 Usage:
1. Visit: `http://localhost:4000`  
2. Submit lifestyle info → Receive mental state score  
3. Trigger Gemini-powered suggestions  
4. Retrain the model using CLI: `python main.py`

---

### 🎯 Why It Matters

In 2080, your neural implants can update in seconds, but your brain still needs rest. *NeuroGuard* is designed to **observe, predict, and protect** — offering digital wellness in a world gone full chrome.

Whether you’re a netrunner, startup hustler, or just trying to survive the feed—NeuroGuard keeps your mind one step ahead of the crash.

---

> *"They enhanced our bodies. We built NeuroGuard to protect what’s left of the mind."*
