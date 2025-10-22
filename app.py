# app.py — Beautiful UI + Logo
from flask import Flask, request, render_template_string
import joblib

app = Flask(__name__)
model = joblib.load("model.pkl")

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📰 TruthGuard — Fake News Detector</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap">
    <style>
        :root {
            --bg: #ffffff;
            --text: #1f2937;
            --primary: #4f46e5;
            --real: #10b981;
            --fake: #ef4444;
            --card: #f9fafb;
            --border: #e5e7eb;
        }
        @media (prefers-color-scheme: dark) {
            :root {
                --bg: #111827;
                --text: #f9fafb;
                --card: #1f2937;
                --border: #374151;
            }
        }
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            line-height: 1.6;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .logo {
            margin-bottom: 16px;
            color: var(--primary);
        }
        .logo svg {
            width: 64px;
            height: 64px;
        }
        h1 {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, var(--primary), #818cf8);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        .subtitle {
            color: #6b7280;
            font-size: 1.1rem;
        }
        .card {
            background: var(--card);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid var(--border);
            margin-bottom: 24px;
        }
        textarea {
            width: 100%;
            min-height: 120px;
            padding: 16px;
            border: 1px solid var(--border);
            border-radius: 12px;
            font-size: 16px;
            font-family: inherit;
            background: var(--bg);
            color: var(--text);
            resize: vertical;
        }
        textarea:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
        }
        button {
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 14px 28px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            width: 100%;
            max-width: 200px;
            margin-top: 16px;
        }
        button:hover {
            background: #4338ca;
            transform: translateY(-2px);
        }
        .result-box {
            text-align: center;
            padding: 24px;
            border-radius: 16px;
            margin-top: 20px;
            animation: fadeIn 0.5s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .result-label {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 12px;
        }
        .real { color: var(--real); }
        .fake { color: var(--fake); }
        .confidence-bar {
            height: 12px;
            background: #e5e7eb;
            border-radius: 6px;
            overflow: hidden;
            margin: 16px auto;
            max-width: 400px;
        }
        .confidence-fill {
            height: 100%;
            border-radius: 6px;
        }
        .real .confidence-fill { background: var(--real); }
        .fake .confidence-fill { background: var(--fake); }
        .confidence-text {
            font-size: 0.95rem;
            color: #6b7280;
            margin-top: 8px;
        }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            color: var(--primary);
            text-decoration: none;
            font-weight: 500;
        }
        .back-link:hover {
            text-decoration: underline;
        }
        footer {
            text-align: center;
            margin-top: 3rem;
            color: #9ca3af;
            font-size: 0.9rem;
        }
        @media (max-width: 600px) {
            .logo svg { width: 50px; height: 50px; }
            h1 { font-size: 1.8rem; }
            .card { padding: 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">
                <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M24 4L8 12V24C8 33.38 13.38 40 24 44C34.62 40 40 33.38 40 24V12L24 4Z" 
                          stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                    <path d="M18 24L22 28L30 20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
            </div>
            <h1>TruthGuard</h1>
            <p class="subtitle">AI-powered fake news detection for headlines</p>
        </header>

        {% if result %}
            <div class="card">
                <div class="result-box {{ 'real' if result == 'Real' else 'fake' }}">
                    <div class="result-label">{{ result }}</div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: {{ confidence }}%;"></div>
                    </div>
                    <div class="confidence-text">Confidence: {{ confidence }}%</div>
                    <div style="margin-top: 16px; font-size: 1rem; color: #6b7280;">
                        “{{ headline[:80] }}{{ '...' if headline|length > 80 else '' }}”
                    </div>
                    <a href="/" class="back-link">← Analyze another headline</a>
                </div>
            </div>
        {% else %}
            <div class="card">
                <form method="POST" action="/predict">
                    <textarea name="headline" placeholder="Paste a news headline here..."></textarea>
                    <button type="submit">Analyze</button>
                </form>
                {% if error %}
                    <p style="color: var(--fake); margin-top: 12px;">{{ error }}</p>
                {% endif %}
            </div>
        {% endif %}

        <footer>
            <p>AI generated content may not be acacurate • ISOT-trained model</p>
        </footer>
    </div>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/predict", methods=["POST"])
def predict():
    headline = request.form.get("headline", "").strip()
    if not headline:
        return render_template_string(HTML_TEMPLATE, error="⚠️ Please enter a headline.")

    pred = model.predict([headline])[0]
    prob = model.predict_proba([headline])[0]
    confidence = round(max(prob) * 100, 2)
    result = "Real" if pred == 0 else "Fake"

    return render_template_string(
        HTML_TEMPLATE,
        result=result,
        confidence=confidence,
        headline=headline
    )

if __name__ == "__main__":
    app.run(debug=True)