# 🤖 SQL智能助手 (SQL Assistant)

一个基于本地Ollama模型的智能SQL查询生成系统，支持自然语言转SQL查询，具备完整的数据库Schema可视化和多模型支持功能。

## 📋 项目概述

SQL智能助手是一个现代化的数据库查询工具，它结合了大语言模型(LLM)的自然语言理解能力和专业的SQL生成技术。用户可以通过自然语言描述查询需求，系统会自动生成相应的SQL语句并执行查询。

### 🌟 核心特性

- **🧠 智能SQL生成**: 支持自然语言到SQL的智能转换
- **🎯 多模型支持**: 兼容SQL专用模型(SQLCoder)和通用大语言模型
- **📊 Schema可视化**: 直观的数据库表结构展示和统计
- **🔧 模块化架构**: 清晰的代码结构，易于维护和扩展
- **🎨 现代化界面**: 基于Streamlit的响应式Web界面
- **⚡ 本地部署**: 完全本地化运行，保护数据隐私
- **🔍 智能提示**: 内置丰富的查询示例和提示词优化

## 🏗️ 系统架构

```
SQL智能助手
├── 前端界面 (Streamlit)
├── 查询引擎 (Query Engine)
├── 模型管理 (LLM Manager)
├── 数据库管理 (Database Manager)
├── 提示词系统 (Prompts)
├── 适配器层 (Adapters)
└── 工具模块 (Utils)
```

## 📁 项目结构

```
sql-assistant/
├── README.md                    # 项目说明文档
├── PROJECT_STRUCTURE.md         # 项目结构详细说明
├── app.py                       # Streamlit应用主入口
├── config.py                    # 配置管理
├── database.py                  # 数据库连接管理
├── llm_model.py                # LLM模型管理
├── query_engine.py             # 查询引擎核心逻辑
├── start_app.py                # 应用启动脚本
│
├── prompts/                     # 提示词模块
│   ├── base_prompts.py         # 基础提示词模板
│   ├── sqlcoder_prompt.py      # SQLCoder专用提示词
│   └── sqlcoder_examples.json  # SQLCoder示例集合
│
├── adapters/                    # 适配器模块
│   └── sqlcoder_adapter.py     # SQLCoder Ollama适配器
│
├── utils/                       # 工具模块
│   ├── data_formatter.py       # 数据格式化工具
│   ├── schema_converter.py     # Schema转换工具
│   ├── sql_processor.py        # SQL处理工具
│   └── sql_post_processor.py   # SQL后处理工具
│
└── tests/                       # 测试模块
    └── test_sqlcoder.py        # SQLCoder测试套件
```

## 🚀 快速开始

### 环境要求

- **Python**: 3.8+
- **Ollama**: 本地Ollama服务
- **MySQL**: 数据库服务
- **操作系统**: Windows/Linux/macOS

### 安装依赖

#### 方法一：使用pip直接安装
```bash
# 核心依赖
pip install streamlit>=1.28.0
pip install langchain>=0.1.0
pip install langchain-community>=0.0.20
pip install langchain-ollama>=0.1.0

# 数据库连接
pip install mysql-connector-python>=8.0.0
pip install SQLAlchemy>=2.0.0

# 数据处理
pip install pandas>=2.0.0
pip install numpy>=1.24.0

# HTTP请求
pip install requests>=2.28.0

# 可选：开发和测试工具
pip install pytest>=7.0.0
pip install black>=23.0.0
pip install flake8>=6.0.0
```

#### 方法二：创建requirements.txt文件
创建 `requirements.txt` 文件并添加以下内容：
```txt
# Web框架
streamlit>=1.28.0

# LLM集成框架
langchain>=0.1.0
langchain-community>=0.0.20
langchain-ollama>=0.1.0

# 数据库连接
mysql-connector-python>=8.0.0
SQLAlchemy>=2.0.0

# 数据处理
pandas>=2.0.0
numpy>=1.24.0

# HTTP请求
requests>=2.28.0

# 开发工具（可选）
pytest>=7.0.0
black>=23.0.0
flake8>=6.0.0
```

然后执行：
```bash
pip install -r requirements.txt
```

