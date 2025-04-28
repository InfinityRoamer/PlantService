import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()  # Подгрузка переменных окружения из системы

host = os.getenv('SERVER')
port = int(os.getenv('PORT'))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
