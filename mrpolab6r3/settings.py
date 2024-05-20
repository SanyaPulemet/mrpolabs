import os
from dotenv import load_dotenv

# Загрузка переменных из файла .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Получение значения переменной DB_CONNECTION_URL
DATABASE_URL = os.getenv("DATABASE_URL")