#### 方法三：使用虚拟环境（推荐）
```bash
# 创建虚拟环境
python -m venv sql-assistant-env

# 激活虚拟环境
# Windows:
sql-assistant-env\Scripts\activate
# Linux/macOS:
source sql-assistant-env/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 依赖说明

| 依赖包 | 版本要求 | 用途说明 |
|--------|----------|----------|
| `streamlit` | >=1.28.0 | Web界面框架，提供响应式UI组件 |
| `langchain` | >=0.1.0 | LLM应用开发框架，核心抽象层 |
| `langchain-community` | >=0.0.20 | LangChain社区扩展，数据库集成 |
| `langchain-ollama` | >=0.1.0 | Ollama模型集成适配器 |
| `mysql-connector-python` | >=8.0.0 | MySQL数据库连接驱动 |
| `SQLAlchemy` | >=2.0.0 | SQL工具包和ORM框架 |
| `pandas` | >=2.0.0 | 数据分析和处理库 |
| `numpy` | >=1.24.0 | 数值计算基础库 |
| `requests` | >=2.28.0 | HTTP请求库，用于Ollama API调用 |

### 配置设置

1. **配置Ollama服务**
   ```python
   # 在 config.py 中修改Ollama配置
   OLLAMA_BASE_URL = "http://localhost:11434"  # 修改为您的Ollama服务地址
   ```

2. **配置数据库连接**
   ```python
   # 在 config.py 中修改数据库配置
   DATABASE_CONFIG = {
       "host": "localhost",
       "user": "your_username",
       "password": "your_password",
       "database": "your_database"
   }
   ```

3. **下载推荐模型**
   ```bash
   # 下载SQL专用模型（推荐）
   ollama pull sqlcoder:15b
   ollama pull sqlcoder:7b
   
   # 下载通用模型
   ollama pull qwen2.5:14b-instruct-q8_0
   ollama pull deepseek-r1:7b
   ```

### 启动应用

```bash
# 方法1: 直接运行主应用
python app.py

# 方法2: 使用启动脚本
python start_app.py

# 方法3: 使用Streamlit命令
streamlit run app.py
```

应用启动后，在浏览器中访问 `http://localhost:8501`

## 🎯 功能特性

### 1. 智能模型选择

- **推荐SQL模型**: 专为SQL查询优化的模型
- **SQL专用模型**: SQLCoder系列模型
- **通用模型**: 支持大、中、小型通用语言模型
- **自动适配**: 根据模型类型自动选择最佳提示词策略

### 2. 数据库Schema可视化

- **分表显示**: 每个表独立展示，包含详细列信息
- **单表选择**: 选择特定表查看详细统计信息
- **智能描述**: 自动生成列的中文描述
- **统计信息**: 显示表的列数、主要数据类型、ID字段等

### 3. 查询功能

- **自然语言查询**: 输入中文问题，自动生成SQL
- **直接SQL执行**: 支持直接输入SQL语句执行
- **查询示例**: 内置丰富的查询示例库
- **结果格式化**: 支持表格和原始格式显示

### 4. 高级特性

- **连接状态检查**: 实时检测数据库和模型连接状态
- **SQL优化**: 自动清理和优化生成的SQL语句
- **错误处理**: 完善的错误提示和处理机制
- **性能监控**: 查询执行时间和状态监控

## 🔧 技术栈

### 核心技术

- **前端框架**: Streamlit - 快速构建数据应用
- **LLM集成**: LangChain - 大语言模型应用框架
- **模型服务**: Ollama - 本地LLM服务
- **数据库**: MySQL - 关系型数据库
- **数据处理**: Pandas - 数据分析和处理

### 支持的模型

#### SQL专用模型（推荐）
- `sqlcoder:15b` - 15B参数的SQL专用模型
- `sqlcoder:7b` - 7B参数的SQLCoder
- `mannix/defog-llama3-sqlcoder-8b:latest` - 基于Llama3的SQL编码器
- `duckdb-nsql:7b` - DuckDB自然语言到SQL模型

#### 通用大语言模型
- **Qwen系列**: qwen2.5:72b, qwen2.5:32b, qwen2.5:14b, qwen2.5:7b
- **DeepSeek系列**: deepseek-r1:14b, deepseek-r1:7b
- **QwQ系列**: QwQ:latest, QwQ:32b

## 🏛️ 技术架构详解

### 整体架构设计

本项目采用**分层架构模式**，将系统分为以下几个核心层次：

```
┌─────────────────────────────────────────────────────────────┐
│                    前端展示层 (Presentation Layer)              │
│                      Streamlit Web UI                      │
├─────────────────────────────────────────────────────────────┤
│                    业务逻辑层 (Business Layer)                 │
│              Query Engine + LLM Manager                    │
├─────────────────────────────────────────────────────────────┤
│                    服务适配层 (Service Layer)                  │
│           Prompt Manager + SQLCoder Adapter                │
├─────────────────────────────────────────────────────────────┤
│                    数据访问层 (Data Access Layer)              │
│              Database Manager + Utils                      │
├─────────────────────────────────────────────────────────────┤
│                    基础设施层 (Infrastructure Layer)           │
│              Ollama + MySQL + LangChain                    │
└─────────────────────────────────────────────────────────────┘
```

### 前端实现 (Frontend Implementation)

#### 🎨 Streamlit框架选择
- **技术选型**: Streamlit - Python原生Web应用框架
- **选择原因**: 
  - 快速开发：无需前后端分离，Python一站式开发
  - 数据科学友好：原生支持Pandas、图表等数据展示
  - 响应式设计：自动适配移动端和桌面端
  - 组件丰富：内置表单、图表、侧边栏等UI组件

