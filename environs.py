from dotenv import load_dotenv
from os import environ
from log_settings.settings import logger

load_dotenv()
token = environ.get('TOKEN')
path_in_remote = environ.get('PATH_IN_REMOTE')
timeout = environ.get('TIMEOUT')
resource = environ.get('RESOURCE')
path_in_disk = environ.get('PATH_IN_DISK')


class CustomError(Exception):
    pass


def clear_data():
    """ Проверяет все ли данные загружены в переменную среду """
    global timeout
    if all((token, path_in_disk, path_in_remote, timeout, resource)):
        logger.debug('Данные из переменной среды успешно получены')
    else:
        raise CustomError(
            'Данные из переменной среды не были получены, проверьте наличие и правильную конфигурацию файла .env')
    try:
        timeout = int(timeout)
    except ValueError:
        raise CustomError(
            'timeout в .env не целое число!!!')



