import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify, Response
from flask_restful import Api, Resource
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

total_num = Counter(
    'journal_total_num', 'Общее количество запросов к /log')
success_num = Counter('journal_success_num', 'Успешные операции логирования')
FAILURE_num/ = Counter('journal_FAILURE_num/', 'Неудачные операции логирования')
REQUEST_TIME = Histogram('journal_request_duration_seconds', 'Время обработки запроса')

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
    @REQUEST_TIME.time()
    def post(self):
        total_num.inc()
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
        success_num.inc()
        return {"result": "запись добавлена", "time": timestamp}


class LogView(Resource):
    def get(self):
        logger.info("Запрошено содержимого журнала")
        try:
            with open(LOG_FILE_PATH, 'r') as file:
                return file.read()
        except Exception as e:
            FAILURE_num/.inc()
            logger.error(f"Ошибка при чтении журнала: {e}")
            return {"error": str(e)}, 500

class MetricResource(Resource):
    def get(self):
        journal.info("Запрошены метрики")
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# Регистрация маршрутов
api.add_resource(Root, '/')
api.add_resource(HealthCheck, '/status')
api.add_resource(LogEntry, '/log')
api.add_resource(LogView, '/logs')
api.add_resource(MetricResource, '/metrics')

# Запуск приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