#### 🖥️ 界面架构设计
```python
# app.py 主要结构
def main():
    # 1. 页面配置和样式设置
    st.set_page_config(
        page_title="SQL智能助手",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 2. 侧边栏：模型选择和连接状态
    with st.sidebar:
        model_selection()      # 模型选择界面
        connection_status()    # 连接状态检查
    
    # 3. 主区域：Schema展示和查询界面
    col1, col2 = st.columns([1, 1])
    with col1:
        schema_visualization() # Schema可视化
    with col2:
        query_interface()      # 查询输入和结果展示
```

#### 🎯 核心UI组件
1. **模型选择器**: 动态加载可用模型，分类展示
2. **连接状态指示器**: 实时检测数据库和LLM连接状态
3. **Schema可视化器**: 表格展示数据库结构，支持折叠展开
4. **查询输入框**: 支持自然语言和SQL两种输入模式
5. **结果展示器**: 表格和原始格式双模式显示

### 后端实现 (Backend Implementation)

#### 🔧 核心模块架构

##### 1. 查询引擎 (Query Engine)
```python
class QueryEngine:
    def __init__(self):
        self.database_manager = database_manager
        self.llm_manager = llm_manager
        self.prompt_manager = prompt_manager
    
    def process_query(self, query, is_natural_language=True):
        """查询处理主流程"""
        if is_natural_language:
            # 自然语言 -> SQL 转换
            sql = self.generate_sql(query)
        else:
            # 直接SQL执行
            sql = self.clean_sql(query)
        
        # 执行SQL并返回结果
        return self.execute_sql(sql)
```

##### 2. LLM管理器 (LLM Manager)
```python
class LLMManager:
    def __init__(self):
        self.current_model = None
        self.ollama_llm = None
        self.sqlcoder_adapter = SQLCoderAdapter()
    
    def generate_sql(self, natural_query, schema_info):
        """根据模型类型选择生成策略"""
        if self.is_sqlcoder_model():
            return self.sqlcoder_adapter.generate_sql(
                natural_query, schema_info
            )
        else:
            return self.generic_llm_generate(
                natural_query, schema_info
            )
```

##### 3. 数据库管理器 (Database Manager)
```python
class DatabaseManager:
    def __init__(self):
        self.db = None
        self.connection_uri = self.build_connection_uri()
    
    def get_database(self):
        """懒加载数据库连接"""
        if self.db is None:
            self.db = SQLDatabase.from_uri(self.connection_uri)
        return self.db
    
    def execute_query(self, sql):
        """安全执行SQL查询"""
        try:
            result = self.get_database().run(sql)
            return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
```

#### 🔄 模块间通信机制
- **全局实例模式**: 各管理器采用单例模式，确保状态一致性
- **事件驱动**: Streamlit的响应式更新机制
- **错误传播**: 统一的错误处理和状态反馈机制

### 🧠 自然语言转SQL详细流程

#### 完整转换流程图
```
用户输入自然语言查询
         ↓
    查询预处理和验证
         ↓
    选择合适的LLM模型
         ↓
┌─────────────────┬─────────────────┐
│   SQLCoder模型   │    通用LLM模型    │
│      路径        │       路径        │
└─────────────────┴─────────────────┘
         ↓                 ↓
   SQLCoder专用        通用LLM提示词
    提示词构建           模板构建
         ↓                 ↓
   Schema信息注入      Schema信息注入
         ↓                 ↓
   Few-shot示例        Few-shot示例
         ↓                 ↓
    模型推理生成         模型推理生成
         ↓                 ↓
         └─────────┬─────────┘
                   ↓
            SQL后处理和清理
                   ↓
            SQL语法验证
                   ↓
            数据库执行
                   ↓
            结果格式化返回
```

#### 🎯 Step 1: 查询预处理
```python
def preprocess_query(self, user_input):
    """查询预处理"""
    # 1. 去除多余空格和特殊字符
    cleaned_input = user_input.strip()
    
    # 2. 检测查询类型（自然语言 vs SQL）
    if self.is_sql_query(cleaned_input):
        return {"type": "sql", "content": cleaned_input}
    else:
        return {"type": "natural", "content": cleaned_input}
    
    # 3. 安全性检查（防止SQL注入）
    if self.contains_dangerous_keywords(cleaned_input):
        raise SecurityError("检测到危险操作")
```

#### 🎯 Step 2: 模型选择策略
```python
def select_generation_strategy(self, model_name):
    """根据模型类型选择生成策略"""
    if model_name in ["sqlcoder:15b", "sqlcoder:7b"]:
        return "sqlcoder_specialized"
    elif "sqlcoder" in model_name.lower():
        return "sqlcoder_generic"
    else:
        return "general_llm"
```

