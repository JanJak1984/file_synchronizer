from disk.get_info import get_files_info
from remote_disk.methods import Remote
import environs
from time import sleep
from log_settings.settings import logger


def syncronize(file_name: str, file_hash: str, remote_files: dict):
    """ Синхронизирует файл с названием file_name с хешем file_hash с директории PATH_IN_DISK в .env,
    информацию о удаленном хранилище берет с  remote_files (ключи-названия файлов, значения-хеши)
    """
    remote_hash = remote_files.pop(file_name, None)
    if file_hash != remote_hash:
        Remote.upload_file(file_name)


def loop() -> None:
    """ Цикл основной программы"""
    while True:
        remote_files = Remote.get_info()
        files = get_files_info()
        if not (remote_files is None) and not (files is None):
            for file_name, file_hash in files.items():
                syncronize(file_name, file_hash, remote_files)
            else:
                file_names = files.keys()
                [Remote.delete_file(file_name) for file_name in remote_files if not (file_name in file_names)]
                logger.info('Cинхронизация завершилась без ошибок')
        logger.debug(f'Следующая попытка синхронизации произойдет через {environs.timeout} секунд')
        sleep(environs.timeout)


def main() -> None:
    """ Основная функция программы, запускает цикл программы"""
    try:
        environs.clear_data()
        loop()
    except environs.CustomError as err:
        logger.error(f'{err}. Программа будет закрыта...')


if __name__ == '__main__':
    main()
