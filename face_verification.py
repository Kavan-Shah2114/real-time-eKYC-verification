import os
import cv2
import numpy as np
import warnings
from deepface import DeepFace

# === Suppress DeepFace & TensorFlow logs ===
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)


def detect_and_extract_face(image_path=None, img=None):
    """
    Detect and crop the largest face in the image.
    Accepts both file path or OpenCV image array.
    Returns the cropped face path.
    """
    try:
        if img is not None:
            input_img = img
        elif image_path and os.path.exists(image_path):
            input_img = cv2.imread(image_path)
        else:
            print("❌ Invalid input to detect_and_extract_face()")
            return None

        gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        if len(faces) == 0:
            print("⚠️ No face detected. Using original image.")
            if image_path:
                return image_path
            else:
                temp_path = "temp_original.jpg"
                cv2.imwrite(temp_path, input_img)
                return temp_path

        # Pick the largest face
        faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
        (x, y, w, h) = faces[0]
        face = input_img[y:y + h, x:x + w]

        save_path = image_path.replace(".jpg", "_face.jpg") if image_path else "temp_face.jpg"
        cv2.imwrite(save_path, face)
        print(f"✅ Face extracted: {save_path}")
        return save_path

    except Exception as e:
        print(f"❌ Error in detect_and_extract_face(): {e}")
        return image_path


def normalize_face(image_path):
    """Resize faces to standard 224x224 for consistent embeddings."""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return image_path
        resized = cv2.resize(img, (224, 224))
        cv2.imwrite(image_path, resized)
        return image_path
    except Exception as e:
        print(f"⚠️ Error normalizing {image_path}: {e}")
        return image_path


def show_faces_side_by_side(img1_path, img2_path, verified, distance, threshold):
    """Display both faces side-by-side with match info."""
    try:
        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)
        if img1 is None or img2 is None:
            return

        img1 = cv2.resize(img1, (250, 250))
        img2 = cv2.resize(img2, (250, 250))
        combined = np.hstack((img1, img2))

        label = f"Match: {verified} | Distance: {distance:.3f} | Threshold: {threshold:.2f}"
        color = (0, 255, 0) if verified else (0, 0, 255)
        cv2.putText(combined, label, (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow("Face Comparison", combined)
        cv2.waitKey(2500)
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"⚠️ Unable to display faces: {e}")


def deepface_face_comparison(image1_path, image2_path):
    """
    Compare two faces using DeepFace (Facenet512).
    Returns True/False based on manual similarity threshold.
    """
    try:
        # Step 1: Detect & normalize
        img1_processed = normalize_face(detect_and_extract_face(image_path=image1_path))
        img2_processed = normalize_face(detect_and_extract_face(image_path=image2_path))

        print("🔍 Running DeepFace verification using Facenet512 model...")

        # Step 2: Run DeepFace verification
        result = DeepFace.verify(
            img1_path=img1_processed,
            img2_path=img2_processed,
            model_name="Facenet512",
            detector_backend="opencv",
            distance_metric="cosine",
            enforce_detection=False
        )

        # Step 3: Extract results
        distance = result.get("distance", 1.0)
        threshold = 0.7  # Custom threshold for Facenet512 + cosine
        verified = distance <= threshold

        # Step 4: Show results visually
        show_faces_side_by_side(img1_processed, img2_processed, verified, distance, threshold)

        print(f"\nModel: Facenet512")
        print(f"Distance: {distance:.3f}")
        print(f"Threshold: {threshold:.2f}")
        print(f"✅ Result: {'MATCH ✅' if verified else 'MISMATCH ❌'}")

        return verified

    except Exception as e:
        print(f"❌ DeepFace verification failed: {e}")
        return False


def get_face_embeddings(image_path):
    """Extracts 512D facial embeddings for database use."""
    try:
        embedding = DeepFace.represent(
            img_path=image_path,
            model_name="Facenet512",
            enforce_detection=False
        )
        print(f"✅ Embedding extracted for {image_path}")
        return embedding[0]["embedding"]
    except Exception as e:
        print(f"❌ Failed to extract embedding: {e}")
        return None


# === Optional quick test ===
if __name__ == "__main__":
    img1 = "contour_id.jpg"        # Replace with your ID image
    img2 = "extracted_face.jpg"    # Replace with your selfie
    result = deepface_face_comparison(img1, img2)
    print("\nFinal Verification:", "✅ MATCH" if result else "❌ MISMATCH")