#### 🎯 Step 3: SQLCoder专用路径
```python
def sqlcoder_generation_path(self, query, schema_info):
    """SQLCoder专用生成路径"""
    # 1. 构建SQLCoder专用提示词
    prompt = self.build_sqlcoder_prompt(query, schema_info)
    
    # 2. Schema信息转换为SQLCoder格式
    schema_context = self.convert_to_sqlcoder_format(schema_info)
    
    # 3. 添加Few-shot示例
    examples = self.get_sqlcoder_examples()
    
    # 4. 组装完整提示
    full_prompt = f"""
    {schema_context}
    
    {examples}
    
    Question: {query}
    SQL:
    """
    
    # 5. 调用SQLCoder模型
    response = self.sqlcoder_adapter.generate(
        prompt=full_prompt,
        temperature=0.1,  # 低温度确保一致性
        max_tokens=500
    )
    
    return response
```

#### 🎯 Step 4: 通用LLM路径
```python
def general_llm_generation_path(self, query, schema_info):
    """通用LLM生成路径"""
    # 1. 构建LangChain SQL链
    sql_chain = self.prompt_manager.create_sql_chain(
        llm=self.ollama_llm,
        database=self.database_manager.get_database()
    )
    
    # 2. 添加详细的SQL生成指导
    enhanced_query = f"""
    请根据以下数据库Schema生成SQL查询：
    
    数据库表结构：
    {schema_info}
    
    查询要求：{query}
    
    注意事项：
    - 使用标准SQL语法
    - 添加适当的LIMIT限制
    - 确保列名和表名正确
    - 优化查询性能
    """
    
    # 3. 执行生成
    response = sql_chain.invoke({"question": enhanced_query})
    
    return response
```

#### 🎯 Step 5: SQL后处理和清理
```python
def post_process_sql(self, raw_sql_response):
    """SQL后处理流程"""
    # 1. 提取SQL语句
    sql = self.sql_processor.extract_sql(raw_sql_response)
    
    # 2. 清理和标准化
    cleaned_sql = self.sql_processor.clean_sql(sql)
    
    # 3. 表名和列名校正
    corrected_sql = self.sql_post_processor.correct_names(
        cleaned_sql, self.get_table_columns()
    )
    
    # 4. 语法验证
    if not self.validate_sql_syntax(corrected_sql):
        raise SQLSyntaxError("生成的SQL语法不正确")
    
    # 5. 安全检查
    if self.contains_dangerous_operations(corrected_sql):
        raise SecurityError("SQL包含危险操作")
    
    return corrected_sql
```

#### 🎯 Step 6: 执行和结果处理
```python
def execute_and_format_result(self, sql):
    """执行SQL并格式化结果"""
    # 1. 数据库执行
    execution_result = self.database_manager.execute_query(sql)
    
    if not execution_result["success"]:
        return {
            "success": False,
            "error": execution_result["error"],
            "sql": sql
        }
    
    # 2. 结果格式化
    formatted_data = self.data_formatter.format_query_result(
        execution_result["data"]
    )
    
    # 3. 返回完整结果
    return {
        "success": True,
        "sql": sql,
        "data": formatted_data,
        "row_count": len(formatted_data),
        "execution_time": execution_result.get("execution_time", 0)
    }
```

### 🔧 关键技术实现细节

#### 1. Schema动态转换
```python
def convert_schema_for_llm(self, table_columns):
    """将配置中的表结构转换为LLM可理解的格式"""
    schema_text = ""
    for table_name, columns in table_columns.items():
        schema_text += f"\n表名: {table_name}\n"
        schema_text += "列信息:\n"
        for col in columns:
            schema_text += f"  - {col['name']} ({col['type']})"
            if col.get('description'):
                schema_text += f" - {col['description']}"
            schema_text += "\n"
    return schema_text
```

#### 2. 提示词工程优化
```python
def build_optimized_prompt(self, query, schema, examples):
    """构建优化的提示词"""
    return f"""
你是一个专业的SQL查询生成专家。请根据以下信息生成准确的SQL查询：

数据库Schema:
{schema}

Few-shot示例:
{examples}

用户查询: {query}

要求:
1. 生成标准的MySQL语法
2. 确保表名和列名完全正确
3. 添加适当的LIMIT限制（默认10条）
4. 优化查询性能
5. 只返回SQL语句，不要其他解释

SQL:
"""
```

#### 3. 错误处理和重试机制
```python
def robust_sql_generation(self, query, max_retries=3):
    """带重试机制的SQL生成"""
    for attempt in range(max_retries):
        try:
            sql = self.generate_sql(query)
            if self.validate_sql(sql):
                return sql
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            # 调整策略重试
            self.adjust_generation_strategy()
    
    raise Exception("SQL生成失败，已达到最大重试次数")
```

### 🚀 性能优化策略

#### 1. 连接池管理
- 数据库连接采用懒加载模式
- LLM模型实例复用，避免重复初始化
- 缓存常用查询结果

