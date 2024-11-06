\documentclass{article}
\usepackage{hyperref}
\usepackage{listings}
\usepackage{amsmath}
\usepackage{enumitem}

\title{Video Quality Evaluator}
\date{}

\begin{document}

\maketitle

\section*{Overview}
This project evaluates the quality of AI-generated videos by comparing them with a ground truth video. It computes various metrics such as Mean Squared Error (MSE), Peak Signal-to-Noise Ratio (PSNR), Structural Similarity Index (SSIM), and face landmark differences using AWS Rekognition. The results are logged and can be visualized using the provided \texttt{visualize.py} script.

\tableofcontents

\section*{Directory Structure}
\begin{verbatim}
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
\end{verbatim}

\section*{Prerequisites}
\begin{itemize}
    \item Python 3.6 or higher
    \item AWS account with access to AWS Rekognition
    \item FFmpeg installed and added to your system's PATH
    \item Python packages listed in \texttt{requirements.txt}
\end{itemize}

\section*{Installation}

\subsection*{Clone the Repository}
\begin{verbatim}
git clone https://github.com/your_username/video_quality_evaluator.git
cd video_quality_evaluator
\end{verbatim}

\subsection*{Install Required Python Packages}
It is recommended to use a virtual environment:
\begin{verbatim}
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
\end{verbatim}

\subsection*{Install FFmpeg}
\begin{enumerate}
    \item Download FFmpeg from \url{https://ffmpeg.org}.
    \item Install it according to your operating system.
    \item Add FFmpeg to your system's PATH environment variable.
\end{enumerate}

\subsection*{Set Up AWS Credentials}
Create a \texttt{.env} file in the root directory with your AWS credentials:
\begin{verbatim}
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_DEFAULT_REGION=your_aws_region
\end{verbatim}
Replace \texttt{your\_aws\_access\_key\_id}, \texttt{your\_aws\_secret\_access\_key}, and \texttt{your\_aws\_region} with your actual AWS credentials and preferred region.

\section*{Configuration}
Edit the \texttt{config/config.yaml} file if needed:
\begin{verbatim}
original_video_path: 'data/original/TEST_original.mp4'
generated_videos_folder: 'data/generated/'
resize_shape: [800, 800]
num_workers: 4
\end{verbatim}

\begin{itemize}
    \item \texttt{original\_video\_path}: Path to your ground truth video.
    \item \texttt{generated\_videos\_folder}: Directory containing the generated videos to evaluate.
    \item \texttt{resize\_shape}: Frame resize dimensions.
    \item \texttt{num\_workers}: Number of worker threads for frame extraction.
\end{itemize}

\section*{Running the Evaluation}
\subsection*{Prepare the Data}
\begin{itemize}
    \item Place your ground truth video in the \texttt{data/original/} directory.
    \item Place the generated videos you want to evaluate in the \texttt{data/generated/} directory.
\end{itemize}

\subsection*{Run the Main Script}
\begin{verbatim}
python main.py
\end{verbatim}
\textbf{Note}: If FFmpeg is not installed or not found in your PATH, you will see a warning:
\begin{verbatim}
ffmpeg is not installed or not found in PATH. Please install ffmpeg to standardize frame rates.
\end{verbatim}
This means frame rate standardization will be skipped.

\subsection*{Check the Logs}
The script will generate detailed logs in \texttt{logs/app.log}, containing frame-wise metrics and average metrics for each video.

\section*{Visualizing the Results}
\subsection*{Run the Visualization Script}
\begin{verbatim}
python visualize.py
\end{verbatim}

\subsection*{View the Visualizations}
The script will generate plots and save them in the \texttt{visualizations/} directory. For each video, you will find:

\begin{itemize}
    \item Frame-wise metrics plots (MSE, PSNR, SSIM, and Landmark Difference if available).
    \item Bar charts showing average metrics.
\end{itemize}

\textbf{Example file names:}
\begin{verbatim}
visualizations/
├── Test_video-retalking.mp4_mse.png
├── Test_video-retalking.mp4_psnr.png
├── Test_video-retalking.mp4_ssim.png
├── Test_video-retalking.mp4_landmark_diff.png
├── Test_video-retalking.mp4_average_metrics.png
└── ... (other videos)
\end{verbatim}

\section*{Project Structure Overview}
\begin{itemize}
    \item \texttt{config/config.yaml}: Configuration file with paths and settings.
    \item \texttt{data/}: Contains the original and generated videos.
    \item \texttt{logs/app.log}: Log file with detailed metrics.
    \item \texttt{src/video\_utils.py}: Utilities for video processing.
    \item \texttt{src/evaluation.py}: Functions for calculating evaluation metrics.
    \item \texttt{main.py}: Main script to run the evaluation.
    \item \texttt{visualize.py}: Script to generate visualizations from logs.
    \item \texttt{requirements.txt}: List of required Python packages.
    \item \texttt{README.md}: Documentation and instructions.
\end{itemize}

\section*{Notes}
\begin{itemize}
    \item \textbf{AWS Rekognition Costs}: Using AWS Rekognition may incur costs. Ensure you are aware of the pricing.
    \item \textbf{RemBG Package}: The \texttt{rembg} package is used for background removal. Ensure it is properly installed.
    \item \textbf{Logging Level}: The script uses the logging module. Adjust the logging level in \texttt{main.py} if needed.
    \item \textbf{System Compatibility}: The scripts are compatible with Unix-like systems and Windows. Ensure path separators are correct for your OS.
    \item \textbf{Error Handling}: The scripts include basic error handling. For production use, consider adding more robust checks and exception handling.
\end{itemize}

\section*{Contact Information}
For any issues or questions, please open an issue on the repository or contact the maintainer at \texttt{your\_email@example.com}.

\end{document}
