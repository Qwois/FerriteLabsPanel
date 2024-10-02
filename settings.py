import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

VALID_USERNAME = "1"

HASHED_PASSWORD = os.getenv("HASHED_PASSWORD")

if not HASHED_PASSWORD:
    password = "1"
    HASHED_PASSWORD = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    with open(".env", "a") as env_file:
        env_file.write(f"HASHED_PASSWORD={HASHED_PASSWORD}\n")

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
