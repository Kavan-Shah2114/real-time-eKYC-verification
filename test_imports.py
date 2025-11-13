# """Test script to verify all required packages are installed."""
# import sys

# def test_imports():
#     """Test if all required packages can be imported."""
#     packages = {
#         'streamlit': 'Streamlit',
#         'cv2': 'OpenCV',
#         'easyocr': 'EasyOCR',
#         'deepface': 'DeepFace',
#         'mysql.connector': 'MySQL Connector',
#         'toml': 'TOML',
#         'yaml': 'PyYAML',
#         'pandas': 'Pandas',
#         'numpy': 'NumPy'
#     }
    
#     failed = []
#     success = []
    
#     for package, name in packages.items():
#         try:
#             __import__(package)
#             success.append(name)
#             print(f"[OK] {name} imported successfully")
#         except ImportError as e:
#             failed.append((name, str(e)))
#             print(f"[FAIL] {name} failed to import: {e}")
    
#     print("\n" + "="*50)
#     if failed:
#         print(f"[ERROR] {len(failed)} package(s) failed to import:")
#         for name, error in failed:
#             print(f"  - {name}: {error}")
#         return False
#     else:
#         print(f"[SUCCESS] All {len(success)} packages imported successfully!")
#         return True

# if __name__ == "__main__":
#     print("Testing package imports...")
#     print("="*50)
#     success = test_imports()
#     sys.exit(0 if success else 1)

from sql_connection import get_connection
conn = get_connection()
print("✅ Connected successfully!")
conn.close()