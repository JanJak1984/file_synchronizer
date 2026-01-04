

from dotenv import load_dotenv
from os import environ
from log_settings.settings import logger

load_dotenv()
token = environ.get('TOKEN')
path_in_yandex = environ.get('PATH_IN_YANDEX')
path_in_disk = environ.get('PATH_IN_DISK')
timeout = environ.get('TIMEOUT')


def clear_data():
    """ Проверяет все ли данные загружены в переменную среду """
    global timeout
    if all((token, path_in_yandex, path_in_disk, timeout)):
        logger.debug('Данные из переменной среды успешно получены')
    else:
        logger.error('Данные из переменной среды не были получены, проверьте наличие и правильную конфигурацию файла .env')
        raise ValueError(
            'Данные из переменной среды не были получены, проверьте наличие и правильную конфигурацию файла .env')
    try:
        timeout = int(timeout)
    except ValueError:
        logger.error(
            'timeout в .env не целое число!!!')
        raise ValueError(
            'timeout в .env не целое число!!!')
clear_data()
