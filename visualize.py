import re
import matplotlib.pyplot as plt
import numpy as np
import os

def parse_log(log_file):
    video_data = {}
    current_video = None
    with open(log_file, 'r') as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Remove 'INFO:root:' prefix if present
        if line.startswith('INFO:root:'):
            line = line[len('INFO:root:'):].strip()
        # Skip empty lines
        if not line:
            i += 1
            continue
        video_match = re.match(r'Results for (.+):', line)
        if video_match:
            current_video = video_match.group(1)
            if current_video not in video_data:
                video_data[current_video] = {
                    'frame_nums': [],
                    'mse_values': [],
                    'psnr_values': [],
                    'ssim_values': [],
                    'landmark_differences': [],
                    'average_mse': None,
                    'average_psnr': None,
                    'average_ssim': None,
                    'average_landmark_difference': None
                }
            i += 1
            continue
        frame_match = re.match(r'Frame (\d+)/\d+ of (.+):', line)
        if frame_match:
            frame_num = int(frame_match.group(1))
            video_name = frame_match.group(2)
            if video_name != current_video:
                current_video = video_name
                if current_video not in video_data:
                    video_data[current_video] = {
                        'frame_nums': [],
                        'mse_values': [],
                        'psnr_values': [],
                        'ssim_values': [],
                        'landmark_differences': [],
                        'average_mse': None,
                        'average_psnr': None,
                        'average_ssim': None,
                        'average_landmark_difference': None
                    }
            i += 1
            # Read the next lines for MSE, PSNR, SSIM, and Landmark Difference
            try:
                mse_line = lines[i].strip()
                if mse_line.startswith('INFO:root:'):
                    mse_line = mse_line[len('INFO:root:'):].strip()
                mse_match = re.match(r'MSE: (.+)', mse_line)
                mse_value = float(mse_match.group(1)) if mse_match else None

                i += 1
                psnr_line = lines[i].strip()
                if psnr_line.startswith('INFO:root:'):
                    psnr_line = psnr_line[len('INFO:root:'):].strip()
                psnr_match = re.match(r'PSNR: (.+)', psnr_line)
                psnr_value = float(psnr_match.group(1)) if psnr_match else None

                i += 1
                ssim_line = lines[i].strip()
                if ssim_line.startswith('INFO:root:'):
                    ssim_line = ssim_line[len('INFO:root:'):].strip()
                ssim_match = re.match(r'SSIM: (.+)', ssim_line)
                ssim_value = float(ssim_match.group(1)) if ssim_match else None

                i += 1
                landmark_line = lines[i].strip()
                if landmark_line.startswith('INFO:root:'):
                    landmark_line = landmark_line[len('INFO:root:'):].strip()
                landmark_match = re.match(r'Landmark Difference: (.+)', landmark_line)
                if landmark_match:
                    landmark_value = float(landmark_match.group(1))
                else:
                    no_landmark_match = re.match(r'No landmarks detected in one of the frames\.', landmark_line)
                    landmark_value = None if no_landmark_match else None

                video_data[current_video]['frame_nums'].append(frame_num)
                video_data[current_video]['mse_values'].append(mse_value)
                video_data[current_video]['psnr_values'].append(psnr_value)
                video_data[current_video]['ssim_values'].append(ssim_value)
                video_data[current_video]['landmark_differences'].append(landmark_value)
                i += 1
            except IndexError:
                # Reached the end of the file unexpectedly
                break
            continue
        avg_mse_match = re.match(r'Average MSE: (.+)', line)
        if avg_mse_match and current_video:
            video_data[current_video]['average_mse'] = float(avg_mse_match.group(1))
            i += 1
            continue
        avg_psnr_match = re.match(r'Average PSNR: (.+)', line)
        if avg_psnr_match and current_video:
            video_data[current_video]['average_psnr'] = float(avg_psnr_match.group(1))
            i += 1
            continue
        avg_ssim_match = re.match(r'Average SSIM: (.+)', line)
        if avg_ssim_match and current_video:
            video_data[current_video]['average_ssim'] = float(avg_ssim_match.group(1))
            i += 1
            continue
        avg_landmark_match = re.match(r'Average Landmark Difference: (.+)', line)
        if avg_landmark_match and current_video:
            video_data[current_video]['average_landmark_difference'] = float(avg_landmark_match.group(1))
            i += 1
            continue
        no_landmarks_match = re.match(r'No landmarks detected in some frames\.', line)
        if no_landmarks_match and current_video:
            video_data[current_video]['average_landmark_difference'] = None
            i += 1
            continue
        # If line doesn't match any expected pattern, skip it
        i += 1
    return video_data

def plot_metrics(video_data, output_dir='visualizations'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for video_name, data in video_data.items():
        frames = data['frame_nums']
        mse_values = data['mse_values']
        psnr_values = data['psnr_values']
        ssim_values = data['ssim_values']
        landmark_differences = data['landmark_differences']
        plt.figure()
        plt.plot(frames, mse_values)
        plt.xlabel('Frame')
        plt.ylabel('MSE')
        plt.title(f'MSE over Frames for {video_name}')
        plt.savefig(os.path.join(output_dir, f'{video_name}_mse.png'))
        plt.close()
        plt.figure()
        plt.plot(frames, psnr_values)
        plt.xlabel('Frame')
        plt.ylabel('PSNR')
        plt.title(f'PSNR over Frames for {video_name}')
        plt.savefig(os.path.join(output_dir, f'{video_name}_psnr.png'))
        plt.close()
        plt.figure()
        plt.plot(frames, ssim_values)
        plt.xlabel('Frame')
        plt.ylabel('SSIM')
        plt.title(f'SSIM over Frames for {video_name}')
        plt.savefig(os.path.join(output_dir, f'{video_name}_ssim.png'))
        plt.close()
        if any(ld is not None for ld in landmark_differences):
            ld_values = [ld if ld is not None else np.nan for ld in landmark_differences]
            plt.figure()
            plt.plot(frames, ld_values)
            plt.xlabel('Frame')
            plt.ylabel('Landmark Difference')
            plt.title(f'Landmark Difference over Frames for {video_name}')
            plt.savefig(os.path.join(output_dir, f'{video_name}_landmark_diff.png'))
            plt.close()
        metrics = ['Average MSE', 'Average PSNR', 'Average SSIM']
        values = [data['average_mse'], data['average_psnr'], data['average_ssim']]
        plt.figure()
        plt.bar(metrics, values)
        plt.title(f'Average Metrics for {video_name}')
        plt.savefig(os.path.join(output_dir, f'{video_name}_average_metrics.png'))
        plt.close()

if __name__ == '__main__':
    log_file = 'logs/app.log'
    video_data = parse_log(log_file)
    plot_metrics(video_data)
