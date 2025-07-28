"""
配置模块 - 存储所有应用配置信息
"""

# Ollama配置 - 请根据您的虚拟机IP地址修改
OLLAMA_BASE_URL = "http://localhost:11434"  # 如果在虚拟机上运行，请修改为虚拟机IP
OLLAMA_MODEL = "sqlcoder:15b"  # 默认使用SQL专用模型

# Ollama配置字典
OLLAMA_CONFIG = {
    "base_url": OLLAMA_BASE_URL,
    "model": OLLAMA_MODEL
}

# 可用模型列表 - 基于您虚拟机上的实际模型
AVAILABLE_MODELS = [
    # SQL专用模型（推荐用于SQL查询）
    "sqlcoder:15b",                              # 15B参数的SQL专用模型
    "sqlcoder:latest",                           # 最新版本的SQLCoder
    "sqlcoder:7b",                               # 7B参数的SQLCoder
    "mannix/defog-llama3-sqlcoder-8b:latest",    # 基于Llama3的SQL编码器
    "duckdb-nsql:7b",                            # DuckDB自然语言到SQL模型
    
    # 通用大语言模型
    "deepseek-r1:14b",                           # DeepSeek推理模型14B
    "deepseek-r1:7b",                            # DeepSeek推理模型7B
    "QwQ:latest",                                # QwQ最新版本
    "QwQ:32b",                                   # QwQ 32B参数版本
    
    # Qwen系列模型
    "qwen2.5:72b-instruct-q8_0",                # Qwen2.5 72B指令模型
    "qwen2.5:72b-instruct-q4_K_M",              # Qwen2.5 72B指令模型（量化版）
    "qwen2.5:32b-instruct-fp16",                # Qwen2.5 32B指令模型
    "qwen2.5:32b-instruct-q8_0",                # Qwen2.5 32B指令模型（量化版）
    "qwen2.5:32b-instruct-q4_k_M",              # Qwen2.5 32B指令模型（量化版）
    "qwen2.5:14b-instruct-fp16",                # Qwen2.5 14B指令模型
    "qwen2.5:14b-instruct-q8_0",                # Qwen2.5 14B指令模型（量化版）
    "qwen2.5:14b-instruct-q4_K_M",              # Qwen2.5 14B指令模型（量化版）
    "qwen2.5:7b-instruct-fp16",                 # Qwen2.5 7B指令模型
    "qwen2.5:7b-instruct-q8_0",                 # Qwen2.5 7B指令模型（量化版）
    "qwen2.5:7b-instruct-q4_K_M",               # Qwen2.5 7B指令模型（量化版）
    "qwen2.5:7b",                               # Qwen2.5 7B基础模型
    "qwen2.5:1.5b-instruct-q8_0",               # Qwen2.5 1.5B指令模型（量化版）
    "qwen2.5:1.5b-instruct-q4_K_M",             # Qwen2.5 1.5B指令模型（量化版）
    "qwen2.5:1.5b-instruct-fp16",               # Qwen2.5 1.5B指令模型
    "qwen2.5:0.5b-instruct-q4_K_M",             # Qwen2.5 0.5B指令模型（量化版）
    "qwen2.5:0.5b-instruct-q8_0",               # Qwen2.5 0.5B指令模型（量化版）
    
    # 嵌入模型
    "nomic-embed-text:latest"                    # 文本嵌入模型
]

# 模型分类和推荐
MODEL_CATEGORIES = {
    "sql_specialized": [
        "sqlcoder:15b",
        "sqlcoder:latest", 
        "sqlcoder:7b",
        "mannix/defog-llama3-sqlcoder-8b:latest",
        "duckdb-nsql:7b"
    ],
    "general_large": [
        "qwen2.5:72b-instruct-q8_0",
        "qwen2.5:32b-instruct-q8_0",
        "QwQ:latest",
        "QwQ:32b"
    ],
    "general_medium": [
        "deepseek-r1:14b",
        "qwen2.5:14b-instruct-q8_0",
        "qwen2.5:7b-instruct-q8_0"
    ],
    "general_small": [
        "deepseek-r1:7b",
        "qwen2.5:1.5b-instruct-q8_0",
        "qwen2.5:0.5b-instruct-q8_0"
    ]
}

# 推荐的SQL查询模型（按优先级排序）
RECOMMENDED_SQL_MODELS = [
    "sqlcoder:15b",                              # 最佳SQL专用模型
    "mannix/defog-llama3-sqlcoder-8b:latest",    # 基于Llama3的SQL模型
    "sqlcoder:7b",                               # 较小的SQL专用模型
    "duckdb-nsql:7b",                            # DuckDB专用模型
    "qwen2.5:14b-instruct-q8_0"                  # 通用模型备选
]

# 数据库连接配置
DATABASE_CONFIG = {
    "host": "localhost",
    "user": "root",  # 使用专门的应用用户
    "password": "MySecure123!",  # 使用安全密码
    "database": "SalesOrderSchema"
}

