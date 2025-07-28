"""
数据库模块 - 处理数据库连接和操作
"""

import streamlit as st
from langchain_community.utilities import SQLDatabase
from config import DATABASE_URI


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self):
        self.db = None
        # 不在初始化时连接，而是在需要时连接
    
    def _connect(self):
        """建立数据库连接"""
        try:
            self.db = SQLDatabase.from_uri(DATABASE_URI)
        except Exception as e:
            st.error(f"数据库连接失败: {str(e)}")
            raise ConnectionError(f"数据库连接失败: {str(e)}")
    
    def get_database(self):
        """获取数据库实例"""
        if self.db is None:
            self._connect()
        return self.db
    
    def execute_query(self, sql_query):
        """执行SQL查询"""
        try:
            if self.db is None:
                self._connect()
            return self.db.run(sql_query)
        except Exception as e:
            st.error(f"查询执行失败: {str(e)}")
            return None
    
    def test_connection(self):
        """测试数据库连接"""
        try:
            if self.db is None:
                self._connect()
            # 执行简单的测试查询
            self.db.run("SELECT 1")
            return True
        except Exception as e:
            st.error(f"数据库连接测试失败: {str(e)}")
            return False


# 全局数据库管理器实例
database_manager = DatabaseManager()