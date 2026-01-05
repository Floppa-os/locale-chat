import os
import hashlib

def get_file_hash(filepath):
    """Получить хеш файла для проверки целостности"""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def split_file(filepath, chunk_size=1024*1024):
    """Разбить файл на чанки"""
    chunks = []
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            chunks.append(chunk)
    return chunks