#### 2. 查询优化
- 自动添加LIMIT限制，防止大结果集
- SQL语句缓存，相同查询直接返回
- 异步执行长时间查询

#### 3. 内存管理
- 及时清理大型查询结果
- 使用生成器处理大数据集
- 限制并发查询数量

### 🔍 核心算法实现

#### 1. SQL语句清理算法
```python
class SQLProcessor:
    def clean_sql(self, sql_text):
        """多层次SQL清理算法"""
        # 第一层：移除代码块标记
        sql_text = re.sub(r'```sql\s*', '', sql_text)
        sql_text = re.sub(r'```\s*', '', sql_text)
        
        # 第二层：移除常见前缀
        prefixes = ['SQL:', 'sql:', 'Query:', 'SELECT', 'select']
        for prefix in prefixes:
            if sql_text.strip().startswith(prefix):
                sql_text = sql_text.strip()[len(prefix):].strip()
        
        # 第三层：特殊字符标准化
        sql_text = sql_text.replace('≥', '>=').replace('≤', '<=')
        
        # 第四层：多行SQL合并
        lines = [line.strip() for line in sql_text.split('\n') if line.strip()]
        sql_text = ' '.join(lines)
        
        return sql_text.strip()
```

#### 2. 智能表名列名校正
```python
class SQLPostProcessor:
    def correct_table_column_names(self, sql, table_columns):
        """智能校正表名和列名"""
        corrected_sql = sql
        
        # 校正表名（模糊匹配）
        for correct_table in table_columns.keys():
            pattern = r'\b' + re.escape(correct_table.lower()) + r'\b'
            corrected_sql = re.sub(
                pattern, correct_table, corrected_sql, flags=re.IGNORECASE
            )
        
        # 校正列名（基于编辑距离）
        for table_name, columns in table_columns.items():
            for col_info in columns:
                correct_col = col_info['name']
                # 查找相似的列名并替换
                pattern = r'\b\w*' + re.escape(correct_col[1:-1]) + r'\w*\b'
                matches = re.findall(pattern, corrected_sql, re.IGNORECASE)
                for match in matches:
                    if self.similarity(match.lower(), correct_col.lower()) > 0.8:
                        corrected_sql = corrected_sql.replace(match, correct_col)
        
        return corrected_sql
    
    def similarity(self, a, b):
        """计算字符串相似度"""
        from difflib import SequenceMatcher
        return SequenceMatcher(None, a, b).ratio()
```

#### 3. 动态提示词构建
```python
class PromptBuilder:
    def build_context_aware_prompt(self, query, schema, model_type):
        """根据查询内容和模型类型构建上下文感知提示词"""
        
        # 分析查询意图
        query_intent = self.analyze_query_intent(query)
        
        # 选择相关表
        relevant_tables = self.select_relevant_tables(query, schema)
        
        # 构建精简Schema
        focused_schema = self.build_focused_schema(relevant_tables, schema)
        
        # 选择合适的示例
        examples = self.select_relevant_examples(query_intent)
        
        if model_type == "sqlcoder":
            return self.build_sqlcoder_prompt(query, focused_schema, examples)
        else:
            return self.build_general_prompt(query, focused_schema, examples)
    
    def analyze_query_intent(self, query):
        """分析查询意图"""
        intent_keywords = {
            "aggregation": ["统计", "计算", "总数", "平均", "最大", "最小", "求和"],
            "filtering": ["查找", "筛选", "条件", "满足", "大于", "小于", "等于"],
            "joining": ["关联", "连接", "对应", "匹配", "相关"],
            "sorting": ["排序", "排列", "最高", "最低", "前", "后"],
            "grouping": ["分组", "按照", "每个", "各个"]
        }
        
        detected_intents = []
        for intent, keywords in intent_keywords.items():
            if any(keyword in query for keyword in keywords):
                detected_intents.append(intent)
        
        return detected_intents
```

### 🛡️ 安全性实现

#### 1. SQL注入防护
```python
class SecurityValidator:
    DANGEROUS_KEYWORDS = [
        'DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE',
        'TRUNCATE', 'EXEC', 'EXECUTE', 'UNION', 'SCRIPT'
    ]
    
    def validate_sql_safety(self, sql):
        """SQL安全性验证"""
        sql_upper = sql.upper()
        
        # 检查危险关键词
        for keyword in self.DANGEROUS_KEYWORDS:
            if keyword in sql_upper:
                raise SecurityError(f"检测到危险操作: {keyword}")
        
        # 检查多语句执行
        if ';' in sql and sql.count(';') > 1:
            raise SecurityError("不允许执行多条SQL语句")
        
        # 检查注释注入
        if '--' in sql or '/*' in sql:
            raise SecurityError("检测到SQL注释，可能存在注入风险")
        
        return True
