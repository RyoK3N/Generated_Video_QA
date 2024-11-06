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
```
---

## Prerequisites

- **Python 3.6** or higher
- **AWS account** with access to AWS Rekognition
- **FFmpeg** installed and added to your system's PATH
- Python packages listed in `requirements.txt`

---

## Installation
### Clone the Repository

```bash
git clone https://github.com/your_username/video_quality_evaluator.git
cd video_quality_evaluator
```

### Install Required Python Packages
It’s recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
pip install -r requirements.txt
```
### Install FFmpeg
Download FFmpeg from ffmpeg.org.
Install it according to your operating system.
#### OR
```bash
python -m pip install ffmpeg
```

Add FFmpeg to your system's PATH environment variable.

### Set Up AWS Credentials
Create a .env file in the root directory with your AWS credentials:
```makefile
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_DEFAULT_REGION=your_aws_region
```
Replace your_aws_access_key_id, your_aws_secret_access_key, and your_aws_region with your actual AWS credentials and preferred region.

### Configuration
Edit the config/config.yaml file if needed:

```yaml
Copy codeoriginal_video_path: 'data/original/TEST_original.mp4'
generated_videos_folder: 'data/generated/'
resize_shape: [800, 800]
num_workers: 4
```
    original_video_path: Path to your ground truth video.
    generated_videos_folder: Directory containing the generated videos to evaluate.
    resize_shape: Frame resize dimensions.
    num_workers: Number of worker threads for frame extraction.
---

## Running the Evaluation

### Prepare the Data
Place your ground truth video in the data/original/ directory.
Place the generated videos you want to evaluate in the data/generated/ directory.

### Run the Main Script
```bash
Copy code
python main.py
```
Note: If FFmpeg is not installed or found in your PATH, you will see a warning:

```vbnet
Copy code
ffmpeg is not installed or not found in PATH. Please install ffmpeg to standardize frame rates.
Frame rate standardization will be skipped if FFmpeg is unavailable.
```

### Check the Logs
Detailed logs with frame-wise metrics and average metrics for each video are saved in logs/app.log.

### Visualizing the Results
Run the Visualization Script
```bash
Copy code
python visualize.py
```
---

## View the Visualizations
Plots are saved in the visualizations/ directory. For each video, you will find:

Frame-wise metrics plots (MSE, PSNR, SSIM, and Landmark Difference, if available).
Bar charts showing average metrics.
Example files:

```plaintext
Copy code
visualizations/
├── Test_video-retalking.mp4_mse.png
├── Test_video-retalking.mp4_psnr.png
├── Test_video-retalking.mp4_ssim.png
├── Test_video-retalking.mp4_landmark_diff.png
├── Test_video-retalking.mp4_average_metrics.png
└── ... (other videos)
```
### Project Structure Overview
    
    config/config.yaml: Configuration file with paths and settings.
    data/: Contains the original and generated videos.
    logs/app.log: Log file with detailed metrics.
    src/video_utils.py: Utilities for video processing.
    src/evaluation.py: Functions for calculating evaluation metrics.
    main.py: Main script to run the evaluation.
    visualize.py: Script to generate visualizations from logs.
    requirements.txt: List of required Python packages.
    README.md: Documentation and instructions.

### Notes

    AWS Rekognition Costs: Using AWS Rekognition may incur costs. Be aware of pricing.
    RemBG Package: The rembg package is used for background removal. Ensure it is properly installed.
    Logging Level: The script uses the logging module. Adjust the logging level in main.py if needed.
    System Compatibility: The scripts are compatible with Unix-like systems and Windows. Ensure path separators are correct for your OS.
    Error Handling: Basic error handling is included. For production use, consider more robust checks and exception handling.

### Contact Information
For any issues or questions, please open an issue on the repository or contact the maintainer at reiyo1113@gmail.com.

---
