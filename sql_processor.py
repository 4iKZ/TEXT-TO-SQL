"""
SQL处理模块 - 处理SQL查询清理和解析
"""

import re
from config import TABLE_COLUMNS


class SQLProcessor:
    """SQL查询处理器"""
    
    def __init__(self):
        pass
    
    def clean_sql_query(self, sql_query):
        """清理SQL查询，移除不必要的前缀和格式化问题"""
        if not isinstance(sql_query, str):
            return str(sql_query)
        
        # 原始查询备份
        original_query = sql_query
        sql_query = sql_query.strip()
        
        # 如果查询为空，返回空字符串
        if not sql_query:
            return ""
        
        # 1. 首先尝试提取代码块中的SQL
        code_block_patterns = [
            r'```sql\s*(.*?)\s*```',  # ```sql ... ```
            r'```mysql\s*(.*?)\s*```',  # ```mysql ... ```
            r'```\s*(SELECT.*?)\s*```',  # ``` SELECT ... ```
            r'```\s*(INSERT.*?)\s*```',  # ``` INSERT ... ```
            r'```\s*(UPDATE.*?)\s*```',  # ``` UPDATE ... ```
            r'```\s*(DELETE.*?)\s*```',  # ``` DELETE ... ```
        ]
        
        for pattern in code_block_patterns:
            match = re.search(pattern, sql_query, re.DOTALL | re.IGNORECASE)
            if match:
                sql_query = match.group(1).strip()
                break
        
        # 2. 移除常见的前缀标识符
        prefixes_to_remove = [
            'sql查询:', 'sql:', 'SQL:', 'SQL查询:', 'mysql:', 'MySQL:', 
            'sql', 'SQL', 'mysql', 'MySQL', '查询:', '查询：',
            'sql语句:', 'SQL语句:', 'sql语句：', 'SQL语句：'
        ]
        
        for prefix in prefixes_to_remove:
            if sql_query.lower().startswith(prefix.lower()):
                sql_query = sql_query[len(prefix):].strip()
                break
        
        # 3. 移除结尾的标记
        suffixes_to_remove = ['```', '`', ';', '；']
        for suffix in suffixes_to_remove:
            while sql_query.endswith(suffix):
                sql_query = sql_query[:-len(suffix)].strip()
        
        # 4. 处理多行文本，提取SQL语句
        lines = sql_query.split('\n')
        sql_lines = []
        found_sql_start = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 检查是否是SQL语句的开始
            if not found_sql_start:
                if re.match(r'^\s*(SELECT|INSERT|UPDATE|DELETE|WITH|CREATE|DROP|ALTER|SHOW|DESCRIBE|EXPLAIN)\s+', line, re.IGNORECASE):
                    found_sql_start = True
                    sql_lines.append(line)
                elif any(keyword in line.upper() for keyword in ['SELECT', 'FROM', 'WHERE', 'ORDER BY', 'GROUP BY', 'HAVING', 'LIMIT']):
                    # 如果包含SQL关键字，也认为是SQL语句
                    found_sql_start = True
                    sql_lines.append(line)
            else:
                # 已经找到SQL开始，继续添加行直到遇到明显的结束标记
                if line.startswith('#') or line.startswith('--') or line.startswith('/*'):
                    # 跳过注释行
                    continue
                elif line.lower() in ['end', 'go', 'commit', 'rollback']:
                    # SQL结束标记
                    break
                elif any(phrase in line.lower() for phrase in ['以上就是', '这就是', '查询语句', '语句结束', '结束查询', '查询完成']):
                    # 检测到SQL语句结束的描述性文本
                    break
                else:
                    sql_lines.append(line)
        
        # 如果找到了SQL行，使用它们
        if sql_lines:
            sql_query = ' '.join(sql_lines)
        
        # 5. 使用正则表达式直接提取SQL语句
        if not sql_lines:
            sql_patterns = [
                r'(SELECT\s+.*?(?:;|$))',
                r'(INSERT\s+.*?(?:;|$))',
                r'(UPDATE\s+.*?(?:;|$))',
                r'(DELETE\s+.*?(?:;|$))',
                r'(WITH\s+.*?(?:;|$))',
                r'(CREATE\s+.*?(?:;|$))',
                r'(DROP\s+.*?(?:;|$))',
                r'(ALTER\s+.*?(?:;|$))',
            ]
            
            for pattern in sql_patterns:
                match = re.search(pattern, sql_query, re.DOTALL | re.IGNORECASE)
                if match:
                    sql_query = match.group(1).strip()
                    break
        
        # 6. 清理和标准化
        # 替换特殊字符
        sql_query = sql_query.replace('≥', '>=').replace('≤', '<=').replace('≠', '!=')
        
        # 移除SQL语句后面的描述性文本
        # 查找常见的结束短语并截断
        end_phrases = [
            '以上就是', '这就是', '查询语句', '语句结束', '结束查询', '查询完成',
            '这是查询', '就是这个', '完成了', '结束了', '。', '；'
        ]
        
        for phrase in end_phrases:
            if phrase in sql_query:
                # 找到短语的位置
                pos = sql_query.find(phrase)
                # 检查这个位置之前是否有完整的SQL语句
                before_phrase = sql_query[:pos].strip()
                if before_phrase and any(before_phrase.upper().startswith(kw) for kw in ['SELECT', 'INSERT', 'UPDATE', 'DELETE']):
                    # 如果前面有完整的SQL语句，截断到这个位置
                    sql_query = before_phrase
                    break
        
        # 移除多余的空白字符，但保持基本的SQL格式
        sql_query = re.sub(r'\s+', ' ', sql_query).strip()
        
        # 移除结尾的分号（如果存在）
        if sql_query.endswith(';'):
            sql_query = sql_query[:-1].strip()
        
        # 7. 最终验证 - 确保是有效的SQL语句
        sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'WITH', 'CREATE', 'DROP', 'ALTER', 'SHOW', 'DESCRIBE', 'EXPLAIN']
        
        if not any(sql_query.upper().startswith(keyword) for keyword in sql_keywords):
            # 如果不是以SQL关键字开始，尝试在字符串中查找
            for keyword in sql_keywords:
                pos = sql_query.upper().find(keyword)
                if pos >= 0:
                    sql_query = sql_query[pos:].strip()
                    break
        
        # 8. 如果仍然没有找到有效的SQL，返回清理后的原始查询
        if not any(sql_query.upper().startswith(keyword) for keyword in sql_keywords):
            # 最后的尝试：查找包含FROM的语句
            if 'FROM' in sql_query.upper():
                from_pos = sql_query.upper().find('FROM')
                # 向前查找SELECT
                before_from = sql_query[:from_pos]
                select_pos = before_from.upper().rfind('SELECT')
                if select_pos >= 0:
                    sql_query = sql_query[select_pos:].strip()
        
        return sql_query
    
    def extract_column_names(self, sql_query):
        """从SQL查询中提取列名"""
        try:
            # 简单的列名提取逻辑
            sql_upper = sql_query.upper()
            select_pos = sql_upper.find('SELECT')
            from_pos = sql_upper.find('FROM')
            
            if select_pos != -1 and from_pos != -1:
                select_part = sql_query[select_pos + 6:from_pos].strip()
                
                # 处理SELECT *的情况
                if select_part.strip() == '*':
                    # 根据FROM子句中的表名返回对应的列名
                    from_part = sql_query[from_pos + 4:].strip()
                    table_name = self._extract_table_name(from_part)
                    return self._get_table_columns(table_name)
                
                # 分割列名
                columns = []
                # 更智能的分割，考虑函数调用中的逗号
                parts = self._split_select_columns(select_part)
                
                for col in parts:
                    col = col.strip()
                    if not col:
                        continue
                        
                    # 处理AS别名
                    if ' AS ' in col.upper():
                        alias = col.upper().split(' AS ')[-1].strip()
                        columns.append(alias.title())
                    elif ' as ' in col:
                        alias = col.split(' as ')[-1].strip()
                        columns.append(alias.title())
                    else:
                        # 提取列名（去掉表前缀）
                        if '.' in col:
                            col_name = col.split('.')[-1].strip('`')
                        else:
                            col_name = col.strip('`')
                        columns.append(col_name.title())
                
                return columns
        except Exception as e:
            print(f"提取列名错误: {e}")
            return []
    
    def _extract_table_name(self, from_part):
        """从FROM子句中提取表名"""
        try:
            # 移除WHERE、ORDER BY等子句
            keywords = ['WHERE', 'ORDER BY', 'GROUP BY', 'HAVING', 'LIMIT', 'JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN']
            from_clean = from_part
            
            # 按关键字长度排序，优先匹配较长的关键字（如ORDER BY而不是ORDER）
            keywords.sort(key=len, reverse=True)
            
            for keyword in keywords:
                # 使用正则表达式确保匹配完整的关键字（前后有空格或字符串边界）
                import re
                pattern = r'\b' + re.escape(keyword) + r'\b'
                match = re.search(pattern, from_clean, re.IGNORECASE)
                if match:
                    from_clean = from_clean[:match.start()]
                    break
            
            # 提取表名（可能包含别名）
            # 先去除前后空格，然后按空格分割取第一个部分
            table_part = from_clean.strip()
            if ' ' in table_part:
                # 如果有空格，取第一个单词作为表名
                table_part = table_part.split()[0]
            
            # 移除可能的反引号和其他字符
            table_name = table_part.strip('`').strip('"').strip("'").strip()
            
            return table_name
        except Exception as e:
            return ""
    
    def _get_table_columns(self, table_name):
        """根据表名返回对应的列名"""
        # 不区分大小写的表名匹配
        for table, columns in TABLE_COLUMNS.items():
            if table.lower() == table_name.lower():
                return columns
        
        return []
    
    def _split_select_columns(self, select_part):
        """智能分割SELECT部分的列名，考虑函数调用中的逗号"""
        columns = []
        current_col = ""
        paren_count = 0
        in_quotes = False
        
        for char in select_part:
            if char == "'" and not in_quotes:
                in_quotes = True
            elif char == "'" and in_quotes:
                in_quotes = False
            elif not in_quotes and char == '(':
                paren_count += 1
            elif not in_quotes and char == ')':
                paren_count -= 1
            elif char == ',' and paren_count == 0 and not in_quotes:
                # 这是一个真正的列分隔符
                if current_col.strip():
                    columns.append(current_col.strip())
                current_col = ""
                continue
            
            current_col += char
        
        # 添加最后一列
        if current_col.strip():
            columns.append(current_col.strip())
        
        return columns


# 全局SQL处理器实例
sql_processor = SQLProcessor()