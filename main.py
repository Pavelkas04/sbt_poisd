import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_restful import Api, Resource

# Инициализация Flask и API
app = Flask(__name__)
api = Api(app)

# Конфигурация через переменные окружения
LOG_LEVEL = os.getenv('LOG_SEVERITY', 'INFO')
PORT = int(os.getenv('SERVICE_PORT', 8000))
GREETING = os.getenv('GREETING', 'Welcome to the custom app')
LOG_FILE_PATH = '/app/journal/app.log'

# Настройка логгера
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE_PATH)
    ]
)
logger = logging.getLogger('journal_service')


class Root(Resource):
    def get(self):
        logger.info("Запрошен корневой маршрут")
        return GREETING


class HealthCheck(Resource):
    def get(self):
        logger.info("Запрошена проверка статуса")
        return {"status": "ok"}


class LogEntry(Resource):
    def post(self):
        data = request.get_json(force=True)
        message = data.get('message', '')
        logger.info(f"Новая запись: {message}")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(LOG_FILE_PATH, 'a') as file:
                file.write(f"[{timestamp}] {message}\n")
        except Exception as e:
            logger.error(f"Ошибка при записи в файл: {e}")
            return {"error": "Ошибка при записи"}, 500

        return {"result": "запись добавлена", "time": timestamp}


class LogView(Resource):
    def get(self):
        logger.info("Запрошено содержимого журнала")
        try:
            with open(LOG_FILE_PATH, 'r') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Ошибка при чтении журнала: {e}")
            return {"error": str(e)}, 500


# Регистрация маршрутов
api.add_resource(Root, '/')
api.add_resource(HealthCheck, '/status')
api.add_resource(LogEntry, '/log')
api.add_resource(LogView, '/logs')

# Запуск приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
