"""
Database setup script for E-KYC project.
This script creates the required MySQL database and tables for PAN and Aadhar users.
"""

import mysql.connector
import toml
import os
import logging

# Logging configuration
logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, "database_setup.log"), level=logging.INFO, format=logging_str, filemode="a")

def create_database_and_tables():
    """Create database and tables if they don't exist."""
    
    # Check if config.toml exists
    if not os.path.exists("config.toml"):
        print("ERROR: config.toml file not found!")
        print("Please create config.toml file with your database credentials.")
        print("You can use config.toml.example as a template.")
        logging.error("config.toml file not found")
        return False
    
    # Load database configuration from config.toml
    try:
        config = toml.load("config.toml")
        db_config = config.get("database", {})
        
        db_user = db_config.get("user")
        db_password = db_config.get("password")
        db_host = db_config.get("host", "localhost")
        db_name = db_config.get("database")
        
        if not db_user or not db_password or not db_name:
            print("ERROR: Database credentials not found in config.toml")
            logging.error("Database credentials not found in config.toml")
            return False
            
    except Exception as e:
        print(f"ERROR: Failed to load config.toml: {e}")
        logging.error(f"Failed to load config.toml: {e}")
        return False
    
    try:
        # Connect to MySQL server (without database)
        print(f"Connecting to MySQL server at {db_host}...")
        mydb = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            port=3306
        )
        mycursor = mydb.cursor()
        logging.info("Connected to MySQL server")
        
        # Create database if it doesn't exist
        print(f"Creating database '{db_name}' if it doesn't exist...")
        mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        logging.info(f"Database '{db_name}' created or already exists")
        
        # Use the database
        mycursor.execute(f"USE {db_name}")
        
        # Create users table (for PAN cards)
        print("Creating 'users' table for PAN cards...")
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            father_name VARCHAR(255),
            dob DATE NOT NULL,
            id_type VARCHAR(50) NOT NULL,
            embedding TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        mycursor.execute(create_users_table)
        logging.info("Table 'users' created or already exists")
        
        # Create aadhar table
        print("Creating 'aadhar' table for Aadhar cards...")
        create_aadhar_table = """
        CREATE TABLE IF NOT EXISTS aadhar (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            gender VARCHAR(50),
            dob DATE NOT NULL,
            id_type VARCHAR(50) NOT NULL,
            embedding TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        mycursor.execute(create_aadhar_table)
        logging.info("Table 'aadhar' created or already exists")
        
        # Commit changes
        mydb.commit()
        mycursor.close()
        mydb.close()
        
        print("Database setup completed successfully!")
        print(f"Database: {db_name}")
        print("Tables created: users, aadhar")
        logging.info("Database setup completed successfully")
        return True
        
    except mysql.connector.Error as err:
        print(f"ERROR: Database error: {err}")
        logging.error(f"Database error: {err}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        logging.error(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("E-KYC Database Setup")
    print("=" * 50)
    success = create_database_and_tables()
    if success:
        print("\nYou can now run the Streamlit app with: streamlit run app.py")
    else:
        print("\nPlease fix the errors and try again.")
    print("=" * 50)

