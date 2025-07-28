"""
SQL智能助手启动脚本 - 使用模块化版本
"""

import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 直接导入app模块中的main函数
from app import main

if __name__ == "__main__":
    main()