# 数据库URI - 用于SQLDatabase连接
DATABASE_URI = f"mysql+mysqlconnector://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}/{DATABASE_CONFIG['database']}"

# 数据库表信息
TABLE_INFO = """
- Customer(CustomerID INT, FirstName VARCHAR(100), LastName VARCHAR(100), Email VARCHAR(255), Phone VARCHAR(20), BillingAddress TEXT, ShippingAddress TEXT, CustomerSince DATE, IsActive TINYINT)
- Employee(EmployeeID INT, FirstName VARCHAR(100), LastName VARCHAR(100), Email VARCHAR(255), Phone VARCHAR(20), HireDate DATE, Position VARCHAR(100), Salary DECIMAL)
- InventoryLog(LogID INT, ProductID INT, ChangeDate DATE, QuantityChange INT, Notes TEXT)
- LineItem(LineItemID INT, SalesOrderID INT, ProductID INT, Quantity INT, UnitPrice DECIMAL, Discount DECIMAL, TotalPrice DECIMAL)
- Product(ProductID INT, ProductName VARCHAR(255), Description TEXT, UnitPrice DECIMAL, StockQuantity INT, ReorderLevel INT, Discontinued TINYINT)
- SalesOrder(SalesOrderID INT, CustomerID INT, OrderDate DATE, RequiredDate DATE, ShippedDate DATE, Status VARCHAR(50), Comments TEXT, PaymentMethod VARCHAR(50), IsPaid TINYINT)
- Supplier(SupplierID INT, CompanyName VARCHAR(255), ContactName VARCHAR(100), ContactTitle VARCHAR(50), Address TEXT, Phone VARCHAR(20), Email VARCHAR(255))
"""

# 表结构映射 - 用于列名提取
TABLE_COLUMNS = {
    'Customer': ['CustomerID', 'FirstName', 'LastName', 'Email', 'Phone', 'BillingAddress', 'ShippingAddress', 'CustomerSince', 'IsActive'],
    'Employee': ['EmployeeID', 'FirstName', 'LastName', 'Email', 'Phone', 'HireDate', 'Position', 'Salary'],
    'Product': ['ProductID', 'ProductName', 'Description', 'UnitPrice', 'StockQuantity', 'ReorderLevel', 'Discontinued'],
    'SalesOrder': ['SalesOrderID', 'CustomerID', 'OrderDate', 'RequiredDate', 'ShippedDate', 'Status', 'Comments', 'PaymentMethod', 'IsPaid'],
    'LineItem': ['LineItemID', 'SalesOrderID', 'ProductID', 'Quantity', 'UnitPrice', 'Discount', 'TotalPrice'],
    'InventoryLog': ['LogID', 'ProductID', 'ChangeDate', 'QuantityChange', 'Notes'],
    'Supplier': ['SupplierID', 'CompanyName', 'ContactName', 'ContactTitle', 'Address', 'Phone', 'Email']
}

# 应用配置
APP_CONFIG = {
    "title": "🤖智能SQL查询助手🤖",
    "description": "基于本地Ollama模型的数据库查询系统，使用提示工程优化查询准确性",
    "max_iterations": 3,
    "max_execution_time": 30,
    "default_limit": 10
}

# 少样本学习示例
FEW_SHOT_EXAMPLES = [
    {
        "input": "查询所有客户的姓名和邮箱",
        "query": "SELECT FirstName, LastName, Email FROM Customer;"
    },
    {
        "input": "显示前10个订单的详细信息",
        "query": "SELECT * FROM SalesOrder LIMIT 10;"
    },
    {
        "input": "查找价格超过100的产品",
        "query": "SELECT ProductName, UnitPrice FROM Product WHERE UnitPrice > 100;"
    },
    {
        "input": "统计每个客户的订单数量",
        "query": "SELECT c.FirstName, c.LastName, COUNT(s.SalesOrderID) as OrderCount FROM Customer c LEFT JOIN SalesOrder s ON c.CustomerID = s.CustomerID GROUP BY c.CustomerID, c.FirstName, c.LastName;"
    },
    {
        "input": "查询2024年的所有订单",
        "query": "SELECT * FROM SalesOrder WHERE YEAR(OrderDate) = 2024;"
    },
    {
        "input": "显示库存不足的产品（库存量小于重订水平）",
        "query": "SELECT ProductName, StockQuantity, ReorderLevel FROM Product WHERE StockQuantity < ReorderLevel;"
    },
    {
        "input": "查询每个产品的总销售额",
        "query": "SELECT p.ProductName, SUM(li.TotalPrice) as TotalSales FROM Product p JOIN LineItem li ON p.ProductID = li.ProductID GROUP BY p.ProductID, p.ProductName ORDER BY TotalSales DESC;"
    },
    {
        "input": "查找最近30天的订单",
        "query": "SELECT * FROM SalesOrder WHERE OrderDate >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);"
    }
]