```

#### 2. 查询结果限制
```python
class QueryLimiter:
    def apply_safety_limits(self, sql):
        """应用安全限制"""
        # 自动添加LIMIT
        if 'LIMIT' not in sql.upper():
            sql += ' LIMIT 100'
        
        # 检查LIMIT值
        limit_match = re.search(r'LIMIT\s+(\d+)', sql, re.IGNORECASE)
        if limit_match:
            limit_value = int(limit_match.group(1))
            if limit_value > 1000:
                sql = re.sub(r'LIMIT\s+\d+', 'LIMIT 1000', sql, flags=re.IGNORECASE)
        
        return sql
```

### 📊 监控和日志

#### 1. 性能监控
```python
class PerformanceMonitor:
    def __init__(self):
        self.query_stats = []
    
    def monitor_query(self, func):
        """查询性能监控装饰器"""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                self.query_stats.append({
                    'timestamp': datetime.now(),
                    'execution_time': execution_time,
                    'success': True,
                    'query_length': len(args[0]) if args else 0
                })
                
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                self.query_stats.append({
                    'timestamp': datetime.now(),
                    'execution_time': execution_time,
                    'success': False,
                    'error': str(e)
                })
                raise
        return wrapper
```

#### 2. 智能日志记录
```python
class SmartLogger:
    def log_query_generation(self, query, sql, model, success):
        """记录查询生成过程"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'natural_query': query,
            'generated_sql': sql,
            'model_used': model,
            'success': success,
            'query_complexity': self.calculate_complexity(query),
            'sql_complexity': self.calculate_sql_complexity(sql)
        }
        
        # 写入日志文件或数据库
        self.write_log(log_entry)
    
    def calculate_complexity(self, query):
        """计算查询复杂度"""
        complexity_score = 0
        complexity_score += len(query.split()) * 0.1  # 词数
        complexity_score += query.count('和') * 0.5   # 连接词
        complexity_score += query.count('或') * 0.5   # 逻辑词
        return min(complexity_score, 10.0)  # 最大10分
```

### 🔧 扩展性设计

#### 1. 插件化模型支持
```python
class ModelRegistry:
    def __init__(self):
        self.registered_models = {}
    
    def register_model(self, model_name, adapter_class):
        """注册新的模型适配器"""
        self.registered_models[model_name] = adapter_class
    
    def get_adapter(self, model_name):
        """获取模型适配器"""
        if model_name in self.registered_models:
            return self.registered_models[model_name]()
        else:
            return DefaultAdapter()

# 使用示例
model_registry = ModelRegistry()
model_registry.register_model("custom_sql_model", CustomSQLAdapter)
```

#### 2. 数据库适配器模式
```python
class DatabaseAdapter:
    """数据库适配器基类"""
    def get_schema_query(self):
        raise NotImplementedError
    
    def format_limit_clause(self, limit):
        raise NotImplementedError

class MySQLAdapter(DatabaseAdapter):
    def get_schema_query(self):
        return "SHOW TABLES"
    
    def format_limit_clause(self, limit):
        return f"LIMIT {limit}"

class PostgreSQLAdapter(DatabaseAdapter):
    def get_schema_query(self):
        return "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
    
    def format_limit_clause(self, limit):
        return f"LIMIT {limit}"
```

### 🎯 最佳实践总结

#### 1. 代码组织原则
- **单一职责**: 每个模块只负责一个核心功能
- **依赖注入**: 通过构造函数注入依赖，便于测试
- **配置外置**: 所有配置集中在config.py中管理
- **错误处理**: 统一的异常处理和错误传播机制

#### 2. 性能优化原则
- **懒加载**: 数据库连接和模型实例按需创建
- **缓存策略**: 缓存常用查询和Schema信息
- **资源管理**: 及时释放大型对象和连接
- **异步处理**: 长时间操作使用异步模式

#### 3. 安全性原则
- **输入验证**: 所有用户输入都进行安全检查
- **权限控制**: 数据库用户使用最小权限原则
- **SQL限制**: 自动添加查询限制，防止资源耗尽
- **日志审计**: 记录所有重要操作和异常

#### 4. 可维护性原则
- **模块化设计**: 清晰的模块边界和接口定义
- **文档完整**: 每个函数都有详细的文档说明
- **测试覆盖**: 核心功能都有对应的单元测试
- **版本控制**: 使用语义化版本号管理

## 📊 数据库Schema

项目默认支持销售订单管理系统的数据库Schema，包含以下表：

- **Customer**: 客户信息表
- **Employee**: 员工信息表
- **Product**: 产品信息表
- **SalesOrder**: 销售订单表
- **LineItem**: 订单明细表
- **InventoryLog**: 库存日志表
- **Supplier**: 供应商信息表

## 🎨 界面预览

### 主界面功能
- 🤖 **模型配置区**: 选择和配置LLM模型
- 🔗 **连接状态**: 实时显示数据库和模型连接状态
- 📊 **Schema展示**: 可视化数据库表结构
- 💬 **查询界面**: 自然语言和SQL查询输入
- 📋 **结果展示**: 格式化的查询结果显示

### Schema可视化特性
- 📋 **分表显示**: 每个表独立的可展开区域
- 🔍 **单表选择**: 下拉选择特定表查看详情
- 📈 **统计信息**: 列数、数据类型、ID字段统计
- 💡 **查询示例**: 每个表的常用查询示例

## 🔧 配置说明

### 模型配置
```python
# 推荐的SQL查询模型（按优先级排序）
RECOMMENDED_SQL_MODELS = [
    "sqlcoder:15b",                              # 最佳SQL专用模型
    "mannix/defog-llama3-sqlcoder-8b:latest",    # 基于Llama3的SQL模型
    "sqlcoder:7b",                               # 较小的SQL专用模型
    "duckdb-nsql:7b",                            # DuckDB专用模型
    "qwen2.5:14b-instruct-q8_0"                  # 通用模型备选
]
```

### 数据库配置
```python
DATABASE_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "SalesOrderSchema"
}
```

### 应用配置
```python
APP_CONFIG = {
    "title": "🤖智能SQL查询助手🤖",
    "description": "基于本地Ollama模型的数据库查询系统",
    "max_iterations": 3,
    "max_execution_time": 30,
    "default_limit": 10
}
```

## 🧪 测试

项目包含完整的测试套件：

```bash
# 运行SQLCoder测试
cd tests
python test_sqlcoder.py

# 测试内容包括：
# - 模型连接测试
# - SQL生成测试
# - 查询执行测试
# - 错误处理测试
```

## 🔍 使用示例

### 自然语言查询示例

```
用户输入: "查询所有客户的姓名和邮箱"
生成SQL: SELECT FirstName, LastName, Email FROM Customer;

用户输入: "显示前10个订单的详细信息"
生成SQL: SELECT * FROM SalesOrder LIMIT 10;

用户输入: "查找价格超过100的产品"
生成SQL: SELECT ProductName, UnitPrice FROM Product WHERE UnitPrice > 100;

用户输入: "统计每个客户的订单数量"
生成SQL: SELECT c.FirstName, c.LastName, COUNT(s.SalesOrderID) as OrderCount 
         FROM Customer c LEFT JOIN SalesOrder s ON c.CustomerID = s.CustomerID 
         GROUP BY c.CustomerID, c.FirstName, c.LastName;
```

## 🛠️ 开发指南

### 添加新模型支持

1. 在 `config.py` 中添加模型到 `AVAILABLE_MODELS`
2. 如果是SQL专用模型，添加到 `MODEL_CATEGORIES["sql_specialized"]`
3. 在 `llm_model.py` 中更新模型检测逻辑

### 扩展数据库支持

1. 在 `config.py` 中更新 `TABLE_COLUMNS` 配置
2. 修改 `DATABASE_CONFIG` 连接信息
3. 更新 `TABLE_INFO` 描述信息

### 自定义提示词

1. 修改 `prompts/base_prompts.py` 中的提示模板
2. 添加新的示例到 `FEW_SHOT_EXAMPLES`
3. 为特定模型创建专用提示词文件

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 更新日志

### v1.0.0 (当前版本)
- ✅ 完整的SQL智能助手功能
- ✅ 多模型支持（SQL专用 + 通用模型）
- ✅ 数据库Schema可视化
- ✅ 模块化架构设计
- ✅ SQLCoder专用适配器
- ✅ 完善的错误处理和测试

## 🚀 部署指南

### 本地开发部署

#### 1. 开发环境设置
```bash
# 克隆项目
git clone <repository-url>
cd sql-assistant

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
streamlit run app.py
```

#### 2. 环境变量配置
创建 `.env` 文件：
```env
# 数据库配置
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=SalesOrderSchema

# Ollama配置
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TIMEOUT=60

# 应用配置
APP_DEBUG=True
APP_LOG_LEVEL=INFO
```

### 生产环境部署

#### 1. Docker部署
创建 `Dockerfile`：
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8501

# 启动命令
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

创建 `docker-compose.yml`：
```yaml
version: '3.8'

services:
  sql-assistant:
    build: .
    ports:
      - "8501:8501"
    environment:
      - DB_HOST=mysql
      - DB_USER=root
      - DB_PASSWORD=password
      - DB_NAME=SalesOrderSchema
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - mysql
      - ollama
    volumes:
      - ./config.py:/app/config.py

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: SalesOrderSchema
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  mysql_data:
  ollama_data:
```

#### 2. 云服务器部署
```bash
# 在云服务器上
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx

# 创建应用目录
sudo mkdir /opt/sql-assistant
sudo chown $USER:$USER /opt/sql-assistant
cd /opt/sql-assistant

# 部署应用
git clone <repository-url> .
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 配置Nginx反向代理
sudo nano /etc/nginx/sites-available/sql-assistant
```

Nginx配置示例：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## 🔧 故障排除

### 常见问题及解决方案

#### 1. 连接问题

**问题**: Ollama连接失败
```
ConnectionError: Cannot connect to Ollama service
```

**解决方案**:
```bash
# 检查Ollama服务状态
ollama list

# 启动Ollama服务
ollama serve

# 检查端口是否被占用
netstat -an | grep 11434

# 修改config.py中的OLLAMA_BASE_URL
OLLAMA_BASE_URL = "http://localhost:11434"
```

**问题**: 数据库连接失败
```
mysql.connector.errors.DatabaseError: 2003 (HY000): Can't connect to MySQL server
```

**解决方案**:
```bash
# 检查MySQL服务状态
sudo systemctl status mysql

# 启动MySQL服务
sudo systemctl start mysql

# 检查数据库配置
mysql -u root -p -e "SHOW DATABASES;"

# 验证用户权限
mysql -u your_username -p -e "SELECT USER(), DATABASE();"
```

#### 2. 模型问题

**问题**: SQLCoder模型不可用
```
Model 'sqlcoder:15b' not found
```

**解决方案**:
```bash
# 下载SQLCoder模型
ollama pull sqlcoder:15b
ollama pull sqlcoder:7b

# 检查已安装模型
ollama list

# 测试模型
ollama run sqlcoder:7b "SELECT * FROM users LIMIT 5;"
```

**问题**: 模型响应慢或超时
```
TimeoutError: Model response timeout
```

**解决方案**:
```python
# 在config.py中调整超时设置
OLLAMA_CONFIG = {
    "timeout": 120,  # 增加超时时间
    "temperature": 0.1,
    "max_tokens": 500
}

# 或选择更小的模型
RECOMMENDED_SQL_MODELS = [
    "sqlcoder:7b",  # 使用7B而不是15B模型
    "qwen2.5:7b"
]
```

#### 3. 性能问题

**问题**: 查询响应慢
```
Query execution time > 30 seconds
```

**解决方案**:
```python
# 优化数据库查询
# 1. 添加索引
CREATE INDEX idx_customer_id ON SalesOrder(CustomerID);
CREATE INDEX idx_product_id ON LineItem(ProductID);

# 2. 限制查询结果
DEFAULT_LIMIT = 50  # 减少默认限制

# 3. 使用查询缓存
ENABLE_QUERY_CACHE = True
CACHE_TTL = 300  # 5分钟缓存
```

**问题**: 内存使用过高
```
MemoryError: Unable to allocate memory
```

**解决方案**:
```python
# 在config.py中限制资源使用
MAX_RESULT_ROWS = 1000
MAX_QUERY_LENGTH = 1000
ENABLE_RESULT_STREAMING = True

# 清理大型对象
import gc
gc.collect()
```

#### 4. 界面问题

**问题**: Streamlit页面无法加载
```
StreamlitAPIException: Streamlit server error
```

**解决方案**:
```bash
# 清除Streamlit缓存
streamlit cache clear

# 重启应用
pkill -f streamlit
streamlit run app.py

# 检查端口占用
lsof -i :8501
```

**问题**: 页面样式异常
```
CSS styles not loading properly
```

**解决方案**:
```python
# 在app.py中强制刷新样式
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# 清除浏览器缓存
# Ctrl+F5 (Windows) 或 Cmd+Shift+R (Mac)
```

### 调试技巧

#### 1. 启用详细日志
```python
import logging

# 在app.py开头添加
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sql_assistant.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

#### 2. 性能分析
```python
import time
import functools

def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

# 使用装饰器监控关键函数
@timing_decorator
def generate_sql(query):
    # 函数实现
    pass
```

#### 3. 错误追踪
```python
import traceback

try:
    # 可能出错的代码
    result = process_query(user_input)
except Exception as e:
    # 详细错误信息
    error_details = {
        'error_type': type(e).__name__,
        'error_message': str(e),
        'traceback': traceback.format_exc(),
        'user_input': user_input,
        'timestamp': datetime.now().isoformat()
    }
    
    # 记录到日志
    logger.error(f"Query processing failed: {error_details}")
    
    # 显示用户友好的错误信息
    st.error("查询处理失败，请检查输入或联系管理员")
```

## 🔒 安全说明

- 本项目完全本地运行，不会向外部发送数据
- 数据库连接信息请妥善保管
- 建议使用专门的数据库用户，限制权限
- 生产环境请修改默认密码

## 📞 支持与反馈

如果您在使用过程中遇到问题或有改进建议，请：

1. 查看项目文档和FAQ
2. 提交Issue描述问题
3. 参与讨论和改进

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

**🎉 感谢使用SQL智能助手！让数据查询变得更简单、更智能！**