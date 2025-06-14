import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    IWISP_API_KEY = os.getenv("IWISP_API_KEY")
    IWISP_API_URL = os.getenv("IWISP_API_URL")
    MONGO_URI = os.getenv("MONGO_URI")
    SECRET_KEY = "clave_secreta"
    UPLOAD_FOLDER = "uploads"