import logging
from logging.handlers import RotatingFileHandler


logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    filemode='w'
)

handler = RotatingFileHandler('main.log', maxBytes=50000000, backupCount=5)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)


def response_image_error():
    logging.error('Ошибка при подключении к основному API')
