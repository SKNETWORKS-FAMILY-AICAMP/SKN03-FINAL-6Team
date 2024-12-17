import time
import random
import hashlib
from threading import Lock

import asyncio

# 전역 변수
conversation_memory = {}
SESSION_EXPIRY_SECONDS = 3600  # 세션 만료 시간 (1시간)
memory_lock = Lock()

def generate_session_id() -> str:
    """고유한 세션 ID를 생성합니다."""
    MAX_ATTEMPTS = 10
    for _ in range(MAX_ATTEMPTS):
        random_number = random.randint(1000000000, 9999999999)
        session_id = hashlib.sha256(str(random_number).encode()).hexdigest()[:16]
        if session_id not in conversation_memory:
            return session_id
    raise RuntimeError("Failed to generate a unique session ID after multiple attempts.")

def initialize_session(session_id):
    """세션을 초기화합니다."""
    with memory_lock:
        if session_id not in conversation_memory:
            conversation_memory[session_id] = {
                "last_access": time.time(),
                "history": [],
            }

def update_session_access(session_id):
    """세션 접근 시 타임스탬프를 갱신합니다."""
    with memory_lock:
        if session_id in conversation_memory:
            conversation_memory[session_id]["last_access"] = time.time()

def cleanup_sessions():
    """만료된 세션을 정리합니다."""
    current_time = time.time()
    with memory_lock:
        expired_sessions = [
            session_id
            for session_id, session_data in conversation_memory.items()
            if (current_time - session_data["last_access"]) > SESSION_EXPIRY_SECONDS
        ]
        for session_id in expired_sessions:
            del conversation_memory[session_id]

async def periodic_cleanup():
    """정기적으로 만료된 세션을 정리합니다."""
    while True:
        cleanup_sessions()
        await asyncio.sleep(3600)  # 1시간 간격
