# 🛡️ TruthGuard — Fake News Detection

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Dataset](https://img.shields.io/badge/Dataset-ISOT-orange)](https://www.kaggle.com/datasets/emineyetm/fake-news-dataset)
[![Flask](https://img.shields.io/badge/Flask-3.0+-black?logo=flask)](https://flask.palletsprojects.com)

A lightweight, offline-first web application that detects **fake vs. real news headlines** using machine learning trained on the **ISOT Fake News Dataset** (68,000+ samples).

> 🔍 **No internet required after setup** • **No external APIs** • **Runs 100% on your machine**

![TruthGuard UI Preview](https://github.com/Malay-Shrivas/Truth-Guard/raw/main/screenshot.png)  

---

## ✨ Features

- **High Accuracy**: ~94% accuracy on real-world fake news data
- **Offline-First**: No cloud dependencies or API keys
- **Beautiful UI**: Responsive design with dark/light mode support
- **Confidence Scoring**: Visual confidence meter for every prediction
- **Privacy-Respecting**: All processing happens locally on your device
- **Mac-Optimized**: Built and tested on macOS (Intel & Apple Silicon)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- `pip` package manager

### Installation
```bash
# Clone the repository
git clone https://github.com/Malay-Shrivas/Truth-Guard.git
cd Truth-Guard

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
