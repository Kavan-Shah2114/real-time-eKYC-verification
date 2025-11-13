# 🌐 E-KYC (Electronic Know Your Customer) Project  

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)
![MySQL](https://img.shields.io/badge/Database-MySQL-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

Welcome to the **E-KYC (Electronic Know Your Customer)** project!  
This project leverages **Computer Vision (CV)**, **Optical Character Recognition (OCR)**, and **Deep Learning (Face Embedding Models)** to automate and simplify the KYC verification process.  

---

## 🧾 Overview

The **E-KYC web application** is built using **Streamlit** and allows users to upload:  
- An **ID card** (currently supports **Aadhar** and **PAN**)  
- A **selfie image**

The system automatically:
1. Detects and extracts the face from the ID card.  
2. Verifies the extracted face with the uploaded selfie using **DeepFace**.  
3. Uses **EasyOCR** to extract textual information from the ID card.  
4. Stores the verified and processed data securely in a **MySQL database**, using hashed IDs for privacy.

---

## ✨ Features

### 1️⃣ Face Verification  
- Detects and compares faces using **DeepFace (FaceNet backend)** and **OpenCV**.  
- If the faces don’t match, the process stops automatically.  

#### Face Verification Demo
![E-KYC Face Verification Demo](https://github.com/abhishekiiitbh2903/E-KYC-/blob/main/assets/Face%20Verification.gif)

Here, I uploaded an ID card of my dad and a selfie of myself. The verification failed — as expected — preventing further execution.

---

### 2️⃣ Optical Character Recognition (OCR)  
- Uses **EasyOCR** to extract text such as Name, DOB, Gender, and ID Number from ID cards.  

---

### 3️⃣ Database Interaction  
- Data is securely stored in a **MySQL database**.  
- Prevents duplicate entries using an automatic **duplicate check** mechanism.  
- Stores **face embeddings** and **hashed IDs** to ensure user privacy.  

---

### 4️⃣ Face Embeddings  
- Uses **FaceNet (via DeepFace)** to retrieve face embeddings stored in the database.

---

### 5️⃣ Security  
- Sensitive data (like ID numbers) are **hashed with SHA256**.  
- Database credentials are stored securely in a **`.env`** file (excluded from Git).  
- Extensive logging ensures transparency and debugging traceability.  

---

## 🧠 Full Workflow of the Web App

![Full Workflow](https://github.com/abhishekiiitbh2903/E-KYC-/blob/main/assets/Full%20Workflow.gif)

Example:  
- Uploading mismatched faces stops execution immediately.  
- Uploading a matching face stores verified data in the database.  
- Re-uploading triggers duplicate detection.

---

## 🧩 Technologies Used  

| Technology | Purpose |
|-------------|----------|
| **Streamlit** | Interactive web UI |
| **OpenCV** | Face detection & image processing |
| **DeepFace (FaceNet)** | Face verification & embeddings |
| **EasyOCR** | Text extraction from ID cards |
| **MySQL** | Data storage |
| **python-dotenv** | Secure credential handling |
| **Pandas** | Data handling |
| **TensorFlow** | Backend for DeepFace models |

---

## 🚧 Upcoming Improvements

1. **Live Face Detection** — integrate webcam for real-time capture.  
2. **Data Privacy** — full data hashing before storage. ✅ Completed  

---

## ⚙️ Prerequisites

Ensure you have the following installed:
- **Python 3.12**
- **MySQL server**

---

## 🛠️ Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/Kavan-Shah2114/eKYC.git
cd eKYC/

```
---

### Step 2: **Create and Activate Conda Environment**
```bash
conda create --name ekyc python=3.12 -y

```
---

### Step 3: **Activate the Virtual Environment**:
- On Windows:
```bash
conda activate ekyc

```
---

### Step 4: **Install the Required Packages**:
```bash
pip install -r requirements.txt

```
---

### 🧩 Step 5: Create a `.env` File for Database Credentials

In your project’s root directory, create a new file named **`.env`** and add your MySQL credentials as shown below:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=ekyc
```

⚠️ Important Note:
🔒 Do not upload this file to GitHub — it contains sensitive credentials.
🧾 The .gitignore file already includes .env, so it will be automatically ignored by Git.
✅ Always keep your .env file secure and private.   

---

### ⚙️ Step 6: Initialize Database Tables

Run the following command to automatically create the required tables (**users** and **aadhar**) in your MySQL database:

```bash
python setup_database.py
```

🗃️ Note:
Make sure your MySQL server is running and the .env file is properly configured before executing this command.

---

### 🔹 Step 7: Run the E-KYC Streamlit Application

To start the Streamlit application, run the following command in your terminal:

```bash
streamlit run app.py
```

Once executed successfully, open your browser and navigate to:

```bash
👉 http://localhost:8501
```

You can now:

📤 Upload your ID card and face image

🧠 Perform face verification

🔍 Extract data using OCR-based text recognition

---

### 🗂️ Project Structure

The folder structure of the **E-KYC** project is organized as follows:

```text
eKYC/
│
├── app.py                 # Main Streamlit application
├── preprocess.py          # Image preprocessing (OpenCV)
├── ocr_engine.py          # OCR (EasyOCR)
├── postprocess.py         # Text parsing and data extraction
├── face_verification.py   # DeepFace-based face verification logic
├── sql_connection.py      # MySQL connection and database operations
├── setup_database.py      # Script to initialize DB and tables
│
├── .env                   # Environment variables (ignored by Git)
├── .gitignore             # Ignore unnecessary or sensitive files
├── requirements.txt       # All dependencies for the project
└── logs/                  # Log files for error tracking and monitoring
```

---

### 🧾 Logging

All major events — including database connections, OCR results, and face verification outcomes — are automatically logged under:

logs/ekyc_logs.log


---

#### 📋 Logs Include:
- ✅ **Database connection attempts and results**  
- ✅ **OCR extraction details**  
- ✅ **Face verification success/failure status**  
- ✅ **Data insertion or duplicate detection information**

---

> ⚠️ **Note:**  
> The `logs/` directory is **excluded from GitHub** for privacy and security reasons.

---

### 🚨 Troubleshooting

| 🧩 **Issue** | 💡 **Solution** |
|--------------|----------------|
| ❌ **Database connection failed** | Ensure MySQL is running and your `.env` file contains the correct credentials. |
| ⚠️ **ModuleNotFoundError** | Run `pip install -r requirements.txt` again to install missing dependencies. |
| ⚠️ **Face not detected** | Upload a clear, front-facing photo with proper lighting. |
| ⚠️ **AttributeError: 'str' object has no attribute 'strftime'** | ✅ Fixed — the current version automatically handles multiple date formats. |

---

### 🚀 Future Enhancements

| 🧠 **Feature** | 📈 **Status / Description** |
|----------------|-----------------------------|
| ✅ **Sensitive Data Hashing** | Implemented for secure storage of user information. |
| 🔜 **Live Webcam-Based Face Detection** | To enable real-time face verification through the user’s webcam. |
| 🔜 **Admin Dashboard** | For viewing analytics, user verification logs, and system performance metrics. |
| 🔜 **REST API Support** | To integrate KYC verification with mobile and third-party applications. |

---

### 👨‍💻 Author

**Kavan Shah**    

💡 Passionate about **AI** and **Scalable MLOps Solutions**  

📧 **Email:** [kavanshah2114@gmail.com](mailto:kavanshah2114@gmail.com)  
🌐 **GitHub:** [Kavan-Shah2114](https://github.com/Kavan-Shah2114)

---

### 🤝 Contributing

Contributions and suggestions are always welcome! 💬  

To contribute:
1. 🍴 **Fork** the repository  
2. 🛠️ **Make improvements** or add new features  
3. 🔁 **Create a pull request**

If your work adds value to the project, it will be **merged and credited** accordingly. 🙌

--- 

### 🛡️ License

This project is **open-source** under the **MIT License**.  

You are free to **use**, **modify**, and **distribute** this project — responsibly and with proper credit.  

📄 For more details, refer to the [LICENSE](LICENSE) file.

---

### 🎥 Demo Showcase

>“**Upload an ID → Verify Face → Extract Data → Store Securely — all in one go.**”  

Experience the seamless **E-KYC verification process** powered by  
🧠 *AI, Computer Vision, and OCR integration* — all in a single streamlined workflow.


## 🧩 E-KYC System Workflow  

Here’s a clear overview of how the **E-KYC application** processes and verifies identity in real-time:  

            ┌──────────────────────────────┐
            │       Upload ID Card         │
            └─────────────┬────────────────┘
                          │
                          ▼
               preprocess.py (OpenCV)
                          │
                          ▼
               OCR Engine → EasyOCR
                          │
                          ▼
               extract_text() → Extracts Name, DOB, ID
                          │
                          ▼
            ┌──────────────────────────────┐
            │       Upload Selfie Image    │
            └─────────────┬────────────────┘
                          │
                          ▼
             face_verification.py (DeepFace)
                          │
                          ▼
               DeepFace → Compare Embeddings
                          │
           ┌──────────────┴──────────────┐
           │                             │
    Faces Matched ✅             Faces Mismatch ❌
           │                             │
           ▼                             ▼


sql_connection.py → Store in MySQL Display Error in Streamlit
│
▼
Streamlit App → Displays Extracted Info, Status & Logs



💡 **Explanation:**  
1. The user uploads their **ID card** and **selfie**.  
2. The system uses **OpenCV** to detect and crop the ID region.  
3. **EasyOCR** extracts textual data like *Name, DOB, Gender, ID Number*.  
4. **DeepFace (FaceNet)** compares the extracted face from ID and selfie.  
5. If both faces match, data is securely stored in the **MySQL** database using **hashed IDs**.  
6. The **Streamlit UI** displays all extracted information, verification result, and logging insights.

---

## 🧠 Simplified Process Flow  

```text
[Upload ID Card] → preprocess.py → OCR (EasyOCR) → extract_text
↓
[Upload Selfie] → face_verification.py → DeepFace → verify match
↓
[Match?] → YES → sql_connection.py → store in MySQL
↓
Streamlit → Displays extracted info & verification result
```

✅ **Outcome:**  
- Fully automated ID verification pipeline  
- Secure database integration  
- Transparent front-end interaction  
- Privacy-first (hashed data storage)  

---

## 🖼️ Visual Overview  

If you prefer, you can also upload this as an image in your repo (recommended filename: `architecture.png`) and embed it below:  

```markdown
![E-KYC System Architecture](https://github.com/Kavan-Shah2114/eKYC/blob/main/assets/architecture.png)