import os
import glob
import logging
import yaml
from src.video_utils import VideoUtils
from src.evaluation import mask_person, MSE, calculate_psnr, calculate_ssim, compare_face_landmarks
import numpy as np
from tqdm import tqdm

def load_config(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def process_videos(video_paths, reference_paths, resize_shape, num_workers, log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO)
    for video_path, reference_path in zip(video_paths, reference_paths):
        frames = VideoUtils.extract_frames(video_path, resize_shape=resize_shape, num_workers=num_workers)
        ref_frames = VideoUtils.extract_frames(reference_path, resize_shape=resize_shape, num_workers=num_workers)
        num_frames = min(len(frames), len(ref_frames))
        mse_values = []
        psnr_values = []
        ssim_values = []
        landmark_differences = []
        for i in tqdm(range(num_frames), desc=f'Processing frames for {os.path.basename(video_path)}'):
            frame = mask_person(frames[i])
            ref_frame = mask_person(ref_frames[i])
            mse = MSE(frame, ref_frame)
            psnr = calculate_psnr(frame, ref_frame)
            ssim_score = calculate_ssim(frame, ref_frame)
            landmark_diff = compare_face_landmarks(frame, ref_frame)
            mse_values.append(mse)
            psnr_values.append(psnr)
            ssim_values.append(ssim_score)
            if landmark_diff is not None:
                landmark_differences.append(landmark_diff)
            logging.info(f"Frame {i+1}/{num_frames} of {os.path.basename(video_path)}:")
            logging.info(f"MSE: {mse}")
            logging.info(f"PSNR: {psnr}")
            logging.info(f"SSIM: {ssim_score}")
            if landmark_diff is not None:
                logging.info(f"Landmark Difference: {landmark_diff}")
            else:
                logging.info("No landmarks detected in one of the frames.")
        logging.info(f"Results for {os.path.basename(video_path)}:")
        logging.info(f"Average MSE: {np.mean(mse_values)}")
        logging.info(f"Average PSNR: {np.mean(psnr_values)}")
        logging.info(f"Average SSIM: {np.mean(ssim_values)}")
        if landmark_differences:
            logging.info(f"Average Landmark Difference: {np.mean(landmark_differences)}")
        else:
            logging.info("No landmarks detected in some frames.")

if __name__ == '__main__':
    config = load_config('config/config.yaml')
    original_video_path = config['original_video_path']
    generated_videos_folder = config['generated_videos_folder']
    resize_shape = tuple(config.get('resize_shape', [800, 800]))
    num_workers = config.get('num_workers', 4)
    log_file = 'logs/app.log'

    VideoUtils.standardize_frame_rate(original_video_path, generated_videos_folder)
    video_files = glob.glob(os.path.join(generated_videos_folder, '*.mp4'))
    reference_paths = [original_video_path] * len(video_files)
    process_videos(video_files, reference_paths, resize_shape, num_workers, log_file)
