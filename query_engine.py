"""
查询引擎模块 - 整合LLM和数据库查询功能
"""

import streamlit as st
from typing import Optional, Tuple, Any
from database import database_manager
from llm_model import llm_manager
from prompts.base_prompts import prompt_manager
from utils.sql_processor import sql_processor
from utils.data_formatter import data_formatter
from utils.schema_converter import SchemaConverter


class QueryEngine:
    """查询引擎 - 整合所有查询相关功能"""
    
    def __init__(self):
        self.db_manager = database_manager
        self.llm_manager = llm_manager
        self.prompt_manager = prompt_manager
        self.sql_processor = sql_processor
        self.data_formatter = data_formatter
        self.schema_converter = SchemaConverter()
    
    def execute_natural_language_query(self, user_question: str, model_name: str) -> Tuple[bool, Any, str, str]:
        """
        执行自然语言查询
        
        Returns:
            Tuple[bool, Any, str, str]: (成功标志, 查询结果, SQL语句, 错误信息)
        """
        try:
            # 获取数据库实例
            db = self.db_manager.get_database()
            if not db:
                return False, None, "", "数据库未正确初始化"
            
            # 检查是否为SQLCoder模型
            if self.llm_manager.is_sqlcoder_model(model_name):
                # 使用SQLCoder专用适配器
                st.info(f"🔧 检测到SQLCoder模型: {model_name}，使用专用提示词")
                
                # 获取schema信息
                schema = self.schema_converter.get_sqlcoder_schema()
                
                # 使用SQLCoder适配器生成SQL
                with st.spinner("正在使用SQLCoder生成SQL查询..."):
                    sql_query = self.llm_manager.generate_sql_with_sqlcoder(
                        user_question, schema, "MySQL", model_name
                    )
                
                if not sql_query:
                    return False, None, "", "SQLCoder无法生成有效的SQL查询"
                    
            else:
                # 使用通用LLM模型和提示词
                st.info(f"🤖 使用通用模型: {model_name}，使用标准提示词")
                
                llm = self.llm_manager.get_model(model_name)
                if not llm:
                    return False, None, "", "LLM模型未正确初始化"
                
                # 创建SQL查询链
                sql_chain = self.prompt_manager.create_sql_chain(llm, db)
                
                # 生成SQL查询
                with st.spinner("正在生成SQL查询..."):
                    response = sql_chain.invoke({"question": user_question})
                    sql_query = response if isinstance(response, str) else str(response)
            
            # 清理SQL查询
            cleaned_sql = self.sql_processor.clean_sql_query(sql_query)
            
            if not cleaned_sql:
                return False, None, sql_query, "无法生成有效的SQL查询"
            
            # 执行SQL查询
            with st.spinner("正在执行查询..."):
                result = self.db_manager.execute_query(cleaned_sql)
                
                if result is None:
                    return False, None, cleaned_sql, "查询执行失败"
                
                return True, result, cleaned_sql, ""
                
        except Exception as e:
            error_msg = f"查询执行错误: {str(e)}"
            st.error(error_msg)
            return False, None, "", error_msg
    
    def execute_direct_sql_query(self, sql_query: str) -> Tuple[bool, Any, str, str]:
        """
        直接执行SQL查询
        
        Returns:
            Tuple[bool, Any, str, str]: (成功标志, 查询结果, 清理后的SQL, 错误信息)
        """
        try:
            # 清理SQL查询
            cleaned_sql = self.sql_processor.clean_sql_query(sql_query)
            
            if not cleaned_sql:
                return False, None, sql_query, "SQL查询为空或无效"
            
            # 执行查询
            with st.spinner("正在执行SQL查询..."):
                result = self.db_manager.execute_query(cleaned_sql)
                
                if result is None:
                    return False, None, cleaned_sql, "查询执行失败"
                
                return True, result, cleaned_sql, ""
                
        except Exception as e:
            error_msg = f"SQL查询执行错误: {str(e)}"
            st.error(error_msg)
            return False, None, sql_query, error_msg
    
    def format_and_display_result(self, result: Any, sql_query: str, display_format: str = "表格"):
        """格式化并显示查询结果"""
        try:
            if display_format == "表格":
                # 提取列名
                columns = self.sql_processor.extract_column_names(sql_query)
                
                # 格式化为DataFrame
                df = self.data_formatter.format_query_result(result, columns)
                
                # 显示DataFrame
                self.data_formatter.display_dataframe(df, "查询结果")
                
            else:  # 原始格式
                self.data_formatter.display_raw_result(result, "原始查询结果")
                
        except Exception as e:
            st.error(f"显示结果时出错: {e}")
    
    def test_connections(self) -> Tuple[bool, bool, str]:
        """
        测试数据库和LLM连接
        
        Returns:
            Tuple[bool, bool, str]: (数据库连接状态, LLM连接状态, 错误信息)
        """
        db_status = self.db_manager.test_connection()
        llm_status = self.llm_manager.test_connection()
        
        error_msg = ""
        if not db_status:
            error_msg += "数据库连接失败; "
        if not llm_status:
            error_msg += "LLM模型连接失败; "
        
        return db_status, llm_status, error_msg.rstrip("; ")
    
    def get_table_info(self) -> str:
        """获取数据库表信息"""
        try:
            return self.prompt_manager.get_table_info()
        except Exception as e:
            return f"获取表信息时出错: {e}"
    
    def add_example(self, question: str, sql: str) -> bool:
        """添加新的查询示例"""
        try:
            self.prompt_manager.add_example(question, sql)
            return True
        except Exception as e:
            st.error(f"添加示例时出错: {e}")
            return False
    
    def get_all_examples(self) -> list:
        """获取所有查询示例"""
        try:
            return self.prompt_manager.get_examples()
        except Exception as e:
            st.error(f"获取示例时出错: {e}")
            return []


# 全局查询引擎实例
query_engine = QueryEngine()