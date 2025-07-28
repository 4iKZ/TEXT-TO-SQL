"""
Schema转换器 - 将config.py中的表结构转换为SQLCoder格式
"""

from config import TABLE_COLUMNS, TABLE_INFO


class SchemaConverter:
    """将现有配置转换为SQLCoder格式的schema"""
    
    @staticmethod
    def convert_table_columns_to_schema():
        """
        将TABLE_COLUMNS转换为SQLCoder格式的schema
        
        Returns:
            dict: SQLCoder格式的schema字典
        """
        schema = {}
        
        # 定义常见的数据类型映射
        type_mapping = {
            'ID': 'INT',
            'CustomerID': 'INT',
            'EmployeeID': 'INT', 
            'ProductID': 'INT',
            'SalesOrderID': 'INT',
            'LineItemID': 'INT',
            'LogID': 'INT',
            'SupplierID': 'INT',
            'FirstName': 'VARCHAR(100)',
            'LastName': 'VARCHAR(100)',
            'CustomerName': 'VARCHAR(100)',
            'ProductName': 'VARCHAR(255)',
            'CompanyName': 'VARCHAR(255)',
            'ContactName': 'VARCHAR(100)',
            'ContactTitle': 'VARCHAR(50)',
            'Email': 'VARCHAR(255)',
            'Phone': 'VARCHAR(20)',
            'Position': 'VARCHAR(100)',
            'Status': 'VARCHAR(50)',
            'PaymentMethod': 'VARCHAR(50)',
            'Description': 'TEXT',
            'Comments': 'TEXT',
            'Notes': 'TEXT',
            'Address': 'TEXT',
            'BillingAddress': 'TEXT',
            'ShippingAddress': 'TEXT',
            'OrderDate': 'DATE',
            'RequiredDate': 'DATE',
            'ShippedDate': 'DATE',
            'HireDate': 'DATE',
            'CustomerSince': 'DATE',
            'ChangeDate': 'DATE',
            'UnitPrice': 'DECIMAL(10,2)',
            'Salary': 'DECIMAL(10,2)',
            'Discount': 'DECIMAL(5,2)',
            'TotalPrice': 'DECIMAL(10,2)',
            'Quantity': 'INT',
            'StockQuantity': 'INT',
            'ReorderLevel': 'INT',
            'QuantityChange': 'INT',
            'IsActive': 'TINYINT',
            'IsPaid': 'TINYINT',
            'Discontinued': 'TINYINT'
        }
        
        # 定义列描述
        column_descriptions = {
            'CustomerID': 'Unique identifier for each customer',
            'EmployeeID': 'Unique identifier for each employee',
            'ProductID': 'Unique identifier for each product',
            'SalesOrderID': 'Unique identifier for each sales order',
            'LineItemID': 'Unique identifier for each line item',
            'LogID': 'Unique identifier for each inventory log entry',
            'SupplierID': 'Unique identifier for each supplier',
            'FirstName': 'First name of the person',
            'LastName': 'Last name of the person',
            'CustomerName': 'Full name of the customer',
            'ProductName': 'Name of the product',
            'CompanyName': 'Name of the company',
            'ContactName': 'Name of the contact person',
            'ContactTitle': 'Title of the contact person',
            'Email': 'Email address',
            'Phone': 'Phone number',
            'Position': 'Job position',
            'Status': 'Current status',
            'PaymentMethod': 'Method of payment',
            'Description': 'Detailed description',
            'Comments': 'Additional comments',
            'Notes': 'Additional notes',
            'Address': 'Physical address',
            'BillingAddress': 'Billing address',
            'ShippingAddress': 'Shipping address',
            'OrderDate': 'Date when the order was placed',
            'RequiredDate': 'Date when the order is required',
            'ShippedDate': 'Date when the order was shipped',
            'HireDate': 'Date when the employee was hired',
            'CustomerSince': 'Date when the customer was registered',
            'ChangeDate': 'Date when the change occurred',
            'UnitPrice': 'Price per unit',
            'Salary': 'Employee salary',
            'Discount': 'Discount amount or percentage',
            'TotalPrice': 'Total price amount',
            'Quantity': 'Quantity amount',
            'StockQuantity': 'Current stock quantity',
            'ReorderLevel': 'Minimum stock level for reordering',
            'QuantityChange': 'Change in quantity',
            'IsActive': 'Whether the record is active (1=Yes, 0=No)',
            'IsPaid': 'Whether the payment is completed (1=Yes, 0=No)',
            'Discontinued': 'Whether the product is discontinued (1=Yes, 0=No)'
        }
        
        # 定义主键
        primary_keys = {
            'Customer': 'CustomerID',
            'Employee': 'EmployeeID',
            'Product': 'ProductID',
            'SalesOrder': 'SalesOrderID',
            'LineItem': 'LineItemID',
            'InventoryLog': 'LogID',
            'Supplier': 'SupplierID'
        }
        
        # 定义外键关系
        relationships = {
            'SalesOrder': [
                {'foreign_key': 'CustomerID', 'references_table': 'Customer', 'references_column': 'CustomerID'}
            ],
            'LineItem': [
                {'foreign_key': 'SalesOrderID', 'references_table': 'SalesOrder', 'references_column': 'SalesOrderID'},
                {'foreign_key': 'ProductID', 'references_table': 'Product', 'references_column': 'ProductID'}
            ],
            'InventoryLog': [
                {'foreign_key': 'ProductID', 'references_table': 'Product', 'references_column': 'ProductID'}
            ]
        }
        
        # 转换每个表
        for table_name, columns in TABLE_COLUMNS.items():
            schema[table_name] = {
                'columns': {},
                'relationships': relationships.get(table_name, [])
            }
            
            for column_name in columns:
                # 确定数据类型
                col_type = type_mapping.get(column_name, 'VARCHAR(255)')
                
                # 确定是否为主键
                is_primary = column_name == primary_keys.get(table_name, '')
                
                # 获取描述
                description = column_descriptions.get(column_name, f'{column_name} column')
                
                schema[table_name]['columns'][column_name] = {
                    'type': col_type,
                    'primary_key': is_primary,
                    'description': description
                }
        
        return schema
    
    @staticmethod
    def get_sqlcoder_schema():
        """获取完整的SQLCoder格式schema"""
        return SchemaConverter.convert_table_columns_to_schema()


# 使用示例
if __name__ == "__main__":
    converter = SchemaConverter()
    schema = converter.get_sqlcoder_schema()
    
    print("=== SQLCoder Schema 示例 ===")
    for table_name, table_info in schema.items():
        print(f"\n表名: {table_name}")
        print(f"列数: {len(table_info['columns'])}")
        print(f"关系数: {len(table_info['relationships'])}")
        
        # 显示前3个列作为示例
        for i, (col_name, col_info) in enumerate(table_info['columns'].items()):
            if i < 3:
                print(f"  - {col_name}: {col_info['type']} ({'主键' if col_info['primary_key'] else '普通列'})")
            elif i == 3:
                print(f"  ... 还有 {len(table_info['columns']) - 3} 个列")
                break