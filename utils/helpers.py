"""
辅助函数工具类
"""
import os
import json
import random
import string
from typing import Any, Dict
from pathlib import Path


def read_json(file_path: str) -> Dict[str, Any]:
    """读取JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(file_path: str, data: Dict[str, Any]):
    """写入JSON文件"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_random_string(length: int = 10) -> str:
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_random_email() -> str:
    """生成随机邮箱"""
    return f"{generate_random_string(8)}@test.com"


def wait_for_file(file_path: str, timeout: int = 30) -> bool:
    """等待文件出现"""
    import time
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time > timeout:
            return False
        time.sleep(0.5)
    return True


def get_project_root() -> Path:
    """获取项目根目录"""
    return Path(__file__).parent.parent


def ensure_dir(directory: str):
    """确保目录存在"""
    os.makedirs(directory, exist_ok=True)

