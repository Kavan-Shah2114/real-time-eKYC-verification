import mysql.connector
import pandas as pd
import logging
import os
from dotenv import load_dotenv

# ---------------------------------------
# Logging configuration
# ---------------------------------------
logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "ekyc_logs.log"),
    level=logging.INFO,
    format=logging_str,
    filemode="a",
)

# ---------------------------------------
# Load environment variables from .env
# ---------------------------------------
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "ekyc")

if not DB_USER or not DB_PASSWORD:
    logging.error("Database user or password not found in .env file.")
    raise ValueError("Database user or password not found in .env file")

# ---------------------------------------
# Connection helper
# ---------------------------------------
def get_connection():
    """Establish and return a new MySQL connection."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        logging.info("✅ Database connection established successfully.")
        return conn
    except mysql.connector.Error as err:
        logging.error(f"❌ Database connection failed: {err}")
        raise


# ---------------------------------------
# Insert Records
# ---------------------------------------
def insert_records(text_info):
    """Insert PAN user record into users table."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO users (id, name, father_name, dob, id_type, embedding)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            text_info.get("ID"),
            text_info.get("Name"),
            text_info.get("Father's Name"),
            text_info.get("DOB"),
            text_info.get("ID Type"),
            str(text_info.get("Embedding")),
        )
        cursor.execute(sql, values)
        conn.commit()
        logging.info("✅ Record inserted successfully into 'users' table.")
    except Exception as e:
        logging.error(f"❌ Error inserting record into 'users' table: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def insert_records_aadhar(text_info):
    """Insert Aadhar user record into aadhar table."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO aadhar (id, name, gender, dob, id_type, embedding)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            text_info.get("ID"),
            text_info.get("Name"),
            text_info.get("Gender"),
            text_info.get("DOB"),
            text_info.get("ID Type"),
            str(text_info.get("Embedding")),
        )
        cursor.execute(sql, values)
        conn.commit()
        logging.info("✅ Record inserted successfully into 'aadhar' table.")
    except Exception as e:
        logging.error(f"❌ Error inserting record into 'aadhar' table: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ---------------------------------------
# Fetch Records
# ---------------------------------------
def fetch_records(text_info):
    """Fetch record from users table by ID."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM users WHERE id = %s"
        cursor.execute(sql, (text_info.get("ID"),))
        result = cursor.fetchall()
        if result:
            df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
            logging.info("✅ Record fetched successfully from 'users' table.")
            return df
        else:
            logging.info("No record found in 'users' table.")
            return pd.DataFrame()
    except Exception as e:
        logging.error(f"❌ Error fetching record from 'users': {e}")
        return pd.DataFrame()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def fetch_records_aadhar(text_info):
    """Fetch record from aadhar table by ID."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM aadhar WHERE id = %s"
        cursor.execute(sql, (text_info.get("ID"),))
        result = cursor.fetchall()
        if result:
            df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
            logging.info("✅ Record fetched successfully from 'aadhar' table.")
            return df
        else:
            logging.info("No record found in 'aadhar' table.")
            return pd.DataFrame()
    except Exception as e:
        logging.error(f"❌ Error fetching record from 'aadhar': {e}")
        return pd.DataFrame()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ---------------------------------------
# Duplicate Check
# ---------------------------------------
def check_duplicacy(text_info):
    """Check if record already exists in users table."""
    try:
        df = fetch_records(text_info)
        if not df.empty:
            logging.info("⚠️ Duplicate record found in 'users' table.")
            return True
        else:
            logging.info("✅ No duplicate found in 'users' table.")
            return False
    except Exception as e:
        logging.error(f"❌ Error checking duplicacy in 'users': {e}")
        return False


def check_duplicacy_aadhar(text_info):
    """Check if record already exists in aadhar table."""
    try:
        df = fetch_records_aadhar(text_info)
        if not df.empty:
            logging.info("⚠️ Duplicate record found in 'aadhar' table.")
            return True
        else:
            logging.info("✅ No duplicate found in 'aadhar' table.")
            return False
    except Exception as e:
        logging.error(f"❌ Error checking duplicacy in 'aadhar': {e}")
        return False