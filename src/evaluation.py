import os
import cv2
import numpy as np
from rembg import remove
from skimage.metrics import structural_similarity as ssim
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')

def mask_person(frame):
    return remove(frame)

def MSE(frame, ref_frame):
    squared_diff = (frame - ref_frame) ** 2
    summed = np.sum(squared_diff)
    num_pix = frame.shape[0] * frame.shape[1]
    err = summed / num_pix
    return err

def calculate_psnr(frame, ref_frame, max_value=255):
    mse = np.mean((frame.astype(np.float32) - ref_frame.astype(np.float32)) ** 2)
    if mse == 0:
        return 100
    return 20 * np.log10(max_value / (np.sqrt(mse)))

def calculate_ssim(frame, ref_frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_ref_frame = cv2.cvtColor(ref_frame, cv2.COLOR_BGR2GRAY)
    score, _ = ssim(gray_frame, gray_ref_frame, full=True)
    return score

def compare_face_landmarks(frame, ref_frame, region_name=AWS_DEFAULT_REGION):
    rekognition = boto3.client(
        'rekognition',
        region_name=region_name,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    _, buffer1 = cv2.imencode('.jpg', frame)
    image_bytes1 = buffer1.tobytes()
    _, buffer2 = cv2.imencode('.jpg', ref_frame)
    image_bytes2 = buffer2.tobytes()
    response1 = rekognition.detect_faces(
        Image={'Bytes': image_bytes1},
        Attributes=['ALL']
    )
    response2 = rekognition.detect_faces(
        Image={'Bytes': image_bytes2},
        Attributes=['ALL']
    )
    if not response1['FaceDetails'] or not response2['FaceDetails']:
        return None
    landmarks1 = response1['FaceDetails'][0]['Landmarks']
    landmarks2 = response2['FaceDetails'][0]['Landmarks']
    coords1 = np.array([[lm['X'], lm['Y']] for lm in landmarks1])
    coords2 = np.array([[lm['X'], lm['Y']] for lm in landmarks2])
    if coords1.shape != coords2.shape:
        return None
    distances = np.linalg.norm(coords1 - coords2, axis=1)
    return np.mean(distances)
