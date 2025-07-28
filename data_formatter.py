"""
数据格式化模块 - 处理查询结果的格式化和显示
"""

import pandas as pd
import streamlit as st
from typing import List, Dict, Any, Union


class DataFormatter:
    """数据格式化器"""
    
    def __init__(self):
        pass
    
    def format_query_result(self, result, columns=None):
        """格式化查询结果为DataFrame"""
        try:
            if not result:
                return pd.DataFrame()
            
            # 如果结果是字符串，尝试解析为表格数据
            if isinstance(result, str):
                return self.parse_string_result(result, columns)
            
            # 如果是单个值，包装成列表
            if not isinstance(result, (list, tuple)):
                result = [result]
            
            # 如果结果是元组列表，转换为字典列表
            if result and isinstance(result[0], (tuple, list)):
                if columns:
                    # 使用提供的列名
                    data = []
                    for row in result:
                        if len(row) == len(columns):
                            data.append(dict(zip(columns, row)))
                        else:
                            # 列数不匹配时，使用默认列名
                            row_dict = {}
                            for i, value in enumerate(row):
                                col_name = columns[i] if i < len(columns) else f"Column_{i+1}"
                                row_dict[col_name] = value
                            data.append(row_dict)
                    return pd.DataFrame(data)
                else:
                    # 没有列名时，使用默认列名
                    if result:
                        num_cols = len(result[0])
                        columns = [f"Column_{i+1}" for i in range(num_cols)]
                        data = [dict(zip(columns, row)) for row in result]
                        return pd.DataFrame(data)
            
            # 如果结果已经是字典列表
            elif result and isinstance(result[0], dict):
                return pd.DataFrame(result)
            
            # 其他情况，创建单列DataFrame
            else:
                return self.create_dataframe_from_list(result)
                
        except Exception as e:
            st.error(f"格式化查询结果时出错: {e}")
            return pd.DataFrame([{"错误": str(e)}])
    
    def parse_string_result(self, result_str, columns=None):
        """解析字符串格式的查询结果"""
        try:
            # 移除首尾空白
            result_str = result_str.strip()
            
            # 如果是空字符串或"查询结果为空"等提示
            if not result_str or "查询结果为空" in result_str or "No results" in result_str:
                return pd.DataFrame()
            
            # 检查是否是Python列表/元组的字符串表示
            if result_str.startswith('[') and result_str.endswith(']'):
                return self.parse_python_list_format(result_str, columns)
            
            # 分割行
            lines = result_str.split('\n')
            lines = [line.strip() for line in lines if line.strip()]
            
            if not lines:
                return pd.DataFrame()
            
            # 尝试解析表格格式的结果
            # 格式1: (value1, value2, value3) 每行一个元组
            if lines[0].startswith('(') and lines[0].endswith(')'):
                return self.parse_tuple_format(lines, columns)
            
            # 格式2: value1, value2, value3 每行逗号分隔
            elif ',' in lines[0]:
                return self.parse_csv_format(lines, columns)
            
            # 格式3: 表格格式 (带分隔符)
            elif '|' in result_str or '\t' in result_str:
                return self.parse_table_format(result_str, columns)
            
            # 格式4: 单列结果
            else:
                return pd.DataFrame({"结果": lines})
                
        except Exception as e:
            st.error(f"解析字符串结果时出错: {e}")
            return pd.DataFrame([{"结果": result_str}])
    
    def parse_python_list_format(self, result_str, columns=None):
        """解析Python列表格式的结果: [('val1', 'val2'), ('val3', 'val4')]"""
        try:
            import ast
            import re
            
            # 尝试使用ast.literal_eval安全解析
            try:
                # 处理Decimal对象 - 将Decimal('xxx')替换为字符串
                cleaned_str = re.sub(r"Decimal\('([^']+)'\)", r"'\1'", result_str)
                parsed_data = ast.literal_eval(cleaned_str)
            except (ValueError, SyntaxError):
                # 如果ast解析失败，尝试手动解析
                return self.manual_parse_list_format(result_str, columns)
            
            if not parsed_data:
                return pd.DataFrame()
            
            # 如果是元组列表，转换为DataFrame
            if isinstance(parsed_data, list) and parsed_data:
                if isinstance(parsed_data[0], (tuple, list)):
                    # 多行数据
                    data = []
                    for row in parsed_data:
                        # 处理每行数据，确保所有值都是字符串或数字
                        processed_row = []
                        for value in row:
                            if str(value).startswith("Decimal("):
                                # 提取Decimal中的数值
                                decimal_match = re.search(r"Decimal\('([^']+)'\)", str(value))
                                if decimal_match:
                                    processed_row.append(decimal_match.group(1))
                                else:
                                    processed_row.append(str(value))
                            else:
                                processed_row.append(value)
                        data.append(processed_row)
                    
                    # 设置列名
                    if columns and len(columns) == len(data[0]):
                        df_columns = columns
                    else:
                        df_columns = [f"Column_{i+1}" for i in range(len(data[0]))]
                    
                    return pd.DataFrame(data, columns=df_columns)
                else:
                    # 单行数据或单列数据
                    if columns:
                        return pd.DataFrame([parsed_data], columns=columns[:len(parsed_data)])
                    else:
                        return pd.DataFrame([parsed_data])
            
            # 其他情况
            return pd.DataFrame([{"结果": str(parsed_data)}])
            
        except Exception as e:
            st.error(f"解析Python列表格式时出错: {e}")
            return pd.DataFrame([{"结果": result_str}])
    
    def manual_parse_list_format(self, result_str, columns=None):
        """手动解析列表格式（当ast解析失败时使用）"""
        try:
            import re
            
            # 移除外层的方括号
            content = result_str.strip('[]')
            
            # 使用更智能的方法来分割元组，处理嵌套括号
            tuples = self._extract_tuples_with_nested_brackets(content)
            
            if not tuples:
                return pd.DataFrame([{"结果": result_str}])
            
            data = []
            for tuple_str in tuples:
                # 移除外层括号
                tuple_content = tuple_str.strip('()')
                
                # 智能分割元组内容，处理嵌套结构
                values = self._smart_split_tuple_content(tuple_content)
                
                # 处理每个值
                processed_values = []
                for value in values:
                    processed_value = self._process_value(value)
                    processed_values.append(processed_value)
                
                data.append(processed_values)
            
            if not data:
                return pd.DataFrame()
            
            # 设置列名
            if columns and len(columns) == len(data[0]):
                df_columns = columns
            else:
                df_columns = [f"Column_{i+1}" for i in range(len(data[0]))]
            
            return pd.DataFrame(data, columns=df_columns)
            
        except Exception as e:
            st.error(f"手动解析列表格式时出错: {e}")
            return pd.DataFrame([{"结果": result_str}])
    
    def _extract_tuples_with_nested_brackets(self, content):
        """提取包含嵌套括号的元组"""
        tuples = []
        i = 0
        while i < len(content):
            if content[i] == '(':
                # 找到元组的开始
                start = i
                bracket_count = 1
                i += 1
                
                # 找到匹配的结束括号
                while i < len(content) and bracket_count > 0:
                    if content[i] == '(':
                        bracket_count += 1
                    elif content[i] == ')':
                        bracket_count -= 1
                    i += 1
                
                if bracket_count == 0:
                    # 找到完整的元组
                    tuple_str = content[start:i]
                    tuples.append(tuple_str)
            else:
                i += 1
        
        return tuples
    
    def _smart_split_tuple_content(self, content):
        """智能分割元组内容，处理嵌套结构"""
        values = []
        current_value = ""
        bracket_count = 0
        quote_char = None
        i = 0
        
        while i < len(content):
            char = content[i]
            
            # 处理引号
            if char in ["'", '"'] and quote_char is None:
                quote_char = char
                current_value += char
            elif char == quote_char:
                quote_char = None
                current_value += char
            elif quote_char is not None:
                # 在引号内，直接添加字符
                current_value += char
            elif char == '(':
                # 不在引号内的左括号
                bracket_count += 1
                current_value += char
            elif char == ')':
                # 不在引号内的右括号
                bracket_count -= 1
                current_value += char
            elif char == ',' and bracket_count == 0:
                # 不在引号内且不在嵌套括号内的逗号，这是分隔符
                values.append(current_value.strip())
                current_value = ""
            else:
                current_value += char
            
            i += 1
        
        # 添加最后一个值
        if current_value.strip():
            values.append(current_value.strip())
        
        return values
    
    def _process_value(self, value):
        """处理单个值，包括Decimal和datetime对象"""
        import re
        
        value = value.strip()
        
        # 处理None
        if value == 'None':
            return None
        
        # 处理Decimal对象 - 更强的匹配模式
        if 'Decimal(' in value:
            # 匹配 Decimal('数字') 格式
            decimal_match = re.search(r"Decimal\('([^']+)'\)", value)
            if decimal_match:
                return decimal_match.group(1)
            # 匹配 Decimal("数字") 格式
            decimal_match = re.search(r'Decimal\("([^"]+)"\)', value)
            if decimal_match:
                return decimal_match.group(1)
            # 如果是不完整的Decimal字符串，尝试提取数字部分
            decimal_match = re.search(r"Decimal\('([^']*)", value)
            if decimal_match:
                return decimal_match.group(1)
        
        # 处理datetime.date对象
        if 'datetime.date(' in value:
            date_match = re.search(r"datetime\.date\((\d+),\s*(\d+),\s*(\d+)\)", value)
            if date_match:
                year, month, day = date_match.groups()
                return f"{year}-{month:0>2}-{day:0>2}"
        
        # 处理datetime.datetime对象
        if 'datetime.datetime(' in value:
            datetime_match = re.search(r"datetime\.datetime\(([^)]+)\)", value)
            if datetime_match:
                return f"datetime({datetime_match.group(1)})"
        
        # 移除外层引号
        if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
            return value[1:-1]
        
        return value
    
    def parse_tuple_format(self, lines, columns=None):
        """解析元组格式的结果: (value1, value2, value3)"""
        try:
            data = []
            for line in lines:
                # 移除括号并分割
                line = line.strip('()')
                values = [v.strip().strip("'\"") for v in line.split(',')]
                data.append(values)
            
            if not data:
                return pd.DataFrame()
            
            # 使用提供的列名或生成默认列名
            if columns and len(columns) == len(data[0]):
                df_columns = columns
            else:
                df_columns = [f"Column_{i+1}" for i in range(len(data[0]))]
            
            return pd.DataFrame(data, columns=df_columns)
            
        except Exception as e:
            st.error(f"解析元组格式时出错: {e}")
            return pd.DataFrame([{"结果": str(lines)}])
    
    def parse_csv_format(self, lines, columns=None):
        """解析CSV格式的结果: value1, value2, value3"""
        try:
            data = []
            for line in lines:
                values = [v.strip().strip("'\"") for v in line.split(',')]
                data.append(values)
            
            if not data:
                return pd.DataFrame()
            
            # 使用提供的列名或生成默认列名
            if columns and len(columns) == len(data[0]):
                df_columns = columns
            else:
                df_columns = [f"Column_{i+1}" for i in range(len(data[0]))]
            
            return pd.DataFrame(data, columns=df_columns)
            
        except Exception as e:
            st.error(f"解析CSV格式时出错: {e}")
            return pd.DataFrame([{"结果": str(lines)}])
    
    def parse_table_format(self, result_str, columns=None):
        """解析表格格式的结果"""
        try:
            # 尝试使用pandas的read_csv来解析
            from io import StringIO
            
            # 如果包含|分隔符，替换为逗号
            if '|' in result_str:
                result_str = result_str.replace('|', ',')
            
            # 尝试读取为CSV
            df = pd.read_csv(StringIO(result_str), sep=',', header=None)
            
            # 设置列名
            if columns and len(columns) == len(df.columns):
                df.columns = columns
            else:
                df.columns = [f"Column_{i+1}" for i in range(len(df.columns))]
            
            return df
            
        except Exception as e:
            st.error(f"解析表格格式时出错: {e}")
            return pd.DataFrame([{"结果": result_str}])
    
    def create_dataframe_from_list(self, data_list):
        """从列表创建DataFrame"""
        try:
            if not data_list:
                return pd.DataFrame()
            
            # 处理不同类型的数据
            processed_data = []
            for item in data_list:
                processed_item = self.process_data_item(item)
                processed_data.append(processed_item)
            
            # 如果所有项目都是字典，直接创建DataFrame
            if all(isinstance(item, dict) for item in processed_data):
                return pd.DataFrame(processed_data)
            
            # 否则创建单列DataFrame
            return pd.DataFrame({"结果": processed_data})
            
        except Exception as e:
            return pd.DataFrame([{"错误": f"创建DataFrame时出错: {e}"}])
    
    def process_data_item(self, item):
        """处理单个数据项"""
        if item is None:
            return "NULL"
        elif isinstance(item, (int, float, str, bool)):
            return item
        elif isinstance(item, (list, tuple)):
            # 如果是列表或元组，转换为字符串表示
            return str(item)
        elif isinstance(item, dict):
            return item
        else:
            # 其他类型转换为字符串
            return str(item)
    
    def format_raw_result(self, result):
        """格式化原始结果为可读字符串"""
        try:
            if result is None:
                return "查询结果为空"
            
            if isinstance(result, str):
                return result
            
            if isinstance(result, (list, tuple)):
                if not result:
                    return "查询结果为空"
                
                # 如果是简单的值列表
                if all(isinstance(item, (str, int, float, bool, type(None))) for item in result):
                    return "\n".join(str(item) for item in result)
                
                # 如果是复杂结构
                formatted_lines = []
                for i, item in enumerate(result):
                    if isinstance(item, (tuple, list)):
                        formatted_lines.append(f"行 {i+1}: {', '.join(str(x) for x in item)}")
                    elif isinstance(item, dict):
                        formatted_lines.append(f"行 {i+1}: {item}")
                    else:
                        formatted_lines.append(f"行 {i+1}: {item}")
                
                return "\n".join(formatted_lines)
            
            if isinstance(result, dict):
                return "\n".join(f"{k}: {v}" for k, v in result.items())
            
            return str(result)
            
        except Exception as e:
            return f"格式化结果时出错: {e}"
    
    def display_dataframe(self, df: pd.DataFrame, title: str = "查询结果"):
        """在Streamlit中显示DataFrame"""
        if df.empty:
            st.info("查询结果为空")
            return
        
        st.subheader(title)
        
        
        # 显示数据统计
        col1, col2 = st.columns(2)
        with col1:
            st.metric("总行数", len(df))
        with col2:
            st.metric("总列数", len(df.columns))
        
        # 显示数据表
        st.dataframe(df, use_container_width=True)
        
        # 提供下载选项
        if not df.empty:
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="下载CSV文件",
                data=csv,
                file_name=f"{title}.csv",
                mime="text/csv"
            )
    
    def display_raw_result(self, result, title: str = "原始查询结果"):
        """显示原始查询结果"""
        st.subheader(title)
        formatted_result = self.format_raw_result(result)
        st.text_area("结果", formatted_result, height=200)


# 全局数据格式化器实例
data_formatter = DataFormatter()