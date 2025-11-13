import os
import logging
import streamlit as st
from preprocess import read_image, extract_id_card, save_image
from ocr_engine import extract_text
from postprocess import extract_information, extract_information1
from face_verification import detect_and_extract_face, deepface_face_comparison, get_face_embeddings
from sql_connection import (
    insert_records,
    fetch_records,
    check_duplicacy,
    insert_records_aadhar,
    fetch_records_aadhar,
    check_duplicacy_aadhar,
)
import hashlib
from datetime import datetime
from dotenv import load_dotenv

# -------------------------
# Logging & folders
# -------------------------
logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "ekyc_logs.log"),
    level=logging.INFO,
    format=logging_str,
    filemode="a",
)

# -------------------------
# Load environment variables (.env)
# -------------------------
load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST", "localhost")
db_name = os.getenv("DB_NAME", "ekyc")

if not db_user or not db_password:
    logging.error("Database credentials not found in .env file.")
else:
    logging.info(f"Loaded DB config: host={db_host}, user={db_user}, database={db_name}")


# -------------------------
# Helpers
# -------------------------
def hash_id(id_value: str) -> str:
    """Return SHA256 hex digest of given id string."""
    hash_object = hashlib.sha256(id_value.encode())
    return hash_object.hexdigest()


def wider_page():
    max_width_str = "max-width: 1200px;"
    st.markdown(
        f"""
        <style>
            .reportview-container .main .block-container{{ {max_width_str} }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    logging.info("Page layout set to wider configuration.")


def set_custom_theme():
    st.markdown(
        """
        <style>
            body {
                background-color: #f0f2f6;
                color: #333333;
            }
            .sidebar .sidebar-content {
                background-color: #ffffff;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    logging.info("Custom theme applied to Streamlit app.")


def sidebar_section():
    st.sidebar.title("Select ID Card Type")
    option = st.sidebar.selectbox("", ("PAN", "AADHAR"))
    logging.info(f"ID card type selected: {option}")
    return option


def header_section(option):
    if option == "AADHAR":
        st.title("Registration Using Aadhar Card")
        logging.info("Header set for Aadhar Card registration.")
    elif option == "PAN":
        st.title("Registration Using PAN Card")
        logging.info("Header set for PAN Card registration.")


# -------------------------
# Main content
# -------------------------
def main_content(image_file, face_image_file, option):
    """
    Main flow:
    - Read uploaded files
    - Extract ID ROI
    - Extract face from ID and from uploaded selfie
    - Verify faces
    - Run OCR and parse text into text_info
    - Normalize DOB, hash ID, check duplicates, insert to DB
    """
    if image_file is None:
        st.warning("Please upload an ID card image.")
        logging.warning("No ID card image uploaded.")
        return

    if face_image_file is None:
        st.error("Please upload a face image (selfie).")
        logging.error("No face image uploaded.")
        return

    # Read images (preprocess.read_image returns image array or None)
    face_image = read_image(face_image_file, is_uploaded=True)
    logging.info("Face image loaded.")
    if face_image is None:
        st.error("Could not read uploaded face image.")
        logging.error("read_image returned None for face_image.")
        return

    image = read_image(image_file, is_uploaded=True)
    logging.info("ID card image loaded.")
    if image is None:
        st.error("Could not read uploaded ID card image.")
        logging.error("read_image returned None for id image.")
        return

    # Extract ID ROI (image of the ID card area)
    image_roi, _ = extract_id_card(image)
    if image_roi is None:
        st.error("Could not detect ID card region. Please upload a clearer image.")
        logging.error("extract_id_card returned None.")
        return
    logging.info("ID card ROI extracted.")

    # Extract face from ID (we pass the image array)
    # detect_and_extract_face supports img= argument
    face_image_path2 = detect_and_extract_face(img=image_roi)
    # Save uploaded selfie to intermediate folder and get path
    face_image_path1 = save_image(face_image, "face_image.jpg", path=os.path.join("data", "02_intermediate_data"))
    logging.info(f"Faces extracted and saved: selfie={face_image_path1}, id_face={face_image_path2}")

    # Verify faces (DeepFace)
    try:
        is_face_verified = deepface_face_comparison(image1_path=face_image_path1, image2_path=face_image_path2)
    except Exception as e:
        logging.error(f"Face verification raised exception: {e}")
        is_face_verified = False

    logging.info(f"Face verification status: {'successful' if is_face_verified else 'failed'}.")

    if not is_face_verified:
        st.error("Face verification failed. Please try again with clearer images.")
        return

    # If verified, run OCR on the ID ROI
    extracted_text = None
    try:
        extracted_text = extract_text(image_roi)
        logging.info("OCR extraction completed.")
    except Exception as e:
        logging.error(f"OCR extraction failed: {e}")
        extracted_text = None

    if not extracted_text:
        st.warning("OCR did not extract text from the ID card. Please try a clearer picture.")
        logging.warning("OCR returned no text.")
        return

    # Parse OCR output into structured fields
    try:
        if option == "PAN":
            text_info = extract_information(extracted_text)
        else:
            text_info = extract_information1(extracted_text)
        logging.info(f"Parsed text_info: {text_info}")
    except Exception as e:
        logging.error(f"Failed to parse OCR text into fields: {e}")
        st.error("Failed to parse ID details. Please check the uploaded ID image.")
        return

    # Validate minimal keys
    if not text_info or "ID" not in text_info:
        st.error("Required fields not detected in OCR output (ID missing).")
        logging.error(f"text_info invalid or missing ID: {text_info}")
        return

    # Safe DOB parsing: many OCRs produce day/month/year or other formats
    dob_raw = text_info.get("DOB", None)
    dob_parsed = None
    if isinstance(dob_raw, datetime):
        dob_parsed = dob_raw
    elif isinstance(dob_raw, str):
        # try multiple common formats
        formats_to_try = ["%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%d.%m.%Y", "%d %b %Y", "%d %B %Y"]
        for fmt in formats_to_try:
            try:
                dob_parsed = datetime.strptime(dob_raw.strip(), fmt)
                break
            except Exception:
                dob_parsed = None
    # final normalized string or None
    text_info["DOB"] = dob_parsed.strftime("%Y-%m-%d") if dob_parsed else None

    # Hash ID before storing / displaying
    original_id_value = text_info.get("ID", "")
    hashed = hash_id(original_id_value)
    text_info["ID"] = hashed

    # Add embedding to record
    try:
        embedding = get_face_embeddings(face_image_path1)
        text_info["Embedding"] = embedding
    except Exception as e:
        logging.error(f"Failed to create embedding: {e}")
        text_info["Embedding"] = None

    # Show parsed info to user
    st.subheader("📄 Extracted Information")
    st.write("**Name:**", text_info.get("Name", "Not found"))
    st.write("**DOB:**", text_info.get("DOB", "Not found"))
    st.write("**ID (hashed):**", text_info.get("ID", "Not found"))
    st.write("**Gender:**", text_info.get("Gender", "Not found"))

    # Check duplicate and insert into DB
    try:
        if option == "PAN":
            records = fetch_records(text_info)
            is_duplicate = check_duplicacy(text_info)
        else:
            records = fetch_records_aadhar(text_info)
            is_duplicate = check_duplicacy_aadhar(text_info)
    except Exception as e:
        logging.error(f"DB lookup failed: {e}")
        st.error("Database error while checking duplicates.")
        return

    if records is not None and getattr(records, "shape", (0,))[0] > 0:
        st.info("Records found for this ID:")
        st.write(records)
    elif is_duplicate:
        st.warning(f"User already present with ID (hashed): {text_info['ID']}")
    else:
        # Insert new record
        try:
            if option == "PAN":
                insert_records(text_info)
            else:
                insert_records_aadhar(text_info)
            st.success("User verified and record inserted successfully.")
            logging.info(f"New user record inserted: {text_info.get('ID')}")
        except Exception as e:
            logging.error(f"Failed to insert record: {e}")
            st.error("Failed to insert record into database. Check logs.")

    # End of main_content


# -------------------------
# Main function
# -------------------------
def main():
    wider_page()
    set_custom_theme()
    option = sidebar_section()
    header_section(option)

    st.write("Upload your ID card image first, then upload your selfie (face image).")
    image_file = st.file_uploader("Upload ID Card", type=["jpg", "jpeg", "png"])
    if image_file is not None:
        face_image_file = st.file_uploader("Upload Face Image", type=["jpg", "jpeg", "png"])
        if st.button("Process"):
            main_content(image_file, face_image_file, option)


if __name__ == "__main__":
    main()