import os
import cv2
import threading
from threading import Thread
from queue import Queue
from tqdm import tqdm
import glob
import subprocess

class VideoUtils:
    @staticmethod
    def extract_frames(video_path, resize_shape=(800, 800), num_workers=4):
        cap = cv2.VideoCapture(video_path)
        frames = []
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        pbar = tqdm(total=total_frames, desc=f'Extracting Frames from {os.path.basename(video_path)}', unit='frame')
        frame_queue = Queue(maxsize=100)
        result_dict = {}
        result_lock = threading.Lock()
        def read_frames():
            idx = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frame_queue.put((idx, frame))
                idx += 1
                pbar.update(1)
            cap.release()
            for _ in range(num_workers):
                frame_queue.put(None)
        def process_frames():
            while True:
                item = frame_queue.get()
                if item is None:
                    break
                idx, frame = item
                if resize_shape:
                    frame = cv2.resize(frame, (resize_shape[1], resize_shape[0]))
                with result_lock:
                    result_dict[idx] = frame
                frame_queue.task_done()
        reader_thread = Thread(target=read_frames)
        reader_thread.start()
        worker_threads = []
        for _ in range(num_workers):
            t = Thread(target=process_frames)
            t.start()
            worker_threads.append(t)
        frame_queue.join()
        for t in worker_threads:
            t.join()
        pbar.close()
        frames = [result_dict[i] for i in sorted(result_dict.keys())]
        return frames

    @staticmethod
    def standardize_frame_rate(original_video_path, generated_videos_folder):
        def check_ffmpeg_installed():
            try:
                subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False
        if not check_ffmpeg_installed():
            print("ffmpeg is not installed or not found in PATH. Please install ffmpeg to standardize frame rates.")
            return
        cap = cv2.VideoCapture(original_video_path)
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        video_files = glob.glob(os.path.join(generated_videos_folder, '*.mp4'))
        for video_file in video_files:
            cap_gen = cv2.VideoCapture(video_file)
            gen_fps = cap_gen.get(cv2.CAP_PROP_FPS)
            cap_gen.release()
            if gen_fps != original_fps:
                temp_output = video_file.replace('.mp4', '_temp.mp4')
                command = [
                    'ffmpeg', '-y', '-i', video_file, '-r', str(original_fps), temp_output
                ]
                try:
                    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if os.path.exists(temp_output):
                        os.replace(temp_output, video_file)
                except subprocess.CalledProcessError as e:
                    print(f"Error processing {video_file}: {e.stderr.decode()}")
                    if os.path.exists(temp_output):
                        os.remove(temp_output)
                    continue
