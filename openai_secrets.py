from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env
SECRET_KEY = os.getenv("OPENAI_API_KEY")
