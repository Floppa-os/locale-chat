import json

def create_message(sender, text, file_path=None):
    """Создать сообщение (текст + файл)"""
    msg = {
        'type': 'message',
        'sender': sender,
        'text': text,
        'file': file_path is not None,
        'timestamp': int(time.time())
    }
    return json.dumps(msg).encode('utf-8')

def create_file_chunk(chunk, chunk_id, total_chunks):
    """Создать чанк файла"""
    return {
        'type': 'file_chunk',
        'chunk_id': chunk_id,
        'total_chunks': total_chunks,
        'data': chunk
    }

def parse_message(data):
    """Разобрать байтовую строку в словарь"""
    try:
        return json.loads(data.decode('utf-8'))
    except:
        return None
