import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    IWISP_API_KEY = os.getenv("IWISP_API_KEY")
    IWISP_API_URL = os.getenv("IWISP_API_URL")
    UPLOAD_FOLDER = "uploads"
    SECRET_KEY = os.getenv("SECRET_KEY")

    # ⚡ En el futuro aquí puedes agregar tu conexión a Supabase
    # SUPABASE_URL = os.getenv("SUPABASE_URL")
    # SUPABASE_KEY = os.getenv("SUPABASE_KEY")
