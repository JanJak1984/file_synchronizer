from disk.get_info import get_files_info
from yandex_disk.methods_yandex import Yandex
from environs import timeout
from time import sleep
from log_settings.settings import logger


def syncronize(file_name: str, file_hash: str, remote_files: dict):
    remote_hash = remote_files.pop(file_name, None)
    if file_hash != remote_hash:
        Yandex.upload_file(file_name)


def loop():
    while True:
        remote_files = Yandex.get_info()
        files = get_files_info()
        if not (remote_files is None) and not (files is None):
            for file_name, file_hash in files.items():
                syncronize(file_name, file_hash, remote_files)
            else:
                file_names = files.keys()
                [Yandex.delete_file(file_name) for file_name in remote_files if not file_name in file_names]
                logger.info('Cинхронизация завершилась без ошибок')
        logger.debug(f'Следующая попытка синхронизации произойдет через {timeout} секунд')
        sleep(timeout)


if __name__ == '__main__':
    loop()
