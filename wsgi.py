import sys
import os

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from config import Config

app = create_app(Config) 