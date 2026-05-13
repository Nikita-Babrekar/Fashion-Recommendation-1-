# import cv2
# import numpy as np
# import os

# def detect_skin_tone(image_path):
#     # Check if file exists before trying to read
#     if not os.path.exists(image_path):
#         print(f"Error: File {image_path} not found.")
#         return None

#     img = cv2.imread(image_path)
#     if img is None:
#         print("Error: Could not decode image.")
#         return None

#     # Resize image if it's too large (improves detection speed and reliability)
#     height, width = img.shape[:2]
#     if width > 1000:
#         scaling = 1000 / width
#         img = cv2.resize(img, (1000, int(height * scaling)))

#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Load face detector with path safety
#     cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
#     face_cascade = cv2.CascadeClassifier(cascade_path)

#     if face_cascade.empty():
#         print("Error: Could not load Haar Cascade XML.")
#         return "medium" # Fallback so the app doesn't crash

#     # Detection - Adjusted parameters for better sensitivity
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
#     if len(faces) == 0:
#         print("No face detected, using global average as fallback.")
#         # Fallback: Instead of returning None (which crashes your app), 
#         # let's analyze the center of the image.
#         h, w, _ = img.shape
#         face = img[h//3:2*h//3, w//3:2*w//3]
#     else:
#         (x, y, w, h) = faces[0]
#         face = img[y:y+h, x:x+w]

#     # Convert to RGB for accurate brightness calculation
#     face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

#     # Take a representative sample from the center of the detected area
#     fh, fw, _ = face_rgb.shape
#     y1, y2 = int(fh * 0.3), int(fh * 0.6)
#     x1, x2 = int(fw * 0.3), int(fw * 0.6)
#     skin_sample = face_rgb[y1:y2, x1:x2]

#     if skin_sample.size == 0:
#         return "medium"

#     # Average color and brightness
#     avg_color = np.mean(skin_sample, axis=(0, 1))
    
    
#     # Using the standard luminance formula for better accuracy:
#     # Brightness = 0.299*R + 0.587*G + 0.114*B
#     brightness = 0.299 * avg_color[0] + 0.587 * avg_color[1] + 0.114 * avg_color[2]

#     print(f"Calculated Brightness: {brightness}")

#     if brightness > 180:
#         return "fair"
#     elif brightness > 90:
#         return "medium"
#     else:
#         return "deep"












import cv2
import numpy as np
import os


# ---------------- SKIN VALIDATION FUNCTION ----------------
def is_skin_color(sample):
    """
    Check if the given sample contains skin-like pixels
    using BOTH HSV and YCrCb color spaces (more accurate)
    """

    # Convert to HSV
    hsv = cv2.cvtColor(sample, cv2.COLOR_RGB2HSV)

    # Convert to YCrCb
    ycrcb = cv2.cvtColor(sample, cv2.COLOR_RGB2YCrCb)

    # HSV skin range
    lower_hsv = np.array([0, 30, 60], dtype=np.uint8)
    upper_hsv = np.array([20, 170, 255], dtype=np.uint8)
    mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # YCrCb skin range (more reliable for skin)
    lower_ycrcb = np.array([0, 135, 85], dtype=np.uint8)
    upper_ycrcb = np.array([255, 180, 135], dtype=np.uint8)
    mask_ycrcb = cv2.inRange(ycrcb, lower_ycrcb, upper_ycrcb)

    # Combine both masks
    combined_mask = cv2.bitwise_and(mask_hsv, mask_ycrcb)

    # Calculate ratio of skin pixels
    skin_ratio = np.sum(combined_mask > 0) / combined_mask.size

    print(f"Skin Ratio: {skin_ratio}")

    # Threshold (tuned)
    return skin_ratio > 0.35


# ---------------- MAIN FUNCTION ----------------
def detect_skin_tone(image_path):
    # Check file exists
    if not os.path.exists(image_path):
        print(f"Error: File {image_path} not found.")
        return None

    img = cv2.imread(image_path)
    if img is None:
        print("Error: Could not decode image.")
        return None

    # Resize large images
    height, width = img.shape[:2]
    if width > 1000:
        scaling = 1000 / width
        img = cv2.resize(img, (1000, int(height * scaling)))

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Load face detector
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)

    if face_cascade.empty():
        print("Error: Could not load Haar Cascade XML.")
        return "medium"

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Fallback if no face
    if len(faces) == 0:
        print("No face detected, using center fallback.")
        h, w, _ = img.shape
        face = img[h//3:2*h//3, w//3:2*w//3]
    else:
        (x, y, w, h) = faces[0]
        face = img[y:y+h, x:x+w]

    # Convert face to RGB
    face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

    # Extract center region (skin sample)
    fh, fw, _ = face_rgb.shape
    y1, y2 = int(fh * 0.3), int(fh * 0.6)
    x1, x2 = int(fw * 0.3), int(fw * 0.6)
    skin_sample = face_rgb[y1:y2, x1:x2]

    if skin_sample.size == 0:
        return "medium"

    # ---------------- VALIDATE SKIN ----------------
    if not is_skin_color(skin_sample):
        print("❌ Invalid: Not a human skin color")
        return "invalid"

    # ---------------- CALCULATE BRIGHTNESS ----------------
    avg_color = np.mean(skin_sample, axis=(0, 1))

    brightness = (
        0.299 * avg_color[0] +
        0.587 * avg_color[1] +
        0.114 * avg_color[2]
    )

    print(f"Brightness: {brightness}")

    # ---------------- CLASSIFY ----------------
    if brightness > 180:
        return "fair"
    elif brightness > 100:
        return "medium"
    else:
        return "deep"