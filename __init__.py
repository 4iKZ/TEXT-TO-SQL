"""
SQL智能助手 - 模块化版本
"""

from config import *
from database import database_manager
from llm_model import llm_manager
from prompts.base_prompts import prompt_manager
from utils.sql_processor import sql_processor
from utils.data_formatter import data_formatter
from query_engine import query_engine
from app import main

__version__ = "2.0.0"
__author__ = "SQL Assistant Team"

# 导出主要组件
__all__ = [
    'database_manager',
    'llm_manager', 
    'prompt_manager',
    'sql_processor',
    'data_formatter',
    'query_engine',
    'main'
]