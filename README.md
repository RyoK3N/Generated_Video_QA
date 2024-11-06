# Video Quality Evaluator

This project is designed to evaluate the quality of AI-generated videos by comparing them with a ground truth video. It computes various metrics such as:
- **MSE** (Mean Squared Error)
- **PSNR** (Peak Signal-to-Noise Ratio)
- **SSIM** (Structural Similarity Index)
- **Face Landmark Differences** (using AWS Rekognition)

The results are logged and can be visualized with the provided `visualize.py` script.

---

## Table of Contents
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Evaluation](#running-the-evaluation)
- [Visualizing the Results](#visualizing-the-results)
- [Project Structure Overview](#project-structure-overview)
- [Notes](#notes)
- [Contact Information](#contact-information)

---

## Directory Structure

```plaintext
video_quality_evaluator/
├── config/
│   └── config.yaml
├── data/
│   ├── generated/
│   │   └── ... (your generated videos)
│   └── original/
│       └── TEST_original.mp4
├── logs/
│   └── app.log
├── src/
│   ├── evaluation.py
│   └── video_utils.py
├── visualizations/
│   └── ... (generated plots)
├── main.py
├── visualize.py
├── requirements.txt
└── README.md
