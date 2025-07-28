"""
SQL后处理器 - 修正SQL查询中的表名和列名大小写
"""

import re
import sys
import os
from typing import Dict, List, Optional

# 添加父目录到路径以便导入config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TABLE_COLUMNS


class SQLPostProcessor:
    """SQL查询后处理器，用于修正表名和列名的大小写"""
    
    def __init__(self):
        # 从配置中获取正确的表名和列名
        self.correct_table_names = list(TABLE_COLUMNS.keys())
        self.table_columns_map = TABLE_COLUMNS
        
        # 创建大小写不敏感的映射
        self.table_name_mapping = {}
        self.column_name_mapping = {}
        
        # 建立表名映射（小写 -> 正确大小写）
        for table_name in self.correct_table_names:
            self.table_name_mapping[table_name.lower()] = table_name
        
        # 建立列名映射（小写 -> 正确大小写）
        for table_name, columns in self.table_columns_map.items():
            for column_name in columns:
                key = f"{table_name.lower()}.{column_name.lower()}"
                value = f"{table_name}.{column_name}"
                self.column_name_mapping[key] = value
                
                # 也添加不带表名的列名映射
                self.column_name_mapping[column_name.lower()] = column_name
    
    def fix_table_names(self, sql_query: str) -> str:
        """
        修正SQL查询中的表名大小写
        
        Args:
            sql_query: 原始SQL查询
            
        Returns:
            修正后的SQL查询
        """
        if not sql_query:
            return sql_query
        
        fixed_sql = sql_query
        
        # 使用正则表达式查找和替换表名
        for incorrect_name, correct_name in self.table_name_mapping.items():
            if incorrect_name != correct_name.lower():
                continue
                
            # 匹配表名的各种情况
            patterns = [
                # FROM table_name
                rf'\bFROM\s+{re.escape(incorrect_name)}\b',
                # JOIN table_name
                rf'\bJOIN\s+{re.escape(incorrect_name)}\b',
                # UPDATE table_name
                rf'\bUPDATE\s+{re.escape(incorrect_name)}\b',
                # INSERT INTO table_name
                rf'\bINTO\s+{re.escape(incorrect_name)}\b',
                # DELETE FROM table_name
                rf'\bFROM\s+{re.escape(incorrect_name)}\b',
                # table_name.column_name
                rf'\b{re.escape(incorrect_name)}\.(\w+)',
            ]
            
            for pattern in patterns:
                if '\\.' in pattern:  # 处理 table.column 的情况
                    def replace_table_column(match):
                        column_part = match.group(1)
                        return f"{correct_name}.{column_part}"
                    fixed_sql = re.sub(pattern, replace_table_column, fixed_sql, flags=re.IGNORECASE)
                else:
                    fixed_sql = re.sub(pattern, lambda m: m.group().replace(incorrect_name, correct_name), 
                                     fixed_sql, flags=re.IGNORECASE)
        
        return fixed_sql
    
    def fix_column_names(self, sql_query: str) -> str:
        """
        修正SQL查询中的列名大小写
        
        Args:
            sql_query: 原始SQL查询
            
        Returns:
            修正后的SQL查询
        """
        if not sql_query:
            return sql_query
        
        fixed_sql = sql_query
        
        # 修正列名（包括带表名前缀的）
        for table_name, columns in self.table_columns_map.items():
            for column_name in columns:
                incorrect_column = column_name.lower()
                if incorrect_column != column_name:
                    # 修正 table.column 格式
                    pattern = rf'\b{re.escape(table_name)}\.{re.escape(incorrect_column)}\b'
                    replacement = f"{table_name}.{column_name}"
                    fixed_sql = re.sub(pattern, replacement, fixed_sql, flags=re.IGNORECASE)
                    
                    # 修正单独的列名（在SELECT, WHERE, ORDER BY等子句中）
                    # 但要小心不要替换关键字
                    if not self._is_sql_keyword(incorrect_column):
                        pattern = rf'\b{re.escape(incorrect_column)}\b'
                        # 只在特定上下文中替换
                        contexts = [
                            rf'SELECT\s+.*?\b{re.escape(incorrect_column)}\b',
                            rf'WHERE\s+.*?\b{re.escape(incorrect_column)}\b',
                            rf'ORDER\s+BY\s+.*?\b{re.escape(incorrect_column)}\b',
                            rf'GROUP\s+BY\s+.*?\b{re.escape(incorrect_column)}\b',
                        ]
                        
                        for context_pattern in contexts:
                            if re.search(context_pattern, fixed_sql, flags=re.IGNORECASE):
                                fixed_sql = re.sub(pattern, column_name, fixed_sql, flags=re.IGNORECASE)
        
        return fixed_sql
    
    def _is_sql_keyword(self, word: str) -> bool:
        """检查是否为SQL关键字"""
        sql_keywords = {
            'select', 'from', 'where', 'join', 'inner', 'left', 'right', 'outer',
            'on', 'and', 'or', 'not', 'in', 'like', 'between', 'is', 'null',
            'order', 'by', 'group', 'having', 'limit', 'offset', 'union',
            'insert', 'into', 'values', 'update', 'set', 'delete', 'create',
            'table', 'index', 'view', 'database', 'schema', 'primary', 'key',
            'foreign', 'references', 'constraint', 'unique', 'check', 'default',
            'auto_increment', 'varchar', 'int', 'date', 'datetime', 'text',
            'decimal', 'float', 'double', 'boolean', 'tinyint', 'bigint'
        }
        return word.lower() in sql_keywords
    
    def process_sql(self, sql_query: str) -> str:
        """
        完整处理SQL查询，修正表名和列名大小写
        
        Args:
            sql_query: 原始SQL查询
            
        Returns:
            修正后的SQL查询
        """
        if not sql_query:
            return sql_query
        
        # 先修正表名，再修正列名
        fixed_sql = self.fix_table_names(sql_query)
        fixed_sql = self.fix_column_names(fixed_sql)
        
        return fixed_sql
    
    def get_correction_report(self, original_sql: str, fixed_sql: str) -> Dict[str, List[str]]:
        """
        生成修正报告，显示所做的更改
        
        Args:
            original_sql: 原始SQL
            fixed_sql: 修正后的SQL
            
        Returns:
            修正报告字典
        """
        report = {
            "table_corrections": [],
            "column_corrections": [],
            "no_changes": original_sql == fixed_sql
        }
        
        if report["no_changes"]:
            return report
        
        # 检查表名修正
        for incorrect_name, correct_name in self.table_name_mapping.items():
            if incorrect_name in original_sql.lower() and correct_name in fixed_sql:
                report["table_corrections"].append(f"{incorrect_name} -> {correct_name}")
        
        # 检查列名修正（简化版）
        for table_name, columns in self.table_columns_map.items():
            for column_name in columns:
                incorrect_column = column_name.lower()
                if (incorrect_column in original_sql.lower() and 
                    column_name in fixed_sql and 
                    incorrect_column != column_name):
                    report["column_corrections"].append(f"{incorrect_column} -> {column_name}")
        
        return report


# 使用示例和测试
if __name__ == "__main__":
    processor = SQLPostProcessor()
    
    # 测试用例
    test_cases = [
        "SELECT customer.customerid, customer.firstname, customer.lastname FROM customer;",
        "SELECT c.customerid, c.email FROM customer c WHERE c.isactive = 1;",
        "SELECT so.salesorderid, c.customername FROM salesorder so JOIN customer c ON so.customerid = c.customerid;",
        "UPDATE customer SET email = 'new@email.com' WHERE customerid = 1;",
        "INSERT INTO customer (firstname, lastname, email) VALUES ('John', 'Doe', 'john@example.com');"
    ]
    
    print("=== SQL后处理器测试 ===")
    
    for i, test_sql in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}:")
        print(f"原始SQL: {test_sql}")
        
        fixed_sql = processor.process_sql(test_sql)
        print(f"修正SQL: {fixed_sql}")
        
        report = processor.get_correction_report(test_sql, fixed_sql)
        if not report["no_changes"]:
            print("修正内容:")
            for correction in report["table_corrections"]:
                print(f"  表名: {correction}")
            for correction in report["column_corrections"]:
                print(f"  列名: {correction}")
        else:
            print("无需修正")