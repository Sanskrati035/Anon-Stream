import cv2
import mediapipe as mp
import numpy as np
import os
import time
import pyvirtualcam

# --- Setup Paths ---
base_dir = os.path.dirname(os.path.abspath(__file__))
seg_model_path = os.path.join(base_dir, 'selfie_segmenter.tflite')
face_model_path = os.path.join(base_dir, 'face_detector.tflite')

# --- MediaPipe Setup ---
BaseOptions = mp.tasks.BaseOptions
ImageSegmenter = mp.tasks.vision.ImageSegmenter
ImageSegmenterOptions = mp.tasks.vision.ImageSegmenterOptions
FaceDetector = mp.tasks.vision.FaceDetector
FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
VisionRunningMode = mp.tasks.vision.RunningMode

seg_options = ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path=seg_model_path),
    running_mode=VisionRunningMode.VIDEO, output_category_mask=True
)
face_options = FaceDetectorOptions(
    base_options=BaseOptions(model_asset_path=face_model_path),
    running_mode=VisionRunningMode.VIDEO, min_detection_confidence=0.3
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
last_frame = None 

# --- VIRTUAL CAMERA INITIALIZATION ---
try:
    vcam = pyvirtualcam.Camera(width=640, height=480, fps=20, fmt=pyvirtualcam.PixelFormat.RGB)
    print(f'🚀 VGuard Engine Active (Clean Mode)')
except Exception as e:
    print(f"❌ Error: {e}")
    exit()

# Sab kuch is "with vcam" ke andar hi hona chahiye
with vcam:
    with ImageSegmenter.create_from_options(seg_options) as segmenter, \
         FaceDetector.create_from_options(face_options) as detector:
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break

            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (640, 480))
            h, w, _ = frame.shape
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            timestamp_ms = int(time.time() * 1000)

            # --- AI PROCESSING ---
            seg_result = segmenter.segment_for_video(mp_image, timestamp_ms)
            category_mask = seg_result.category_mask.numpy_view()
            is_foreground = np.logical_not(category_mask > 0.5)
            if is_foreground.ndim == 3: is_foreground = is_foreground[:,:,0]

            process_buffer = frame.copy()
            
            # --- INTRUDER DETECTION & PIXELATION ---
            face_result = detector.detect_for_video(mp_image, timestamp_ms)
            frame_center_x = w // 2

            if face_result.detections:
                for detection in face_result.detections:
                    bbox = detection.bounding_box
                    fx, fy, fw, fh = int(bbox.origin_x), int(bbox.origin_y), int(bbox.width), int(bbox.height)
                    
                    if abs((fx + fw//2) - frame_center_x) > 130:
                        y1, y2, x1, x2 = max(0, fy), min(h, fy+fh), max(0, fx), min(w, fx+fw)
                        face_roi = frame[y1:y2, x1:x2]
                        if face_roi.size > 0:
                            small = cv2.resize(face_roi, (8, 8), interpolation=cv2.INTER_LINEAR)
                            pixelated = cv2.resize(small, (x2-x1, y2-y1), interpolation=cv2.INTER_NEAREST)
                            process_buffer[y1:y2, x1:x2] = pixelated

            final_output = process_buffer
            last_frame = final_output.copy()

            # --- SEND TO VIRTUAL CAM ---
            vcam_frame = cv2.cvtColor(final_output, cv2.COLOR_BGR2RGB)
            vcam.send(vcam_frame)
            vcam.sleep_until_next_frame()

            cv2.imshow('VGuard: Privacy Shield', final_output)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("🛑 Stopping stream...")
                break

        # --- THE FIX: Freeze Frame loop inside the "with" block ---
        if last_frame is not None:
            # Last image par "STAY SAFE" ya kuch likhna ho toh (Optional)
            vcam_end_frame = cv2.cvtColor(last_frame, cv2.COLOR_BGR2RGB)
            print("❄️ Freezing last frame for 2 seconds...")
            for _ in range(40): # Send the last frame 40 times (approx 2 sec)
                vcam.send(vcam_end_frame)
                vcam.sleep_until_next_frame()

cap.release()
cv2.destroyAllWindows()