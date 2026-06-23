# Lip2Speech — ReVox

Offline Assistive AI for Spatio-Temporal Lip Reading and Speech Synthesis.

---

## 1 — Repository Details
* **GitHub Repository**: [AlekhyaGangopadhyay/Lip2Speech_ReVox](https://github.com/AlekhyaGangopadhyay/Lip2Speech_ReVox)
* **Hugging Face Space**: [iamalekhya/Lip2Speech](https://huggingface.co/spaces/iamalekhya/Lip2Speech)

---

## 2 — Project Structure

```
lip2speech/
├── app.py                          ← Flask backend + model inference
├── requirements.txt                ← Python dependencies (no dlib compile needed!)
├── lipreading_model.pth            ← ⚠ YOUR MODEL WEIGHTS (place in root)
├── templates/
│   └── index.html                  ← frontend web interface
├── static/
│   ├── logo.png                    ← web app logo
│   ├── system_architecture.png     ← slide graphic: methodology flowchart
│   └── performance_dashboard.png   ← slide graphic: ablation matrix benchmarks
├── scratch/
│   └── populate_presentation.py    ← script to compile PPTX presentation
├── Smart Verse template...pptx     ← original presentation PowerPoint template
├── Smart_Verse_Lip..._Pres.pptx    ← final populated PowerPoint slides
├── presentation_content.md         ← slide transcript & copy-pasteable draft
└── README.md                       ← this guide
```

---

## 3 — Architecture Overview

This project implements a lightweight visual-to-speech assistant:
* **Feature Extractor**: MobileNetV2 backbone (frozen features) extracting spatial representations from lip region crops.
* **Sequence Modeler**: 2-layer Bidirectional LSTM processing frame sequences temporally.
* **Inference Preprocessing**: Face and lip detection powered by OpenCV's Haar Cascade (100% offline, C++ compiler independent) instead of `dlib`. Mouth area mathematically targeted and scaled to $112 \times 112$ px.
* **Decoding**: Word-level argmax sequence classification using the 51-class `GRID_VOCAB`.
* **Grammar Correction**: Optional local HuggingFace `t5-base` LLM to refine spelling, word repetition, and syntax.
* **Speech Synthesis**: Offline text-to-speech engine using `pyttsx3` with online `gTTS` fallback.

---

## 4 — Setup and Run

### Virtual Environment Setup
```bash
# 1. Clone the repository
git clone https://github.com/AlekhyaGangopadhyay/Lip2Speech_ReVox.git
cd Lip2Speech_ReVox

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Running the Web Server
Make sure to copy your trained weights file `lipreading_model.pth` to the project root. Then run:
```bash
python app.py
```
Open **http://localhost:5000** in your browser.

---

## 5 — PowerPoint Slide Generation

To compile the **Smart Verse** PowerPoint presentation populated with the project details, flowchart diagrams, ablation matrices, and result tables:

```bash
python scratch/populate_presentation.py
```
This script reads the original presentation template, inserts your custom project text (including the compact 3-column Problem Statement, 3-column Existing Solutions, and Result metrics table), positions the visual diagrams from `/static`, and saves the deck to **`Smart_Verse_Lip2Speech_Presentation.pptx`**.

---

## 6 — Troubleshooting

| Problem | Fix |
|---|---|
| `Model weights not found` | Copy `lipreading_model.pth` to the project root |
| T5 download fails / slow | Check your internet connection; the model is ~890MB and downloads only on the first run with LLM active. |
| `(no speech detected)` | Video may have no visible face or lips / model needs more training |
| Audio plays silently | pyttsx3 may need a system TTS engine; on Linux install `espeak`: `sudo apt install espeak` |
| CUDA OOM | Force CPU execution: set environment variable `CUDA_VISIBLE_DEVICES=""` before running |
