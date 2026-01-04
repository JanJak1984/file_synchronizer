import os.path
from typing import Optional

from environs import token, path_in_yandex, path_in_disk
from log_settings.settings import logger
from requests import get, put, delete
from requests.exceptions import ConnectionError


class Yandex:

    @staticmethod
    def get_info() -> Optional[dict]:
        """ Получает информацию о файлах в указанной директории яндекс диска
        в виде словаря, в качестве ключа которого имя файла, а значения-его sha256 хэш"""
        try:
            response = get(url=f'https://cloud-api.yandex.net/v1/disk/resources?path={path_in_yandex}',
                           headers={'Authorization': f'OAuth {token}'},
                           )
            status_code = response.status_code
            if status_code != 200:
                logger.error(
                    f"При попытке получения информации на сервере получен статус-код {status_code}."
                    "Возможно указан не верный токен либо папка, которая не существует на сервере"
                )
                return None
            else:
                files = {
                    object_['name']: object_['sha256'] for object_ in response.json().get('_embedded').get('items') if \
                    object_['type'] == 'file'
                }
                return files
        except ConnectionError:
            logger.error('Ошибка подключения, проверьте соединение...')

    @staticmethod
    def upload_file(filename: str):
        """ загружает файл на яндекс диск (в указанную в .env директорию) """
        headers = {"Authorization": f"OAuth {token}"}
        local_path = os.path.join(path_in_disk, filename)
        remote_path = f"{path_in_yandex}/{filename}"
        try:
            resp = get("https://cloud-api.yandex.net/v1/disk/resources/upload",
                       params={"path": remote_path, "overwrite": "true"}, headers=headers)
            upload_url = resp.json()["href"]
            try:
                with open(local_path, "rb") as f:
                    put(upload_url, files={"file": f})
                logger.info(f"Файл {filename} успешно загружен или перезаписан на Яндекс.Диске")
            except FileNotFoundError:
                logger.error(f"Файл {filename} не найден в дирректории диска")
        except ConnectionError:
            logger.error('Ошибка подключения, проверьте соединение...')

    @staticmethod
    def delete_file(filename: str) -> None:
        """ удаляет файл с именем filename с указанной в .env директории яндекс-диска """
        headers = {"Authorization": f"OAuth {token}"}
        remote_path = f"{path_in_yandex}/{filename}"
        try:
            resp = delete("https://cloud-api.yandex.net/v1/disk/resources", params={"path": remote_path},
                          headers=headers)
            status_code = resp.status_code
            if status_code == 204:
                logger.info(f"Файл {filename} успешно удален с Яндекс.Диска при синхронизации")
            else:
                logger.error(
                    f"При попытке удаления файла {filename} во время синхронизации получен статус-код {status_code}"
                )
        except ConnectionError:
            logger.error('Ошибка подключения, проверьте соединение...')
