"""
模型模块 - 处理Ollama模型初始化和管理
"""

import streamlit as st
from langchain_ollama import OllamaLLM
from config import OLLAMA_CONFIG, AVAILABLE_MODELS, MODEL_CATEGORIES
from adapters.sqlcoder_adapter import SQLCoderAdapter


class LLMManager:
    """大语言模型管理器"""
    
    def __init__(self):
        self.llm = None
        self.current_model = None
        # SQLCoder适配器将在需要时动态创建，以便传递正确的模型名称
        # 不在初始化时连接，而是在需要时连接
    
    def _initialize_model(self, model_name=None):
        """初始化Ollama模型"""
        try:
            # 使用传入的模型名称，如果没有则使用配置中的默认模型
            model_to_use = model_name or OLLAMA_CONFIG["model"]
            
            self.llm = OllamaLLM(
                model=model_to_use,
                base_url=OLLAMA_CONFIG["base_url"],
                temperature=0
            )
            self.current_model = model_to_use
        except Exception as e:
            st.error(f"模型初始化失败: {str(e)}")
            raise ConnectionError(f"模型初始化失败: {str(e)}")
    
    def get_model(self, model_name=None):
        """获取模型实例"""
        # 如果没有模型实例，或者请求的模型与当前模型不同，则重新初始化
        if self.llm is None or (model_name and model_name != self.current_model):
            self._initialize_model(model_name)
        return self.llm
    
    def test_connection(self, model_name=None):
        """测试模型连接"""
        try:
            if self.llm is None or (model_name and model_name != self.current_model):
                self._initialize_model(model_name)
            # 执行简单的测试调用
            test_response = self.llm.invoke("Hello")
            return True
        except Exception as e:
            st.error(f"模型连接测试失败: {str(e)}")
            return False
    
    def get_model_info(self):
        """获取模型信息"""
        return {
            "model": self.current_model or OLLAMA_CONFIG["model"],
            "base_url": OLLAMA_CONFIG["base_url"],
            "temperature": 0
        }
    
    def get_available_models(self):
        """获取可用模型列表"""
        return AVAILABLE_MODELS
    
    def get_model_categories(self):
        """获取模型分类信息"""
        return MODEL_CATEGORIES
    
    def is_sqlcoder_model(self, model_name=None):
        """检查是否为SQLCoder专用模型"""
        model_to_check = model_name or self.current_model or OLLAMA_CONFIG["model"]
        
        # 检查模型名称中是否包含sqlcoder关键词
        model_lower = model_to_check.lower()
        sqlcoder_keywords = ['sqlcoder', 'sql-coder', 'defog-llama3-sqlcoder']
        
        return any(keyword in model_lower for keyword in sqlcoder_keywords)
    
    def generate_sql_with_sqlcoder(self, question: str, schema: dict, database_type: str = "MySQL", model_name: str = None):
        """
        使用SQLCoder模型生成SQL查询
        
        Args:
            question: 用户的自然语言问题
            schema: 数据库schema信息
            database_type: 数据库类型
            model_name: 指定的SQLCoder模型名称
            
        Returns:
            生成的SQL查询字符串
        """
        # 确定要使用的模型名称
        target_model = model_name or self.current_model or OLLAMA_CONFIG["model"]
        
        # 动态创建SQLCoder适配器，传递正确的模型名称
        sqlcoder_adapter = SQLCoderAdapter(model_name=target_model)
        
        if not sqlcoder_adapter.is_available():
            st.warning("SQLCoder模型不可用，请确保已安装并运行Ollama服务")
            return None
        
        return sqlcoder_adapter.generate_sql(question, schema, database_type)
    
    def test_sqlcoder_connection(self, model_name: str = None):
        """测试SQLCoder连接"""
        target_model = model_name or self.current_model or OLLAMA_CONFIG["model"]
        sqlcoder_adapter = SQLCoderAdapter(model_name=target_model)
        return sqlcoder_adapter.test_connection()
    
    def switch_model(self, model_name):
        """切换模型"""
        if model_name in AVAILABLE_MODELS:
            self._initialize_model(model_name)
            return True
        else:
            st.error(f"模型 {model_name} 不在可用模型列表中")
            return False


# 全局模型管理器实例
llm_manager = LLMManager()