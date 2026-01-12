# 🏥 HealthCareAI
**Empowering Healthcare with Vision, Voice, and Explainable AI (XAI)**

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Gradio](https://img.shields.io/badge/UI-Gradio-orange.svg)
![Llama4](https://img.shields.io/badge/Model-Llama--4--Scout-green.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

## 🌟 Overview
AI Doctor 2.0 is a professional-grade medical diagnostic assistant designed for **Neurathon 2026**. It bridges the gap between complex AI and clinical trust by combining **Vision (Image Analysis)**, **Voice (Patient Intake)**, and **Reasoning Traces (Explainability)**. 

Unlike standard "black-box" models, this system provides a visual grounding of its findings and a human-like logical deduction path to assist healthcare professionals in remote or underserved areas.

---

## 🚀 Key Features

### 1. Multimodal Patient Intake
* **Voice-to-Text (STT):** Uses **OpenAI Whisper (via Groq)** for high-accuracy transcription of patient symptoms.
* **Vision Analysis:** Powered by **Llama-4-Scout**, capable of identifying anomalies in X-rays, skin lesions, and neurological scans.

### 2. Explainable AI (XAI) & Visual Grounding
* **Reasoning Trace:** Instead of a single diagnosis, the AI generates a clinical logic path (Observation -> History -> Deduction).
* **Anomaly Highlighting:** Dynamically draws a semi-transparent bounding box over detected medical anomalies using **Pillow (PIL)**.

### 3. Professional Medical Dashboard
* **Doctor-in-the-Loop UI:** A clean, sidebar-driven dashboard built with Gradio 5.
* **Human-Like Interaction:** Empathetic, professional responses converted to high-fidelity audio via **ElevenLabs**.

---

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Inference Engine:** Groq (Llama-4-Scout-17B & Whisper-Large-v3)
* **Voice Synthesis:** ElevenLabs (Turbo v2.5)
* **Interface:** Gradio 5 (Custom CSS/Theme)
* **Image Processing:** Pillow (PIL)

---

## 📂 Project Structure
```text
.
├── brain_of_the_doctor.py    # Vision analysis & reasoning logic
├── voice_of_the_patient.py   # Transcription (STT) handling
├── voice_of_the_doctor.py    # Speech synthesis (TTS) handling
├── gradio_app.py             # Main Medical Dashboard UI
├── .env                      # API Keys (Excluded from Git)
├── .env.example              # Template for environment variables
└── requirements.txt          # Project dependencies

