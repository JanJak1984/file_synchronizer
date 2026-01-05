import os
from typing import Optional

from environs import path_in_remote
from log_settings.settings import logger
import hashlib


def path_is_exists(path_file_in_disk: str) -> None:
    """ Проверяет, существует ли путь и является ли он папкой, если нет, вызывает ValueError """
    if os.path.exists(path_file_in_disk) and os.path.isdir(path_file_in_disk):
        return None
    logger.error(f'Путь {path_file_in_disk} не найден или не является папкой')
    raise ValueError(f'Путь {path_file_in_disk} не найден или не является папкой')


def calc_hash(path: str, algo: str = "md5") -> str:
    # создаём объект хэш-функции
    hasher = hashlib.new(algo)
    # читаем файл блоками, чтобы работать даже с большими файлами
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_files_info() -> Optional[dict]:
    """ получает словарь из файлов в указанной папке на диске, в котором ключ - название файла,
    значение - его хэш """
    try:
        path_is_exists(path_in_remote)
    except ValueError:
        return None
    files = {}
    for filename in os.listdir(path_in_remote):
        filepath = os.path.join(path_in_remote, filename)
        if os.path.isfile(filepath):
            files[filename] = calc_hash(filepath, 'sha256')
    return files
